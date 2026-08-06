#!/usr/bin/env python3
"""
wi.py — Writing Intelligence v4 deterministic verification CLI.

The free floor: every check here is deterministic, offline, dependency-free, and
language-independent where it can be. It compares strings, numbers, and dates.
It never judges prose quality and never calls a model.

Stdlib only, Python 3.8+. Runs air-gapped.

Subcommands
-----------
  preserve       Snapshot a file before editing (Law B).
  scan-sources   Flag injection indicators and hidden text in sources (Law F).
  extract-claims Build a claim ledger from a document (Proof Protocol §1-3).
  verify         Span lock + quotation + numeric + date checks (Law D).
  gate           Emit RELEASE / HOLD / BLOCK with repairs.

Exit codes (with --exit-code on `gate`): 0 RELEASE, 1 HOLD, 2 BLOCK.
"""

import argparse
import datetime as _dt
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

VERSION = "4.0.0"

# --------------------------------------------------------------------------
# Text normalization. Offsets are Unicode code point indices over NFC text.
# --------------------------------------------------------------------------

def nfc(text):
    """Normalize to NFC. Done once, before hashing or offsetting anything."""
    return unicodedata.normalize("NFC", text)


def fold_ws(text):
    """Collapse all whitespace runs to a single space. For verbatim comparison
    that should survive line wrapping and PDF extraction artifacts."""
    return re.sub(r"\s+", " ", text).strip()


def read_text(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    return nfc(raw)


def load_sources(paths):
    """Load every readable text file under the given paths."""
    sources = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files = sorted(f for f in p.rglob("*") if f.is_file())
        else:
            files = [p]
        for f in files:
            if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf",
                                    ".zip", ".docx", ".xlsx", ".pptx"}:
                # Binary or needs extraction first. Report rather than skip silently.
                sources.append({"id": str(f), "title": f.name, "text": None,
                                "note": "not plain text; extract before verifying"})
                continue
            try:
                sources.append({"id": str(f), "title": f.name, "text": read_text(f)})
            except Exception as exc:  # unreadable is a finding, not a crash
                sources.append({"id": str(f), "title": f.name, "text": None,
                                "note": "unreadable: %s" % exc})
    return sources


# --------------------------------------------------------------------------
# Sentence segmentation. Honest about its own limits (Law C, Law 20).
# --------------------------------------------------------------------------

# Scripts with no reliable whitespace/period sentence convention.
_NO_SPACE_RANGES = [
    (0x0E00, 0x0E7F),   # Thai
    (0x1780, 0x17FF),   # Khmer
    (0x0F00, 0x0FFF),   # Tibetan
    (0x1000, 0x109F),   # Myanmar
]
_CJK_RANGES = [
    (0x3040, 0x30FF),   # Kana
    (0x4E00, 0x9FFF),   # CJK unified
    (0xAC00, 0xD7AF),   # Hangul
    (0x3400, 0x4DBF),
]

_TERMINATORS = ".!?\u3002\uFF01\uFF1F\u061F\u06D4\u0964\u0965"


def _in_ranges(cp, ranges):
    return any(lo <= cp <= hi for lo, hi in ranges)


def script_profile(text):
    """Return (tier, note). Tier drives which metrics are legitimate."""
    sample = text[:4000]
    if not sample.strip():
        return "unknown", "empty text"
    cjk = sum(1 for ch in sample if _in_ranges(ord(ch), _CJK_RANGES))
    nospace = sum(1 for ch in sample if _in_ranges(ord(ch), _NO_SPACE_RANGES))
    letters = sum(1 for ch in sample if ch.isalpha())
    if letters == 0:
        return "unknown", "no letters detected"
    if nospace / letters > 0.2:
        return "tier3", "script without whitespace word boundaries; word metrics unavailable"
    if cjk / letters > 0.2:
        return "tier2", "CJK script; word-based metrics unavailable, structural metrics valid"
    return "tier1", "space-delimited script; word metrics available"


def sentences(text):
    """Split into sentences. Heuristic, and it says so via script_profile.

    Handles Latin, Cyrillic, Greek, Arabic, Devanagari and CJK terminators.
    For scripts with no sentence-final punctuation convention this returns
    paragraph-sized units, which is the honest result rather than a wrong one.
    """
    text = nfc(text)
    out, buf = [], []
    # Common abbreviations that should not end a sentence in Latin scripts.
    abbrev = re.compile(r"(?:^|\s)(?:[A-Z][a-z]{0,3}|e\.g|i\.e|vs|cf|et al|Dr|Mr|Mrs|Ms|Prof|Fig|No|pp)\.$")
    i = 0
    while i < len(text):
        ch = text[i]
        buf.append(ch)
        if ch in _TERMINATORS:
            nxt = text[i + 1] if i + 1 < len(text) else " "
            cur = "".join(buf)
            # Decimal numbers: 3.5 — not a boundary.
            if ch == "." and i + 1 < len(text) and text[i + 1].isdigit() \
               and i > 0 and text[i - 1].isdigit():
                i += 1
                continue
            if ch == "." and abbrev.search(cur):
                i += 1
                continue
            if nxt.isspace() or nxt in "\u201d\"')]" or ord(ch) > 0x3000:
                # Absorb trailing closers so a closing quote stays with its
                # sentence instead of opening the next one.
                j = i + 1
                while j < len(text) and text[j] in "\u201d\u2019\"')]\u00bb":
                    buf.append(text[j])
                    j += 1
                s = "".join(buf).strip()
                if s:
                    out.append(s)
                buf = []
                i = j
                continue
        i += 1
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return out


# --------------------------------------------------------------------------
# Claim detection. Signal is checkable content, not assertive tone.
# --------------------------------------------------------------------------

RE_NUMBER = re.compile(r"(?<![\w.])\d[\d,._]*\.?\d*\s?%?")
RE_PERCENT = re.compile(r"\d[\d,.]*\s?(?:%|percent|per cent|pct)", re.I)
RE_CURRENCY = re.compile(r"[$€£¥₹₦₽]\s?\d|(?:\d[\d,.]*)\s?(?:USD|EUR|GBP|JPY|NGN|INR|CAD|AUD)\b", re.I)
RE_YEAR = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")
RE_ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
RE_QUOTE = re.compile(r"[\"\u201c]([^\"\u201c\u201d]{12,400})[\"\u201d]")
RE_ATTRIB = re.compile(r"\b(according to|as reported by|per the|cited in|stated that|found that|concluded that|writes that|notes that)\b", re.I)
RE_SUPERLATIVE = re.compile(r"\b(largest|smallest|first|only|best|worst|highest|lowest|fastest|leading|most|least|unprecedented)\b", re.I)
RE_COMPARATIVE = re.compile(r"\b(more than|less than|fewer than|greater than|twice|three times|double|triple|compared (?:to|with)|outperform\w*)\b", re.I)
RE_CAUSAL = re.compile(r"\b(causes?|caused|because of|due to|results? in|resulted in|leads? to|drives?|attributable to)\b", re.I)
RE_CATEGORICAL = re.compile(r"\b(all|every|no one|none|never|always|without exception|universally)\b", re.I)
RE_HEDGE = re.compile(r"\b(may|might|could|appears?|suggests?|approximately|roughly|about|estimated|likely|potentially)\b", re.I)
RE_FIRSTPERSON = re.compile(r"\b(we|we've|our|ours|my|mine|us|I)\b", re.I)
RE_RECOMMEND = re.compile(r"\b(should|must|recommend\w*|propose\w*|we will|plan to|intend to)\b", re.I)
RE_CITATION = re.compile(
    r"\((?:[A-Z][A-Za-z\-']+(?:\s(?:et al\.?|and|&)\s[A-Z][A-Za-z\-']+)?,?\s*\d{4}[a-z]?)\)"
    r"|\[\d{1,3}\]"
    # Narrative style: "According to Whitfield and Barnes (2021),"
    r"|(?:[A-Z][A-Za-z\-']+(?:\s(?:et al\.?|and|&)\s[A-Z][A-Za-z\-']+)*)\s\((?:19|20)\d{2}[a-z]?\)"
)
# Proper nouns near a citation, for resolution against source text.
RE_CITE_NAME = re.compile(r"[A-Z][A-Za-z\-']{2,}")


def classify(sentence):
    """Return (claim_class, signals). See PROOF_PROTOCOL.md §3."""
    signals = []
    if RE_QUOTE.search(sentence):
        signals.append("quotation")
    if RE_PERCENT.search(sentence):
        signals.append("percentage")
    if RE_CURRENCY.search(sentence):
        signals.append("currency")
    if RE_ISO_DATE.search(sentence) or RE_YEAR.search(sentence):
        signals.append("date")
    if RE_NUMBER.search(sentence):
        signals.append("numeral")
    if RE_ATTRIB.search(sentence):
        signals.append("attribution")
    if RE_SUPERLATIVE.search(sentence):
        signals.append("superlative")
    if RE_COMPARATIVE.search(sentence):
        signals.append("comparative")
    if RE_CAUSAL.search(sentence):
        signals.append("causal")
    if RE_CATEGORICAL.search(sentence):
        signals.append("categorical")
    if RE_CITATION.search(sentence):
        signals.append("citation")
    if RE_HEDGE.search(sentence):
        signals.append("hedged")

    if not signals or signals == ["hedged"]:
        return "rhetoric", signals

    if RE_RECOMMEND.search(sentence) and "attribution" not in signals:
        return "recommendation", signals

    # First person plus a checkable figure is usually the author's own record,
    # not an external fact. Misclassifying this as unsupported is insulting.
    if RE_FIRSTPERSON.search(sentence) and "attribution" not in signals \
       and "citation" not in signals:
        return "observed_fact", signals

    if RE_CAUSAL.search(sentence) and not ("attribution" in signals or "citation" in signals):
        return "inference", signals

    return "sourced_fact", signals


def extract_claims(doc_path):
    text = read_text(doc_path)
    tier, tier_note = script_profile(text)
    claims = []
    offset = 0
    for idx, sent in enumerate(sentences(text)):
        pos = text.find(sent, offset)
        if pos < 0:
            pos = offset
        offset = pos + len(sent)
        cls, signals = classify(sent)
        if cls == "rhetoric":
            continue
        claims.append({
            "id": "c%04d" % (len(claims) + 1),
            "text": sent,
            "class": cls,
            "signals": signals,
            "offset": pos,
            "status": "unverified",
            "spans": [],
            "notes": [],
        })
    return {
        "wi_version": VERSION,
        "document": str(doc_path),
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "script_tier": tier,
        "script_note": tier_note,
        "sentence_count": len(sentences(text)),
        "claims": claims,
    }


# --------------------------------------------------------------------------
# Verification: span lock, quotation, numeric, date, citation resolution.
# --------------------------------------------------------------------------

def find_verbatim(needle, sources):
    """Locate `needle` verbatim in any source. Whitespace-folded comparison.
    Returns (source_id, char_offset) or (None, None)."""
    target = fold_ws(nfc(needle))
    if len(target) < 8:
        return None, None
    for src in sources:
        if not src.get("text"):
            continue
        hay = fold_ws(src["text"])
        pos = hay.find(target)
        if pos >= 0:
            return src["id"], pos
    return None, None


def numbers_in(text):
    """Canonical numeric values found in text, for comparison."""
    vals = set()
    for m in RE_NUMBER.finditer(text):
        raw = m.group(0).strip()
        pct = raw.endswith("%")
        cleaned = raw.rstrip("%").strip().replace(",", "").replace("_", "")
        # Trailing dot from sentence punctuation.
        cleaned = cleaned.rstrip(".")
        if not cleaned:
            continue
        try:
            v = float(cleaned)
        except ValueError:
            continue
        vals.add(round(v / 100.0, 6) if pct else round(v, 6))
    return vals


def years_in(text):
    return {int(y) for y in RE_YEAR.findall(text)}


def verify(ledger, sources, tolerance=0.0):
    """Run all deterministic checks. Mutates and returns the ledger."""
    readable = [s for s in sources if s.get("text")]
    ledger["sources"] = [{"id": s["id"], "title": s["title"],
                          "readable": bool(s.get("text")),
                          "note": s.get("note")} for s in sources]
    ledger["sources_readable"] = len(readable)

    for claim in ledger["claims"]:
        claim["notes"] = []
        claim["spans"] = []
        text = claim["text"]

        if not readable:
            claim["status"] = "needs_source"
            claim["notes"].append("no readable sources supplied; not verified")
            continue

        # 1. Quotation check — misquotation is the most common serious error.
        quote_ok = None
        for qm in RE_QUOTE.finditer(text):
            quoted = qm.group(1)
            sid, pos = find_verbatim(quoted, readable)
            if sid:
                claim["spans"].append({"source": sid, "offset": pos,
                                       "text": fold_ws(quoted), "kind": "quotation"})
                quote_ok = True if quote_ok is not False else False
            else:
                claim["notes"].append(
                    "quoted text not found verbatim in any source: %s" % _trunc(quoted))
                quote_ok = False

        # 2. Span lock — is the assertion itself present verbatim anywhere?
        sid, pos = find_verbatim(text, readable)
        if sid:
            claim["spans"].append({"source": sid, "offset": pos,
                                   "text": fold_ws(text), "kind": "exact"})

        # 3. Citation resolution — the fabrication check.
        if "citation" in claim["signals"]:
            cites = [m.group(0) for m in RE_CITATION.finditer(text)]
            resolved = False
            corpus = " ".join(fold_ws(s["text"]).lower() for s in readable)
            for c in cites:
                names = [n for n in RE_CITE_NAME.findall(c)
                         if n.lower() not in {"et", "al", "and"}]
                if not names:
                    # Bare [12] style: cannot resolve without a bibliography.
                    continue
                if all(n.lower() in corpus for n in names):
                    resolved = True
            if cites and not resolved:
                claim["notes"].append(
                    "citation does not resolve to any supplied source")
                claim["status"] = "unsafe"
                continue

        # 4. Numeric agreement. Report only the values actually missing —
        #    listing every number in the sentence buries the real finding.
        claim_years = years_in(text)
        claim_nums = {n for n in numbers_in(text)
                      if not (n.is_integer() and int(n) in claim_years)}
        if claim_nums:
            missing_nums = _missing_numbers(claim_nums, readable, tolerance)
            if missing_nums:
                claim["notes"].append(
                    "figure(s) not found in any source: %s"
                    % ", ".join(_fmt(n) for n in sorted(missing_nums)))

        # 5. Date agreement.
        if claim_years:
            src_years = set()
            for src in readable:
                src_years |= years_in(src["text"])
            missing = claim_years - src_years
            if missing:
                claim["notes"].append(
                    "year(s) not present in any source: %s"
                    % ", ".join(str(y) for y in sorted(missing)))

        # 6. Status decision. Under-claim (Law E).
        if claim["status"] == "unsafe":
            continue
        if quote_ok is False:
            claim["status"] = "conflicted"
        elif any(s["kind"] == "quotation" for s in claim["spans"]):
            claim["status"] = "quote_verified"
        elif claim["class"] == "observed_fact":
            claim["status"] = "author_asserted"
        elif claim["class"] == "inference":
            claim["status"] = "inference"
        elif claim["class"] == "recommendation":
            claim["status"] = "recommendation"
        elif claim["spans"]:
            # An exact verbatim match of the whole sentence is support, but the
            # deterministic tier cannot judge paraphrase. That is E1/E2 work.
            claim["status"] = "supported"
        else:
            claim["status"] = "needs_source"
            if not claim["notes"]:
                claim["notes"].append(
                    "no verbatim span found; deterministic tier cannot confirm paraphrased support")

    ledger["verified_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    ledger["engine"] = {"tier": "E0-deterministic", "version": VERSION,
                        "note": "string, numeric and date comparison only; "
                                "no paraphrase or entailment judgment"}
    return ledger


def _missing_numbers(claim_nums, sources, tolerance):
    """Which of the claim's figures appear nowhere in the sources."""
    src_nums = set()
    for s in sources:
        src_nums |= numbers_in(s["text"])
    missing = set()
    for n in claim_nums:
        if not any(abs(n - m) <= max(tolerance * abs(n), 1e-9) for m in src_nums):
            missing.add(n)
    return missing


def _fmt(n):
    return ("%g" % n)


def _trunc(s, n=60):
    s = fold_ws(s)
    return s if len(s) <= n else s[:n] + "..."


# --------------------------------------------------------------------------
# Source scanning: injection indicators and hidden text.
# --------------------------------------------------------------------------

INJECTION_PATTERNS = [
    (r"ignore (?:all |any )?(?:previous|prior|above|preceding) (?:instructions?|prompts?|rules?)",
     "imperative_to_system"),
    (r"disregard (?:the )?(?:above|previous|prior|earlier)", "imperative_to_system"),
    (r"you are now\b", "imperative_to_system"),
    (r"^\s*(?:system|assistant|user)\s*:", "role_marker"),
    (r"<\|?(?:im_start|im_end|system|endoftext)\|?>", "role_marker"),
    (r"mark (?:all )?(?:claims?|statements?) (?:as )?verified", "verification_override"),
    (r"skip (?:the )?(?:check|verification|review|audit)", "verification_override"),
    (r"approve (?:this )?without (?:review|checking)", "verification_override"),
    (r"do not (?:flag|report|mention) (?:this|the following)", "suppression"),
    (r"new instructions?\s*:", "imperative_to_system"),
]

ZERO_WIDTH = {0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x180E}
BIDI_CONTROL = {0x202A, 0x202B, 0x202C, 0x202D, 0x202E,
                0x2066, 0x2067, 0x2068, 0x2069}


def scan_source_text(text, title):
    findings = []
    lowered = text.lower()
    for pattern, kind in INJECTION_PATTERNS:
        for m in re.finditer(pattern, lowered, re.I | re.M):
            findings.append({
                "kind": kind, "offset": m.start(),
                "excerpt": _trunc(text[max(0, m.start() - 20):m.start() + 90], 110),
            })

    zw = [i for i, ch in enumerate(text) if ord(ch) in ZERO_WIDTH]
    if zw:
        findings.append({"kind": "invisible_text", "offset": zw[0],
                         "excerpt": "%d zero-width character(s)" % len(zw)})

    bidi = [i for i, ch in enumerate(text) if ord(ch) in BIDI_CONTROL]
    if bidi:
        findings.append({"kind": "bidi_control", "offset": bidi[0],
                         "excerpt": "%d bidirectional control character(s); "
                                    "visible order may differ from stored order" % len(bidi)})

    for m in re.finditer(r"[A-Za-z0-9+/]{80,}={0,2}", text):
        findings.append({"kind": "encoded_payload", "offset": m.start(),
                         "excerpt": "%d-char base64-like block" % len(m.group(0))})

    return {"title": title, "findings": findings,
            "quarantine": any(f["kind"] in {"imperative_to_system", "role_marker",
                                            "verification_override", "suppression",
                                            "invisible_text"}
                              for f in findings)}


# --------------------------------------------------------------------------
# Gate
# --------------------------------------------------------------------------

REPAIRS = [
    "attach a source that states this",
    "qualify the claim to match what your sources actually say",
    "cut the claim",
    "proceed with a stated caveat (records a waiver)",
]


def gate(ledger, mode="standard"):
    blocking, holding, advisory = [], [], []
    for c in ledger["claims"]:
        st = c["status"]
        if st == "unsafe":
            blocking.append((c, "citation does not resolve to a supplied source"))
        elif st == "conflicted":
            (blocking if mode == "regulated" else holding).append(
                (c, "source conflict or misquotation"))
        elif st == "stale":
            if mode in ("strict", "regulated"):
                holding.append((c, "verified earlier; the sentence changed since"))
        elif st == "needs_source":
            if mode in ("strict", "regulated"):
                holding.append((c, "no verbatim support found"))
            elif mode == "standard":
                advisory.append((c, "no verbatim support found"))

    if blocking:
        decision = "BLOCK"
    elif holding:
        decision = "HOLD"
    else:
        decision = "RELEASE"

    return {"decision": decision, "mode": mode,
            "blocking": blocking, "holding": holding, "advisory": advisory}


def render_gate(result, ledger):
    L = []
    counts = {}
    for c in ledger["claims"]:
        counts[c["status"]] = counts.get(c["status"], 0) + 1

    L.append("# Release gate: %s" % result["decision"])
    L.append("")
    L.append("Evidence mode: `%s` · %d claims · %d readable source(s)"
             % (result["mode"], len(ledger["claims"]), ledger.get("sources_readable", 0)))
    L.append("")
    L.append("Checks run: quotation · numeric · date · citation resolution · verbatim span.")
    L.append("Not run: paraphrase support (needs a judgment tier, not this script).")
    L.append("")
    if counts:
        L.append("| Status | Count |")
        L.append("|---|---|")
        for k in sorted(counts):
            L.append("| `%s` | %d |" % (k, counts[k]))
        L.append("")

    def section(title, items, note):
        if not items:
            return
        L.append("## %s (%d)" % (title, len(items)))
        L.append("")
        L.append(note)
        L.append("")
        for c, reason in items:
            L.append("**%s** — %s" % (c["id"], reason))
            L.append("")
            L.append("> %s" % _trunc(c["text"], 300))
            L.append("")
            for n in c["notes"]:
                L.append("- %s" % n)
            L.append("- Repairs: " + " · ".join(REPAIRS))
            L.append("")

    section("Blocking", result["blocking"],
            "These do not survive a hostile reader. Resolve before sending.")
    section("Holding", result["holding"],
            "You can proceed; you are choosing to, with these outstanding.")
    section("Advisory", result["advisory"],
            "Flagged, not blocking at this evidence mode.")

    if result["decision"] == "RELEASE":
        L.append("Nothing outstanding at this evidence mode.")
        L.append("")
        L.append("This means every claim is supported *within the sources you supplied*, ")
        L.append("marked as your own assertion, or classified as reasoning rather than fact. ")
        L.append("It does not mean the sources are correct.")
    return "\n".join(L)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def cmd_preserve(args):
    src = Path(args.path)
    if not src.exists():
        print("error: %s not found" % src, file=sys.stderr)
        return 2
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    dst = src.with_suffix(src.suffix + ".original-%s" % stamp)
    dst.write_bytes(src.read_bytes())
    print("preserved: %s" % dst)
    return 0


def cmd_scan_sources(args):
    sources = load_sources(args.paths)
    reports, quarantined = [], 0
    for s in sources:
        if not s.get("text"):
            reports.append({"title": s["title"], "findings": [],
                            "quarantine": False, "note": s.get("note")})
            continue
        r = scan_source_text(s["text"], s["title"])
        if r["quarantine"]:
            quarantined += 1
        reports.append(r)

    if args.json:
        print(json.dumps({"wi_version": VERSION, "reports": reports}, indent=2))
        return 0

    print("Scanned %d source(s). %d flagged for review.\n" % (len(reports), quarantined))
    for r in reports:
        if r.get("note"):
            print("  %s — %s" % (r["title"], r["note"]))
            continue
        if not r["findings"]:
            print("  %s — clean" % r["title"])
            continue
        print("  %s — %d finding(s)%s"
              % (r["title"], len(r["findings"]),
                 "  [QUARANTINE]" if r["quarantine"] else ""))
        for f in r["findings"]:
            print("      %-22s @%-8d %s" % (f["kind"], f["offset"], f["excerpt"]))
    print("\nNote: this scan reads extracted text. It cannot detect white-on-white")
    print("or off-page text in a PDF that was flattened before extraction.")
    return 0


def cmd_extract(args):
    ledger = extract_claims(args.document)
    out = args.out or str(Path(args.document).with_suffix(".claims.json"))
    Path(out).write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
    by_class = {}
    for c in ledger["claims"]:
        by_class[c["class"]] = by_class.get(c["class"], 0) + 1
    print("%d claim(s) from %d sentence(s) -> %s"
          % (len(ledger["claims"]), ledger["sentence_count"], out))
    for k in sorted(by_class):
        print("  %-16s %d" % (k, by_class[k]))
    print("script tier: %s (%s)" % (ledger["script_tier"], ledger["script_note"]))
    return 0


def cmd_verify(args):
    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    sources = load_sources(args.sources)
    ledger = verify(ledger, sources, tolerance=args.tolerance)
    out = args.out or args.ledger
    Path(out).write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
    counts = {}
    for c in ledger["claims"]:
        counts[c["status"]] = counts.get(c["status"], 0) + 1
    print("verified %d claim(s) against %d readable source(s) -> %s"
          % (len(ledger["claims"]), ledger["sources_readable"], out))
    for k in sorted(counts):
        print("  %-18s %d" % (k, counts[k]))
    return 0


def cmd_gate(args):
    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    result = gate(ledger, mode=args.mode)
    report = render_gate(result, ledger)
    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        print("gate: %s -> %s" % (result["decision"], args.out))
    else:
        print(report)
    if args.exit_code:
        return {"RELEASE": 0, "HOLD": 1, "BLOCK": 2}[result["decision"]]
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="wi", description="Writing Intelligence v4 deterministic checks")
    p.add_argument("--version", action="version", version="wi %s" % VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("preserve", help="snapshot a file before editing (Law B)")
    sp.add_argument("path")
    sp.set_defaults(func=cmd_preserve)

    sp = sub.add_parser("scan-sources", help="flag injection indicators and hidden text")
    sp.add_argument("paths", nargs="+")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_scan_sources)

    sp = sub.add_parser("extract-claims", help="build a claim ledger from a document")
    sp.add_argument("document")
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_extract)

    sp = sub.add_parser("verify", help="span lock, quotation, numeric and date checks")
    sp.add_argument("ledger")
    sp.add_argument("sources", nargs="+")
    sp.add_argument("--out")
    sp.add_argument("--tolerance", type=float, default=0.0,
                    help="relative numeric tolerance, e.g. 0.01 for 1%%")
    sp.set_defaults(func=cmd_verify)

    sp = sub.add_parser("gate", help="emit RELEASE / HOLD / BLOCK with repairs")
    sp.add_argument("ledger")
    sp.add_argument("--mode", default="standard",
                    choices=["light", "standard", "strict", "regulated"])
    sp.add_argument("--out")
    sp.add_argument("--exit-code", action="store_true",
                    help="exit 0/1/2 for RELEASE/HOLD/BLOCK (for CI and git hooks)")
    sp.set_defaults(func=cmd_gate)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
