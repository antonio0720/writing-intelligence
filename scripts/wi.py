#!/usr/bin/env python3
"""
wi.py — Writing Intelligence v5, the Proof-Carrying Authorship core.

Every check here is deterministic, offline, dependency-free, and language-
independent where it can be. It compares bytes, strings, numbers and dates.
It never judges prose quality and it never calls a model.

Stdlib only, Python 3.8+. Runs air-gapped. One file — copy it anywhere.

v4 floor (unchanged)
--------------------
  preserve         Snapshot a file before editing (Law B).
  scan-sources     Flag injection indicators and hidden text (Law F).
  extract-claims   Sentence-level claim ledger.
  verify           Span lock + quotation + numeric + date checks (Law D).
  gate             Emit RELEASE / HOLD / BLOCK with repairs.

v5 — meaning, dependency, proof
-------------------------------
  init             Create a .wi workspace: SQLite index + object store.
  ingest           Content-address sources; immutable versions.
  atomize          Split sentences into independently checkable claim atoms.
  anchor           Bind atoms to evidence anchors and run the check set.
  graph            Show the authorship graph.
  impact           What a changed source breaks, and what it provably does not.
  diff --semantic  Classify what a rewrite did to meaning.
  test             Run writing tests and concept-registry contracts.
  explain          Why is this sentence here, and what depends on it.
  bundle           Build a .wiab proof-carrying release bundle.
  verify-release   Verify a bundle offline, with no model.
  doctor           Capability report — what this surface can and cannot do.

Exit codes (with --exit-code on `gate`): 0 RELEASE, 1 HOLD, 2 BLOCK.
`test` exits 1 on any failing writing test. `verify-release` exits 2 on tamper.
"""

import argparse
import datetime as _dt
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

VERSION = "5.0.0"

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


# ==========================================================================
# v5 — Proof-Carrying Authorship
#
# Everything above this line is the v4 deterministic floor and is unchanged.
# Everything below turns those checks into a dependency system: content
# addressing, claim atoms, evidence anchors, a persistent authorship graph,
# staleness propagation, deterministic semantic diff, writing tests, and
# proof-carrying release bundles.
#
# Still stdlib only. Still offline. sqlite3 and zipfile ship with Python.
# ==========================================================================

import hashlib
import sqlite3
import zipfile
import difflib
import fnmatch
import uuid as _uuid

SCHEMA_VERSION = "5.0.0"
NORMALIZATION = "nfc-1"
CANONICALIZATION = "wi-json-v1"
WIAB_FORMAT = "wi-release-manifest"

WI_DIR = ".wi"
PROJECT_FILE = "wi.project.yaml"


# --------------------------------------------------------------------------
# Errors. Stable codes, and every one carries a route forward (Law C).
# --------------------------------------------------------------------------

class WIError(Exception):
    def __init__(self, code, message, repair=None, details=None):
        Exception.__init__(self, message)
        self.code = code
        self.message = message
        self.repair = repair or []
        self.details = details or {}

    def envelope(self):
        return {"error": {"code": self.code, "message": self.message,
                          "basis": "verified", "repair": self.repair,
                          "details": self.details}}

    def render(self):
        L = ["%s: %s" % (self.code, self.message)]
        for k, v in sorted(self.details.items()):
            L.append("    %s: %s" % (k, v))
        if self.repair:
            L.append("  repair:")
            for r in self.repair:
                L.append("    - %s" % r)
        return "\n".join(L)


# --------------------------------------------------------------------------
# Canonical serialization and domain-separated hashing.
#
# The whole staleness and attestation system rests on this being boring and
# exact: the same state must always produce the same digest, on every machine,
# in every Python version we support.
# --------------------------------------------------------------------------

def _nfc_deep(obj):
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {_nfc_deep(k): _nfc_deep(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_nfc_deep(v) for v in obj]
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            raise WIError("WI_INPUT_INVALID",
                          "NaN and infinities cannot be canonically serialized",
                          ["replace the value with a decimal string"])
    return obj


def canonical_bytes(obj):
    """RFC 8785-shaped canonical JSON: NFC strings, sorted keys, no spaces."""
    return json.dumps(_nfc_deep(obj), sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def content_digest(obj):
    """Digest of the canonical payload alone."""
    return "sha256:" + sha256_hex(canonical_bytes(obj))


def state_digest(obj, schema):
    """Digest that additionally binds schema and normalization version.

    Domain separated on purpose: the same raw digest must never ambiguously
    represent a source byte stream and a semantic object.
    """
    pre = (b"wi-state-v5\x00"
           + ("schema=%s@%s\x00" % (schema, SCHEMA_VERSION)).encode("utf-8")
           + ("normalization=%s\x00" % NORMALIZATION).encode("utf-8")
           + b"payload=" + canonical_bytes(obj))
    return "sha256:" + sha256_hex(pre)


def blob_digest(raw_bytes):
    """Source identity. Raw bytes, never normalized first."""
    return "sha256:" + sha256_hex(raw_bytes)


def logical_id(kind, *parts):
    """Content-derived logical identity, UUID-shaped and reproducible.

    Random ids would make every build produce a different graph, which would
    make `wi bundle` non-reproducible and the published checksum meaningless.
    The identity is derived from what makes the node *the same node* across
    versions — for a claim atom, its proposition skeleton, not its wording.
    That is Law G in one function.
    """
    key = ("wi5:%s:" % kind) + "\x00".join(str(p) for p in parts)
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return str(_uuid.UUID(bytes=h[:16], version=5))


def digest_record(digest):
    return {"digest_algorithm": "sha256", "canonicalization": CANONICALIZATION,
            "digest": digest}


# --------------------------------------------------------------------------
# Minimal YAML reader.
#
# A dependency-free tool cannot import PyYAML, and the config surface we
# actually use is small: nested maps, lists, scalars, comments. Anything this
# parser does not understand is reported, never guessed.
# --------------------------------------------------------------------------

def _yaml_scalar(tok):
    tok = tok.strip()
    if not tok:
        return None
    if tok == "{}":
        return {}
    if tok == "[]":
        return []
    if tok[0] in "{[":
        raise WIError("WI_INPUT_INVALID",
                      "flow-style YAML is not supported here: %s" % tok[:40],
                      ["rewrite it as an indented block",
                       "use {} or [] for an empty collection"])
    if tok[0] in "\"'" and tok[-1] == tok[0] and len(tok) >= 2:
        return tok[1:-1]
    low = tok.lower()
    if low in ("true", "yes", "on"):
        return True
    if low in ("false", "no", "off"):
        return False
    if low in ("null", "~", "none"):
        return None
    try:
        return int(tok)
    except ValueError:
        pass
    try:
        return float(tok)
    except ValueError:
        pass
    return tok


def _yaml_strip(line):
    out, quote = [], None
    for ch in line:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def parse_yaml(text):
    """Parse the YAML subset this project uses. Returns dict/list/scalar."""
    lines = []
    for raw in nfc(text).splitlines():
        if "\t" in raw.split("#")[0]:
            raise WIError("WI_INPUT_INVALID", "tab indentation is not valid YAML",
                          ["replace tabs with spaces"])
        stripped = _yaml_strip(raw)
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        lines.append((indent, stripped.strip()))

    def block(i, indent):
        if i >= len(lines):
            return None, i
        if lines[i][1].startswith("- "):
            items = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                body = lines[i][1][2:].strip()
                if ":" in body and not body.startswith(("\"", "'")):
                    k, _, v = body.partition(":")
                    item = {}
                    if v.strip():
                        item[k.strip()] = _yaml_scalar(v)
                    i += 1
                    child_indent = indent + 2
                    while i < len(lines) and lines[i][0] >= child_indent:
                        sub, i = block(i, lines[i][0])
                        if isinstance(sub, dict):
                            item.update(sub)
                        else:
                            break
                    items.append(item)
                    continue
                items.append(_yaml_scalar(body))
                i += 1
            return items, i
        out = {}
        while i < len(lines) and lines[i][0] == indent:
            line = lines[i][1]
            if line.startswith("- "):
                break
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            i += 1
            if val:
                out[key] = _yaml_scalar(val)
                continue
            if i < len(lines) and lines[i][0] > indent:
                child, i = block(i, lines[i][0])
                out[key] = child
            else:
                out[key] = None
        return out, i

    result, _ = block(0, lines[0][0]) if lines else ({}, 0)
    return result if result is not None else {}


def load_yaml_file(path):
    p = Path(path)
    if not p.exists():
        raise WIError("WI_INPUT_INVALID", "%s not found" % p,
                      ["run `wi init` to create one"])
    return parse_yaml(p.read_text(encoding="utf-8", errors="replace"))


# --------------------------------------------------------------------------
# Claim atomization.
#
# The canonical verification unit in v5 is the claim atom, not the sentence.
# A compound sentence can be partially supported, because its independently
# checkable parts are independent objects with their own proof state.
# --------------------------------------------------------------------------

RE_UNIT = re.compile(
    r"(?P<num>\d[\d,._]*\.?\d*)\s?(?P<pct>%|percent|per cent|pct)?\s*"
    r"(?P<unit>[a-z][a-z\-]{2,24}(?:s)?)?", re.I)
RE_RANGE = re.compile(
    r"\b(?:between|from)\s+((?:19|20)\d{2})\s+(?:and|to|through|-|–)\s+((?:19|20)\d{2})\b", re.I)
RE_SINCE = re.compile(r"\bsince\s+((?:19|20)\d{2})\b", re.I)
RE_IN_YEAR = re.compile(r"\b(?:in|during|by)\s+((?:19|20)\d{2})\b", re.I)
RE_MODAL_MAY = re.compile(r"\b(may|might|could|can)\b", re.I)
RE_MODAL_MUST = re.compile(r"\b(must|shall|is required to|are required to|required)\b", re.I)
RE_MODAL_SHOULD = re.compile(r"\b(should|ought to|recommended|recommends?)\b", re.I)
RE_MODAL_WILL = re.compile(r"\b(will|shall be|is going to)\b", re.I)
RE_NEGATION = re.compile(r"\b(not|no|never|neither|nor|without|fails? to)\b", re.I)
RE_ATTRIB_NAME = re.compile(
    r"\b(?:according to|as reported by|per the|cited in)\s+([A-Z][\w\-'.]*(?:\s+(?:and|&|et al\.?)\s+[A-Z][\w\-'.]*)?(?:\s+[A-Z][\w\-'.]*)*)")
RE_ENTITY = re.compile(r"\b([A-Z][a-z\-']{2,}(?:\s+[A-Z][a-z\-']{2,})*)\b")

# Where a compound sentence may be cut. Each side must still carry a
# checkable signal, or the split is discarded — over-splitting produces
# atoms nothing can support and teaches people to ignore the ledger.
RE_SPLIT = re.compile(
    r"(?:,\s+and\s+|;\s+and\s+|;\s+|\s+and\s+(?=(?:the|it|they|we|this|that|median|average|total)\b)"
    r"|,\s+while\s+|,\s+whereas\s+|,\s+but\s+)", re.I)

STOP_ENTITIES = {"The", "This", "That", "These", "Those", "It", "They", "We",
                 "Between", "From", "According", "During", "In", "By", "A", "An"}


def _units_of(text):
    """(value, unit) pairs. Percentages normalize to their fractional value."""
    out = []
    for m in RE_UNIT.finditer(text):
        raw = m.group("num").replace(",", "").replace("_", "").rstrip(".")
        if not raw:
            continue
        try:
            val = float(raw)
        except ValueError:
            continue
        if m.group("pct"):
            out.append({"value": round(val / 100.0, 6), "unit": "ratio",
                        "surface": m.group(0).strip()})
            continue
        unit = (m.group("unit") or "").lower().strip()
        if unit in {"and", "the", "of", "in", "to", "for", "with", "was", "were"}:
            unit = ""
        if 1900 <= val <= 2099 and float(val).is_integer() and not unit:
            continue  # a bare year is temporal scope, not a quantity
        out.append({"value": round(val, 6), "unit": unit or None,
                    "surface": m.group(0).strip()})
    return out


def temporal_scope(text):
    m = RE_RANGE.search(text)
    if m:
        return {"start": m.group(1), "end": m.group(2), "kind": "range"}
    m = RE_SINCE.search(text)
    if m:
        return {"start": m.group(1), "end": None, "kind": "open_range"}
    m = RE_IN_YEAR.search(text)
    if m:
        return {"start": m.group(1), "end": m.group(1), "kind": "point"}
    return None


def modality(text):
    if RE_MODAL_MUST.search(text):
        return "must"
    if RE_MODAL_SHOULD.search(text):
        return "should"
    if RE_MODAL_WILL.search(text):
        return "will"
    if RE_MODAL_MAY.search(text):
        return "may"
    return "is"


def entities_in(text):
    """Proper-noun phrases, minus the obvious false positives.

    A single capitalized word at the start of a sentence is capitalization, not
    an entity. Treating it as one produces `entity.presence` failures that teach
    people to ignore the check, which is worse than not running it.
    """
    found = []
    for m in RE_ENTITY.finditer(text):
        name = m.group(1)
        if name in STOP_ENTITIES or name.split()[0] in STOP_ENTITIES:
            continue
        if m.start() == 0 and " " not in name:
            continue
        if name not in found:
            found.append(name)
    return found


def proposition_of(text):
    """The structured skeleton of an assertion. Deliberately modest.

    v5.0 does not attempt a universal ontology of language. It extracts the
    dimensions that make a *consequential* change mechanically visible.
    """
    attrib = RE_ATTRIB_NAME.search(text)
    return {
        "quantities": _units_of(text),
        "temporal_scope": temporal_scope(text),
        "modality": modality(text),
        "negated": bool(RE_NEGATION.search(text)),
        "attribution": attrib.group(1).strip() if attrib else None,
        "entities": entities_in(text)[:6],
        "causal": bool(RE_CAUSAL.search(text)),
        "categorical": bool(RE_CATEGORICAL.search(text)),
        "hedged": bool(RE_HEDGE.search(text)),
    }


def proposition_skeleton(prop, fallback):
    """The identity key for a claim atom.

    Two atoms with the same skeleton are the same claim, however differently
    worded. Change the skeleton and you have a different claim, which is
    exactly when the proof must not carry forward.
    """
    q = sorted((x["value"], x["unit"] or "") for x in prop["quantities"])
    ts = prop["temporal_scope"] or {}
    parts = [
        "q=" + ";".join("%s/%s" % (v, u) for v, u in q),
        "t=%s-%s" % (ts.get("start"), ts.get("end")),
        "m=%s" % prop["modality"],
        "n=%s" % int(prop["negated"]),
        "a=%s" % (prop["attribution"] or ""),
        "e=" + ";".join(sorted(prop["entities"])),
    ]
    key = "|".join(parts)
    if key == "q=|t=None-None|m=is|n=0|a=|e=":
        # Nothing structural to key on; fall back to normalized wording so the
        # atom still gets a stable identity rather than colliding with others.
        key = "w=" + fold_ws(fallback).lower()
    return key


def atomize_sentence(sentence):
    """Split one sentence into independently checkable atoms."""
    pieces, cursor = [], 0
    for m in RE_SPLIT.finditer(sentence):
        chunk = sentence[cursor:m.start()].strip()
        if chunk:
            pieces.append((chunk, cursor))
        cursor = m.end()
    tail = sentence[cursor:].strip()
    if tail:
        pieces.append((tail, cursor))
    if not pieces:
        pieces = [(sentence.strip(), 0)]

    # A split is only kept when every side still carries something checkable.
    def checkable(t):
        return bool(RE_NUMBER.search(t) or RE_QUOTE.search(t)
                    or RE_CITATION.search(t) or RE_YEAR.search(t))

    if len(pieces) > 1 and not all(checkable(t) for t, _ in pieces):
        pieces = [(sentence.strip(), 0)]
    return pieces


def atomize_document(doc_path, project=None):
    """Build the v5 claim ledger: paragraphs, sentences, atoms, propositions."""
    text = read_text(doc_path)
    tier, tier_note = script_profile(text)
    doc_key = str(Path(doc_path).as_posix())

    paragraphs, atoms = [], []
    offset = 0
    for pidx, para in enumerate(re.split(r"\n\s*\n", text)):
        if not para.strip():
            offset += len(para) + 2
            continue
        ppos = text.find(para, offset)
        if ppos < 0:
            ppos = offset
        offset = ppos + len(para)
        para_id = logical_id("paragraph", doc_key, fold_ws(para)[:96])
        para_rec = {
            "logical_id": para_id,
            "type": "structure.paragraph",
            "document": doc_key,
            "index": pidx,
            "offset": ppos,
            "line": text.count("\n", 0, ppos) + 1,
            "text": para.strip(),
        }
        para_rec["state_digest"] = state_digest(
            {"document": doc_key, "text": fold_ws(para)}, "structure.paragraph")
        paragraphs.append(para_rec)

        for sent in sentences(para):
            spos = text.find(sent, ppos)
            if spos < 0:
                spos = ppos
            for chunk, rel in atomize_sentence(sent):
                cls, signals = classify(chunk)
                if cls == "rhetoric":
                    continue
                prop = proposition_of(chunk)
                skel = proposition_skeleton(prop, chunk)
                aid = logical_id("claim_atom", doc_key, skel)
                payload = {"proposition": prop, "class": cls,
                           "surface": fold_ws(chunk)}
                atoms.append({
                    "logical_id": aid,
                    "id": "a%04d" % (len(atoms) + 1),
                    "type": "meaning.claim_atom",
                    "class": cls,
                    "realm": {"sourced_fact": "external_fact",
                              "inference": "external_fact",
                              "observed_fact": "author_observation"}.get(
                                  cls, "rhetorical"),
                    "text": chunk,
                    "sentence": sent,
                    "signals": signals,
                    "proposition": prop,
                    "skeleton": skel,
                    "paragraph": para_id,
                    "document": doc_key,
                    "offset": spos + rel,
                    "line": text.count("\n", 0, spos) + 1,
                    "status": "unverified",
                    "anchors": [],
                    "checks": [],
                    "notes": [],
                    "state_digest": state_digest(payload, "meaning.claim_atom"),
                })

    ledger = {
        "wi_version": VERSION,
        "schema": "claim_ledger@%s" % SCHEMA_VERSION,
        "document": doc_key,
        "document_digest": blob_digest(Path(doc_path).read_bytes()),
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "script_tier": tier,
        "script_note": tier_note,
        "paragraphs": paragraphs,
        "atoms": atoms,
        "engine": {"tier": "E0-deterministic", "version": VERSION,
                   "note": "structural extraction only; no paraphrase judgment"},
    }
    if project:
        ledger["project"] = project.get("project", {}).get("id")
    return ledger


# --------------------------------------------------------------------------
# Evidence anchors.
#
# The v4 span lock, generalized. v5.0 ships the text_span anchor as executable.
# The other anchor types are specified in references/v5/EVIDENCE_ANCHORS.md and
# are reported unavailable rather than faked.
# --------------------------------------------------------------------------

SUPPORTED_ANCHOR_TYPES = ["text_span"]


def _byte_span(text, char_start, char_end):
    return (len(text[:char_start].encode("utf-8")),
            len(text[:char_end].encode("utf-8")))


def _locate(needle, hay):
    """Whitespace-tolerant search. Returns (char_start, char_end) or None."""
    target = fold_ws(needle)
    if len(target) < 8:
        return None
    direct = hay.find(needle)
    if direct >= 0:
        return direct, direct + len(needle)
    # Fold the haystack while keeping a map back to original offsets.
    folded, index = [], []
    prev_space = True
    for i, ch in enumerate(hay):
        if ch.isspace():
            if prev_space:
                continue
            folded.append(" ")
            index.append(i)
            prev_space = True
        else:
            folded.append(ch)
            index.append(i)
            prev_space = False
    fh = "".join(folded).strip()
    shift = len("".join(folded)) - len("".join(folded).lstrip())
    pos = fh.find(target)
    if pos < 0:
        return None
    start = index[pos + shift]
    end_i = min(pos + shift + len(target) - 1, len(index) - 1)
    return start, index[end_i] + 1


def make_anchor(source, char_start, char_end):
    quote = source["text"][char_start:char_end]
    sb, eb = _byte_span(source["text"], char_start, char_end)
    payload = {"source_state_digest": source["state_digest"],
               "start_byte": sb, "end_byte": eb,
               "quote_digest": "sha256:" + sha256_hex(fold_ws(quote).encode("utf-8"))}
    return {
        "anchor_id": logical_id("anchor", source["logical_id"], sb, eb),
        "type": "source.segment",
        "anchor_type": "text_span",
        "source_logical_id": source["logical_id"],
        "source_state_digest": source["state_digest"],
        "source_blob_digest": source.get("blob_digest"),
        "start_byte": sb,
        "end_byte": eb,
        "quote": quote.strip(),
        "quote_digest": payload["quote_digest"],
        "state_digest": state_digest(payload, "evidence.anchor"),
    }


def _source_records(sources):
    """Attach identity to every loaded source.

    Three distinct things get three distinct fields, on purpose:
      artifact_id   the file as a continuing thing ("the outcomes report")
      logical_id    this exact version of it, which is what an anchor binds to
      blob_digest   the raw bytes, hashed before any normalization
    Collapsing any two of these is how a system ends up unable to say
    "the bytes did not change; the extractor did."
    """
    out = []
    for s in sources:
        name = Path(s["id"]).name
        art = logical_id("source", name)
        if not s.get("text"):
            out.append(dict(s, artifact_id=art, logical_id=art,
                            blob_digest=None, state_digest=None, unreadable=True))
            continue
        raw = (Path(s["id"]).read_bytes() if Path(s["id"]).exists()
               else s["text"].encode("utf-8"))
        bd = blob_digest(raw)
        out.append(dict(s, artifact_id=art,
                        logical_id=logical_id("source_version", name, bd),
                        blob_digest=bd,
                        state_digest=state_digest(
                            {"artifact": art, "blob_digest": bd,
                             "byte_length": len(raw)}, "source.version"),
                        byte_length=len(raw)))
    return out


def anchor_and_check(ledger, sources, tolerance=0.0):
    """Bind atoms to evidence anchors and run the deterministic check set.

    Every atom ends with an explicit list of checks that ran and checks that
    did not. An unavailable check is never silently omitted (Law C).
    """
    srcs = _source_records(sources)
    readable = [s for s in srcs if s.get("text")]
    corpus = " ".join(fold_ws(s["text"]).lower() for s in readable)
    src_nums, src_years = set(), set()
    for s in readable:
        src_nums |= numbers_in(s["text"])
        src_years |= years_in(s["text"])

    ledger["sources"] = [{"logical_id": s["logical_id"],
                          "artifact_id": s["artifact_id"], "path": s["id"],
                          "title": s["title"], "readable": bool(s.get("text")),
                          "blob_digest": s.get("blob_digest"),
                          "state_digest": s.get("state_digest"),
                          "byte_length": s.get("byte_length"),
                          "note": s.get("note")} for s in srcs]
    ledger["sources_readable"] = len(readable)
    ledger["anchors"] = []
    ledger["checks_not_run"] = [
        "paraphrase entailment (judgment tier; no provider configured)",
        "pdf_region / sheet_range / audio_time / video_time / image_region anchors "
        "(specified, not executable in this build)",
    ]

    seen_anchor = {}

    for atom in ledger["atoms"]:
        atom["anchors"], atom["checks"], atom["notes"] = [], [], []
        text = atom["text"]

        def record(check, result, basis="verified", detail=None):
            entry = {"check": check, "result": result, "basis": basis}
            if detail:
                entry["detail"] = detail
            atom["checks"].append(entry)
            return entry

        if not readable:
            atom["status"] = "needs_source"
            record("anchor.integrity", "unavailable", "verified",
                   "no readable sources supplied")
            atom["notes"].append("no readable sources supplied; not verified")
            continue

        # 1. Quotation. Misquotation is the most common serious error, and it
        #    is the one a reader can check fastest.
        quote_state = None
        for qm in RE_QUOTE.finditer(text):
            quoted = qm.group(1)
            hit = None
            for s in readable:
                loc = _locate(quoted, s["text"])
                if loc:
                    hit = (s, loc)
                    break
            if hit:
                s, (cs, ce) = hit
                a = make_anchor(s, cs, ce)
                seen_anchor[a["anchor_id"]] = a
                atom["anchors"].append(a["anchor_id"])
                record("quote.verbatim", "pass")
                quote_state = True if quote_state is not False else False
            else:
                record("quote.verbatim", "fail", "verified", _trunc(quoted))
                atom["notes"].append(
                    "quoted text not found verbatim in any source: %s" % _trunc(quoted))
                quote_state = False

        # 2. Span lock on the assertion itself, then the located span it lives in.
        #
        #    There is a real and useful distinction between "these figures exist
        #    somewhere in the corpus" and "these figures, dates and entities all
        #    appear together in this one sentence of this one source." The second
        #    is a deterministic result, not a guess, and v4 threw it away.
        exact = None
        for s in readable:
            loc = _locate(text, s["text"])
            if loc:
                exact = (s, loc)
                break
        span_text = None
        if exact:
            s, (cs, ce) = exact
            a = make_anchor(s, cs, ce)
            seen_anchor[a["anchor_id"]] = a
            atom["anchors"].append(a["anchor_id"])
            span_text = a["quote"]
            record("anchor.integrity", "pass", "verified", "verbatim span")
        else:
            cand = _candidate_anchor(atom, readable)
            if cand:
                seen_anchor[cand["anchor_id"]] = cand
                atom["anchors"].append(cand["anchor_id"])
                span_text = cand["quote"]
                record("anchor.integrity", "pass", "verified",
                       "locating span found; wording differs")
            else:
                record("anchor.integrity", "fail", "verified", "no locating span found")

        # 3. Citation resolution — the fabrication check.
        if "citation" in atom["signals"]:
            cites = [m.group(0) for m in RE_CITATION.finditer(text)]
            resolved = False
            for c in cites:
                names = [n for n in RE_CITE_NAME.findall(c)
                         if n.lower() not in {"et", "al", "and"}]
                if names and all(n.lower() in corpus for n in names):
                    resolved = True
            if cites and not resolved:
                record("citation.resolution", "fail")
                atom["notes"].append("citation does not resolve to any supplied source")
                atom["status"] = "unsafe"
                continue
            if cites:
                record("citation.resolution", "pass")

        # 4-6. Component checks, run twice: inside the located span, then across
        #      the whole corpus. Co-location is the stronger, cheaper result.
        span_low = fold_ws(span_text).lower() if span_text else ""
        span_nums = numbers_in(span_text) if span_text else set()
        span_years = years_in(span_text) if span_text else set()

        years = years_in(text)
        nums = {n for n in numbers_in(text) if not (n.is_integer() and int(n) in years)}
        ents = atom["proposition"]["entities"]
        checked, co_located = False, True

        def _missing(vals, pool):
            return {n for n in vals
                    if not any(abs(n - m) <= max(tolerance * abs(n), 1e-9)
                               for m in pool)}

        if nums:
            checked = True
            miss_corpus = _missing(nums, src_nums)
            if miss_corpus:
                co_located = False
                record("numeric.value", "fail", "verified",
                       "not in any source: " + ", ".join(_fmt(n) for n in sorted(miss_corpus)))
                atom["notes"].append("figure(s) not found in any source: %s"
                                     % ", ".join(_fmt(n) for n in sorted(miss_corpus)))
            elif span_text and not _missing(nums, span_nums):
                record("numeric.value", "pass", "verified", "within the anchor span")
            else:
                co_located = False
                record("numeric.value", "pass", "verified",
                       "present in the corpus but not inside the anchor span")

        if years:
            checked = True
            miss_y = years - src_years
            if miss_y:
                co_located = False
                record("date.range", "fail", "verified",
                       ", ".join(str(y) for y in sorted(miss_y)))
                atom["notes"].append("year(s) not present in any source: %s"
                                     % ", ".join(str(y) for y in sorted(miss_y)))
            elif span_text and not (years - span_years):
                record("date.range", "pass", "verified", "within the anchor span")
            else:
                co_located = False
                record("date.range", "pass", "verified",
                       "present in the corpus but not inside the anchor span")

        if ents:
            absent = [e for e in ents if e.lower() not in corpus]
            if absent:
                record("entity.presence", "fail", "verified", ", ".join(absent))
                if atom["class"] == "sourced_fact":
                    co_located = False
            elif span_text and all(e.lower() in span_low for e in ents):
                record("entity.presence", "pass", "verified", "within the anchor span")
            else:
                record("entity.presence", "pass", "verified",
                       "present in the corpus but not inside the anchor span")
                co_located = False

        # 7. Status. Under-claim (Law E): the weakest defensible label wins.
        failed = [c["check"] for c in atom["checks"] if c["result"] == "fail"]
        if atom["status"] == "unsafe":
            continue
        if quote_state is False:
            atom["status"] = "conflicted"
        elif quote_state is True:
            atom["status"] = "quote_verified"
        elif atom["class"] == "observed_fact":
            # The author is the source. Checking their own attested observation
            # against someone else's documents and calling it unsupported is
            # both wrong and insulting; the note stays, the verdict does not.
            atom["status"] = "author_asserted"
        elif atom["class"] == "recommendation":
            atom["status"] = "recommendation"
        elif "numeric.value" in failed or "date.range" in failed:
            atom["status"] = "needs_source"
        elif atom["class"] == "inference":
            atom["status"] = "inference"
        elif exact:
            atom["status"] = "supported"
        elif span_text and checked and co_located:
            atom["status"] = "span_supported"
            atom["notes"].append(
                "every checkable component appears inside one span of one source; "
                "whether that span entails the sentence is a judgment-tier question "
                "and was not evaluated")
        elif atom["anchors"]:
            atom["status"] = "candidate_support"
            atom["notes"].append(
                "components located across the corpus but not inside a single span; "
                "confirming this needs the judgment tier, which is not configured")
        else:
            atom["status"] = "needs_source"
            if not atom["notes"]:
                atom["notes"].append("no locating span found in any supplied source")

    ledger["anchors"] = [seen_anchor[k] for k in sorted(seen_anchor)]
    ledger["anchored_at"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    return ledger


def _candidate_anchor(atom, readable):
    """Locate the source sentence carrying this atom's figures.

    A candidate is retrieval, not proof. It is stored so a human can look at
    the right paragraph in one click, and it is labelled so nothing downstream
    mistakes it for support.
    """
    nums = numbers_in(atom["text"])
    ents = [e.lower() for e in atom["proposition"]["entities"]]
    if not nums and not ents:
        return None
    best = None
    for s in readable:
        for sent in sentences(s["text"]):
            low = sent.lower()
            hit = len(nums & numbers_in(sent)) * 2 + sum(1 for e in ents if e in low)
            if hit and (best is None or hit > best[0]):
                loc = _locate(sent, s["text"])
                if loc:
                    best = (hit, s, loc)
    if not best:
        return None
    _, s, (cs, ce) = best
    return make_anchor(s, cs, ce)


# --------------------------------------------------------------------------
# The workspace: SQLite index plus a content-addressed object store.
# --------------------------------------------------------------------------

DDL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS workspace (
    id TEXT PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL,
    schema_version TEXT NOT NULL, core_version TEXT NOT NULL,
    mode TEXT NOT NULL DEFAULT 'standard');

CREATE TABLE IF NOT EXISTS object_blob (
    digest TEXT PRIMARY KEY, media_type TEXT NOT NULL,
    byte_length INTEGER NOT NULL, storage_path TEXT NOT NULL,
    created_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS node (
    logical_id TEXT PRIMARY KEY, node_type TEXT NOT NULL,
    created_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS node_state (
    state_digest TEXT PRIMARY KEY,
    logical_id TEXT NOT NULL REFERENCES node(logical_id),
    schema_id TEXT NOT NULL, payload_digest TEXT NOT NULL,
    payload_json TEXT NOT NULL, created_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_node_state_logical
    ON node_state(logical_id, created_at);

CREATE TABLE IF NOT EXISTS edge (
    edge_id TEXT PRIMARY KEY,
    from_logical_id TEXT NOT NULL, to_logical_id TEXT NOT NULL,
    relation TEXT NOT NULL, edge_state_digest TEXT NOT NULL,
    payload_json TEXT, created_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_edge_from ON edge(from_logical_id, relation);
CREATE INDEX IF NOT EXISTS idx_edge_to   ON edge(to_logical_id, relation);

CREATE TABLE IF NOT EXISTS current_state (
    logical_id TEXT PRIMARY KEY REFERENCES node(logical_id),
    state_digest TEXT NOT NULL, updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS invalidation (
    invalidation_id TEXT PRIMARY KEY, cause_state_digest TEXT NOT NULL,
    affected_state_digest TEXT NOT NULL, affected_logical_id TEXT NOT NULL,
    reason_code TEXT NOT NULL, created_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_invalidation_affected
    ON invalidation(affected_state_digest);

CREATE TABLE IF NOT EXISTS release_build (
    build_id TEXT PRIMARY KEY, project_state_digest TEXT NOT NULL,
    policy_digest TEXT NOT NULL, core_version TEXT NOT NULL,
    verdict TEXT NOT NULL, created_at TEXT NOT NULL);
"""

# X depends_on Y: a change in Y invalidates X unless provably unaffected.
DEPENDENCY = "depends_on"
STRUCTURAL = ("asserted_in", "renders_as", "derived_from", "supports", "supersedes")


class Workspace(object):
    def __init__(self, root):
        self.root = Path(root)
        self.dir = self.root / WI_DIR
        self.db_path = self.dir / "workspace.db"
        self.objects = self.dir / "objects" / "sha256"
        self._db = None

    # -- discovery ---------------------------------------------------------
    @staticmethod
    def find(start="."):
        p = Path(start).resolve()
        for cand in [p] + list(p.parents):
            if (cand / WI_DIR / "workspace.db").exists():
                return Workspace(cand)
        raise WIError("WI_INPUT_INVALID", "no Writing Intelligence workspace found",
                      ["run `wi init` in your project directory"],
                      {"searched_from": str(p)})

    @staticmethod
    def find_or_none(start="."):
        try:
            return Workspace.find(start)
        except WIError:
            return None

    # -- lifecycle ---------------------------------------------------------
    def create(self, title, mode):
        for sub in ("objects/sha256", "snapshots", "graph", "decisions",
                    "judgments", "builds", "reports", "attestations", "cache"):
            (self.dir / sub).mkdir(parents=True, exist_ok=True)
        db = self.db
        db.executescript(DDL)
        db.execute(
            "INSERT OR REPLACE INTO workspace VALUES (?,?,?,?,?,?)",
            (logical_id("workspace", str(self.root.resolve())), title,
             _now(), SCHEMA_VERSION, VERSION, mode))
        db.commit()

    @property
    def db(self):
        if self._db is None:
            self.dir.mkdir(parents=True, exist_ok=True)
            self._db = sqlite3.connect(str(self.db_path))
            self._db.row_factory = sqlite3.Row
            self._db.execute("PRAGMA foreign_keys = ON")
        return self._db

    def meta(self):
        row = self.db.execute("SELECT * FROM workspace LIMIT 1").fetchone()
        return dict(row) if row else {}

    # -- objects -----------------------------------------------------------
    def put_blob(self, raw, media_type="application/octet-stream"):
        d = blob_digest(raw)
        hexd = d.split(":", 1)[1]
        path = self.objects / hexd[:2] / hexd[2:4] / hexd
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.db.execute(
            "INSERT OR IGNORE INTO object_blob VALUES (?,?,?,?,?)",
            (d, media_type, len(raw), str(path.relative_to(self.root)), _now()))
        return d

    def get_blob(self, digest):
        hexd = digest.split(":", 1)[1]
        path = self.objects / hexd[:2] / hexd[2:4] / hexd
        if not path.exists():
            raise WIError("WI_GRAPH_INTEGRITY", "object %s is missing" % digest[:19],
                          ["re-ingest the source", "restore the workspace object store"])
        return path.read_bytes()

    # -- graph -------------------------------------------------------------
    def put_node(self, logical, node_type, schema_id, payload, sdigest=None):
        sd = sdigest or state_digest(payload, schema_id)
        db = self.db
        db.execute("INSERT OR IGNORE INTO node VALUES (?,?,?)",
                   (logical, node_type, _now()))
        db.execute("INSERT OR IGNORE INTO node_state VALUES (?,?,?,?,?,?)",
                   (sd, logical, schema_id, content_digest(payload),
                    json.dumps(payload, sort_keys=True, ensure_ascii=False), _now()))
        db.execute("INSERT OR REPLACE INTO current_state VALUES (?,?,?)",
                   (logical, sd, _now()))
        return sd

    def put_edge(self, frm, to, relation, payload=None):
        eid = logical_id("edge", frm, to, relation)
        sd = state_digest({"from": frm, "to": to, "relation": relation,
                           "payload": payload}, "graph.edge")
        self.db.execute("INSERT OR REPLACE INTO edge VALUES (?,?,?,?,?,?,?)",
                        (eid, frm, to, relation, sd,
                         json.dumps(payload or {}, sort_keys=True), _now()))
        return eid

    def node_type(self, logical):
        row = self.db.execute("SELECT node_type FROM node WHERE logical_id=?",
                              (logical,)).fetchone()
        return row["node_type"] if row else None

    def current(self, logical):
        row = self.db.execute(
            "SELECT ns.* FROM current_state cs JOIN node_state ns"
            " ON ns.state_digest = cs.state_digest WHERE cs.logical_id=?",
            (logical,)).fetchone()
        return dict(row) if row else None

    def payload(self, logical):
        cur = self.current(logical)
        return json.loads(cur["payload_json"]) if cur else None

    def dependents(self, logical):
        """Nodes that declare a dependency on this one."""
        return [r["from_logical_id"] for r in self.db.execute(
            "SELECT from_logical_id FROM edge WHERE to_logical_id=? AND relation=?",
            (logical, DEPENDENCY))]

    def outgoing(self, logical, relation=None):
        if relation:
            q = "SELECT * FROM edge WHERE from_logical_id=? AND relation=?"
            return [dict(r) for r in self.db.execute(q, (logical, relation))]
        return [dict(r) for r in self.db.execute(
            "SELECT * FROM edge WHERE from_logical_id=?", (logical,))]

    def nodes(self, node_type=None):
        if node_type:
            q = ("SELECT n.logical_id, n.node_type, cs.state_digest FROM node n"
                 " LEFT JOIN current_state cs ON cs.logical_id=n.logical_id"
                 " WHERE n.node_type=? ORDER BY n.logical_id")
            return [dict(r) for r in self.db.execute(q, (node_type,))]
        q = ("SELECT n.logical_id, n.node_type, cs.state_digest FROM node n"
             " LEFT JOIN current_state cs ON cs.logical_id=n.logical_id"
             " ORDER BY n.node_type, n.logical_id")
        return [dict(r) for r in self.db.execute(q)]

    def edges(self):
        return [dict(r) for r in self.db.execute(
            "SELECT * FROM edge ORDER BY relation, from_logical_id, to_logical_id")]

    def counts(self):
        out = {}
        for r in self.db.execute(
                "SELECT node_type, COUNT(*) c FROM node GROUP BY node_type"):
            out[r["node_type"]] = r["c"]
        return out

    def mark_stale(self, cause_sd, logical, sd, reason):
        cur = self.current(logical)
        sd = sd or (cur["state_digest"] if cur else "")
        self.db.execute(
            "INSERT OR REPLACE INTO invalidation VALUES (?,?,?,?,?,?)",
            (logical_id("inv", cause_sd, logical, reason), cause_sd, sd, logical,
             reason, _now()))

    def stale_nodes(self):
        return {r["affected_logical_id"]: r["reason_code"] for r in self.db.execute(
            "SELECT affected_logical_id, reason_code FROM invalidation")}

    def clear_stale(self, logical):
        self.db.execute("DELETE FROM invalidation WHERE affected_logical_id=?",
                        (logical,))

    def commit(self):
        self.db.commit()


def _now():
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


# --------------------------------------------------------------------------
# Graph writing: turn a ledger into nodes and edges.
# --------------------------------------------------------------------------

def register_sources(ws, sources):
    """Ingest sources as content-addressed artifacts with immutable versions."""
    registered = []
    for s in _source_records(sources):
        if not s.get("text"):
            registered.append({"path": s["id"], "readable": False,
                               "note": s.get("note")})
            continue
        raw = Path(s["id"]).read_bytes()
        digest = ws.put_blob(raw, "text/plain")
        art_id, ver_id = s["artifact_id"], s["logical_id"]

        prev = ws.payload(art_id)
        # Rights and consent start `unknown` and are never silently upgraded.
        art_payload = {"path": str(Path(s["id"]).as_posix()),
                       "title": s["title"], "media_type": "text/plain",
                       "confidentiality": "unlabelled",
                       "rights": {"basis": "unknown", "scope": None,
                                  "expires_at": None},
                       "identity": {"contains_identifiable_person": None,
                                    "consent_basis": "unknown"}}
        ws.put_node(art_id, "source.artifact", "source.artifact", art_payload)
        ver_payload = {"artifact": art_id, "blob_digest": digest,
                       "byte_length": len(raw)}
        ver_sd = ws.put_node(ver_id, "source.version", "source.version",
                             ver_payload, s["state_digest"])
        ws.put_edge(ver_id, art_id, "derived_from")

        prior = [n["logical_id"] for n in ws.nodes("source.version")
                 if ws.payload(n["logical_id"]) and
                 ws.payload(n["logical_id"]).get("artifact") == art_id and
                 n["logical_id"] != ver_id]
        for p in prior:
            ws.put_edge(ver_id, p, "supersedes")

        registered.append({"path": s["id"], "readable": True,
                           "artifact": art_id, "version": ver_id,
                           "blob_digest": digest, "state_digest": ver_sd,
                           "bytes": len(raw), "new": prev is None,
                           "superseded": prior})
    ws.commit()
    return registered


def write_ledger_to_graph(ws, ledger):
    """Persist paragraphs, atoms, anchors, checks and their dependency edges."""
    doc = ledger["document"]
    work_id = logical_id("work", doc)
    ws.put_node(work_id, "structure.work", "structure.work",
                {"document": doc, "digest": ledger["document_digest"]})

    for para in ledger["paragraphs"]:
        ws.put_node(para["logical_id"], "structure.paragraph", "structure.paragraph",
                    {"document": doc, "index": para["index"],
                     "line": para["line"], "text": fold_ws(para["text"])},
                    para["state_digest"])
        ws.put_edge(para["logical_id"], work_id, "asserted_in")
        ws.put_edge(work_id, para["logical_id"], DEPENDENCY)

    by_id = {a["anchor_id"]: a for a in ledger.get("anchors", [])}
    for a in by_id.values():
        ws.put_node(a["anchor_id"], "source.segment", "evidence.anchor",
                    {"source": a["source_logical_id"],
                     "source_blob_digest": a.get("source_blob_digest"),
                     "start_byte": a["start_byte"], "end_byte": a["end_byte"],
                     "quote_digest": a["quote_digest"]},
                    a["state_digest"])
        ws.put_edge(a["anchor_id"], a["source_logical_id"], "derived_from")
        ws.put_edge(a["anchor_id"], a["source_logical_id"], DEPENDENCY)

    for atom in ledger["atoms"]:
        ws.put_node(atom["logical_id"], "meaning.claim_atom", "meaning.claim_atom",
                    {"class": atom["class"], "realm": atom["realm"],
                     "surface": fold_ws(atom["text"]),
                     "proposition": atom["proposition"]},
                    atom["state_digest"])
        ws.put_edge(atom["logical_id"], atom["paragraph"], "asserted_in")
        ws.put_edge(atom["paragraph"], atom["logical_id"], DEPENDENCY)
        for aid in atom["anchors"]:
            if aid in by_id:
                ws.put_edge(by_id[aid]["anchor_id"], atom["logical_id"], "supports")
                ws.put_edge(atom["logical_id"], aid, DEPENDENCY)

        if atom["checks"]:
            vid = logical_id("verification", atom["logical_id"], atom["state_digest"])
            ws.put_node(vid, "verification.result", "verification.record",
                        {"claim": atom["logical_id"],
                         "claim_state": atom["state_digest"],
                         "status": atom["status"], "checks": atom["checks"]})
            ws.put_edge(vid, atom["logical_id"], DEPENDENCY)

    ws.commit()
    return work_id


def register_targets(ws, project):
    """A release target depends on the works that render into it."""
    targets = (project or {}).get("targets") or {}
    made = []
    if not isinstance(targets, dict):
        return made
    for name, spec in targets.items():
        spec = spec or {}
        tid = logical_id("target", name)
        ws.put_node(tid, "release.target", "release.target",
                    {"name": name, "renderer": spec.get("renderer"),
                     "entry": spec.get("entry")})
        for work in ws.nodes("structure.work"):
            pay = ws.payload(work["logical_id"]) or {}
            entry = spec.get("entry")
            if not entry or fnmatch.fnmatch(pay.get("document", ""), entry):
                ws.put_edge(work["logical_id"], tid, "renders_as")
                ws.put_edge(tid, work["logical_id"], DEPENDENCY)
        made.append(name)
    ws.commit()
    return made


# --------------------------------------------------------------------------
# Staleness: invalidation and the minimum repair frontier.
#
# The rule that makes this useful rather than alarming: an anchor whose byte
# range lies outside every changed region of a source is provably unaffected,
# and propagation stops there.
# --------------------------------------------------------------------------

def changed_byte_ranges(old_text, new_text):
    """Byte ranges of `old_text` that the edit touched."""
    sm = difflib.SequenceMatcher(None, old_text, new_text, autojunk=False)
    ranges = []
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        b1 = len(old_text[:i1].encode("utf-8"))
        b2 = len(old_text[:max(i2, i1 + 1)].encode("utf-8"))
        ranges.append((b1, b2))
    return ranges


def _overlaps(span, ranges):
    s, e = span
    return any(not (e <= r0 or s >= r1) for r0, r1 in ranges)


def compute_impact(ws, artifact_id, old_version, new_version, changed_ranges):
    """Return the exact stale set and the exact provably-unaffected set."""
    all_anchors = [n["logical_id"] for n in ws.nodes("source.segment")]
    affected_anchors, safe_anchors = [], []
    for aid in all_anchors:
        pay = ws.payload(aid) or {}
        if pay.get("source") not in (old_version, new_version, artifact_id):
            continue
        span = (pay.get("start_byte", 0), pay.get("end_byte", 0))
        if changed_ranges is None or _overlaps(span, changed_ranges):
            affected_anchors.append(aid)
        else:
            safe_anchors.append(aid)

    stale, queue, seen = [], list(affected_anchors), set(affected_anchors)
    while queue:
        node = queue.pop(0)
        stale.append(node)
        for dep in ws.dependents(node):
            if dep not in seen:
                seen.add(dep)
                queue.append(dep)

    grouped = {}
    for n in stale:
        grouped.setdefault(ws.node_type(n) or "unknown", []).append(n)

    total = {}
    for n in ws.nodes():
        total[n["node_type"]] = total.get(n["node_type"], 0) + 1

    return {"cause": {"artifact": artifact_id, "old_version": old_version,
                      "new_version": new_version,
                      "changed_ranges": changed_ranges},
            "stale": grouped, "stale_total": len(stale),
            "unaffected_anchors": safe_anchors,
            "totals": total}


REPAIR_COST = {"rerun_check": 1, "rerun_judgment": 2, "replace_anchor": 3,
               "qualify_claim": 4, "remove_claim": 5,
               "request_human_resolution": 8, "rebuild_target": 2}


def repair_plan(impact):
    steps = []
    anchors = impact["stale"].get("source.segment", [])
    atoms = impact["stale"].get("meaning.claim_atom", [])
    verifs = impact["stale"].get("verification.result", [])
    targets = impact["stale"].get("release.target", [])
    if anchors:
        steps.append(("replace_anchor",
                      "re-anchor %d claim(s) to the current source version" % len(anchors)))
    if verifs or atoms:
        steps.append(("rerun_check",
                      "re-run deterministic checks on %d claim atom(s)" % max(len(atoms), 1)))
    if targets:
        steps.append(("rebuild_target",
                      "rebuild %d target(s): %s" % (len(targets), ", ".join(
                          sorted(t[:8] for t in targets)))))
    cost = sum(REPAIR_COST.get(k, 1) for k, _ in steps)
    return {"steps": [{"op": k, "detail": d} for k, d in steps], "cost": cost}


# --------------------------------------------------------------------------
# Deterministic semantic diff.
#
# The judged remainder is out of scope for this tier and says so. Everything
# below is structural comparison: it cannot be wrong about what it reports,
# only silent about what it cannot see.
# --------------------------------------------------------------------------

DELTA_PROOF_IMPACT = {
    "quantity_changed": "invalidates",
    "unit_changed": "invalidates",
    "date_changed": "invalidates",
    "temporal_scope_changed": "invalidates",
    "entity_changed": "invalidates",
    "attribution_changed": "invalidates",
    "certainty_strengthened": "invalidates",
    "certainty_weakened": "requires_recheck",
    "negation_changed": "invalidates",
    "causality_added": "invalidates",
    "causality_removed": "requires_recheck",
    "scope_broadened": "invalidates",
    "scope_narrowed": "requires_recheck",
    "obligation_added": "invalidates",
    "obligation_removed": "requires_recheck",
    "recommendation_changed": "requires_recheck",
    "citation_binding_changed": "invalidates",
    "compression": "unaffected",
    "expansion": "unaffected",
    "wording_only": "unaffected",
}

MODAL_STRENGTH = {"may": 1, "should": 2, "will": 3, "must": 4, "is": 3}


def compare_atoms(a, b):
    """Classify the semantic delta between two claim atom states."""
    pa, pb = a["proposition"], b["proposition"]
    deltas = []

    qa = sorted((x["value"], x["unit"] or "") for x in pa["quantities"])
    qb = sorted((x["value"], x["unit"] or "") for x in pb["quantities"])
    if [v for v, _ in qa] != [v for v, _ in qb]:
        deltas.append("quantity_changed")
    elif [u for _, u in qa] != [u for _, u in qb]:
        deltas.append("unit_changed")

    ta, tb = pa["temporal_scope"] or {}, pb["temporal_scope"] or {}
    if ta.get("start") != tb.get("start") or ta.get("end") != tb.get("end"):
        if ta or tb:
            deltas.append("temporal_scope_changed" if (ta and tb) else "date_changed")

    if pa["modality"] != pb["modality"]:
        sa, sb = MODAL_STRENGTH.get(pa["modality"], 3), MODAL_STRENGTH.get(pb["modality"], 3)
        deltas.append("certainty_strengthened" if sb > sa else "certainty_weakened")
        if pb["modality"] in ("must",) and pa["modality"] not in ("must",):
            deltas.append("obligation_added")
        if pa["modality"] in ("must",) and pb["modality"] not in ("must",):
            deltas.append("obligation_removed")

    if pa["hedged"] and not pb["hedged"]:
        if "certainty_strengthened" not in deltas:
            deltas.append("certainty_strengthened")
    if pb["hedged"] and not pa["hedged"]:
        if "certainty_weakened" not in deltas:
            deltas.append("certainty_weakened")

    if pa["negated"] != pb["negated"]:
        deltas.append("negation_changed")
    if pa["attribution"] != pb["attribution"]:
        deltas.append("attribution_changed")
    if set(pa["entities"]) != set(pb["entities"]):
        deltas.append("entity_changed")
    if pa["causal"] != pb["causal"]:
        deltas.append("causality_added" if pb["causal"] else "causality_removed")
    if pa["categorical"] != pb["categorical"]:
        deltas.append("scope_broadened" if pb["categorical"] else "scope_narrowed")

    sa, sb = fold_ws(a["text"]), fold_ws(b["text"])
    if not deltas and sa != sb:
        ratio = len(sb) / float(max(len(sa), 1))
        deltas.append("compression" if ratio < 0.75 else
                      "expansion" if ratio > 1.33 else "wording_only")

    impact = {"invalidates": [], "requires_recheck": [], "unaffected": []}
    for d in deltas:
        impact.setdefault(DELTA_PROOF_IMPACT.get(d, "requires_recheck"), []).append(d)
    return {"deltas": deltas, "proof_impact": impact,
            "judged_remainder": bool(sa != sb and deltas in ([], ["wording_only"]))}


def semantic_diff(old_ledger, new_ledger):
    """Align atoms by identity, then by wording, and classify what changed."""
    old_by = {}
    for a in old_ledger["atoms"]:
        old_by.setdefault(a["logical_id"], a)
    new_by = {}
    for b in new_ledger["atoms"]:
        new_by.setdefault(b["logical_id"], b)

    same_id = set(old_by) & set(new_by)
    changes, added, removed = [], [], []

    unmatched_old = [old_by[k] for k in old_by if k not in same_id]
    unmatched_new = [new_by[k] for k in new_by if k not in same_id]

    # Identity match: same meaning skeleton, so any difference is wording.
    for k in sorted(same_id):
        a, b = old_by[k], new_by[k]
        if fold_ws(a["text"]) != fold_ws(b["text"]):
            changes.append({"before": a["text"], "after": b["text"],
                            "logical_id": k, **compare_atoms(a, b)})

    # Surface match: different skeleton, so the meaning moved. This is the
    # class of edit v4 could see happening and could not name.
    used = set()
    for a in unmatched_old:
        best, score = None, 0.0
        for i, b in enumerate(unmatched_new):
            if i in used:
                continue
            r = difflib.SequenceMatcher(None, fold_ws(a["text"]).lower(),
                                        fold_ws(b["text"]).lower()).ratio()
            if r > score:
                best, score = i, r
        if best is not None and score >= 0.55:
            used.add(best)
            b = unmatched_new[best]
            changes.append({"before": a["text"], "after": b["text"],
                            "logical_id": a["logical_id"],
                            "new_logical_id": b["logical_id"],
                            **compare_atoms(a, b)})
        else:
            removed.append(a)
    for i, b in enumerate(unmatched_new):
        if i not in used:
            added.append(b)

    return {"changed": changes, "added": added, "removed": removed,
            "note": "deterministic classes only; paraphrase equivalence is a "
                    "judgment-tier question and was not evaluated"}


# --------------------------------------------------------------------------
# Writing tests and the concept registry.
# --------------------------------------------------------------------------

def _iter_docs(root, patterns):
    seen = []
    for pat in patterns or []:
        for p in sorted(Path(root).glob(pat)):
            if p.is_file() and p not in seen:
                seen.append(p)
    return seen


def run_writing_tests(root, project, tests, ledgers):
    """Execute the test suite. Each result names its basis, never a score."""
    results = []
    concepts = (project or {}).get("concepts") or {}
    if not isinstance(concepts, dict):
        concepts = {}

    def add(tid, ok, basis, detail, members=None):
        results.append({"id": tid, "result": "pass" if ok else "fail",
                        "basis": basis, "detail": detail,
                        "members": members or []})

    for t in tests or []:
        if not isinstance(t, dict):
            continue
        tid = t.get("id") or t.get("name") or "unnamed"
        assertion = t.get("assert")

        if assertion == "evidence.coverage":
            need, have, missing = 0, 0, []
            for led in ledgers:
                for a in led["atoms"]:
                    if a["class"] != "sourced_fact":
                        continue
                    need += 1
                    if a["status"] in SUPPORTED_STATES:
                        have += 1
                    else:
                        missing.append("%s:%d %s" % (led["document"], a["line"],
                                                     _trunc(a["text"], 60)))
            want = t.get("equals", 1.0)
            ratio = (have / float(need)) if need else 1.0
            add(tid, ratio >= float(want), "verified",
                "%d of %d required claim atoms carry a verbatim span (%.3f)"
                % (have, need, ratio), missing)

        elif assertion == "terminology.forbidden":
            term = t.get("term") or ""
            hits = []
            for p in _iter_docs(root, t.get("in") or ["**/*.md"]):
                text = read_text(p)
                for m in re.finditer(re.escape(term), text, re.I):
                    hits.append("%s:%d" % (p, text.count("\n", 0, m.start()) + 1))
            add(tid, not hits, "verified",
                "forbidden term %r found %d time(s)" % (term, len(hits)), hits)

        elif assertion == "concept.equals":
            name = t.get("concept")
            spec = (concepts.get(name) or {}) if isinstance(concepts, dict) else {}
            canonical = str(spec.get("canonical", t.get("equals", "")) or "")
            if not canonical:
                add(tid, True, "unavailable",
                    "concept %r is not in the registry; nothing to compare" % name)
                continue
            hits, misses = [], []
            for p in _iter_docs(root, t.get("in") or ["**/*.md"]):
                text = read_text(p)
                if canonical and canonical.lower() in text.lower():
                    hits.append(str(p))
                else:
                    misses.append(str(p))
            aliases = spec.get("aliases") or {}
            forbidden = (spec.get("forbidden_aliases")
                         or (aliases.get("forbidden") if isinstance(aliases, dict) else None)
                         or [])
            for alias in forbidden:
                for p in _iter_docs(root, t.get("in") or ["**/*.md"]):
                    if str(alias).lower() in read_text(p).lower():
                        misses.append("%s uses forbidden alias %r" % (p, alias))
            add(tid, not misses, "verified",
                "concept %r canonical value present in %d file(s)" % (name, len(hits)),
                misses)

        elif assertion == "structure.required_section":
            heading = (t.get("section") or "").lower()
            misses = []
            for p in _iter_docs(root, t.get("in") or ["**/*.md"]):
                text = read_text(p).lower()
                if not re.search(r"^#{1,6}\s*.*%s" % re.escape(heading), text, re.M):
                    misses.append(str(p))
            add(tid, not misses, "verified",
                "required section %r missing from %d file(s)" % (heading, len(misses)),
                misses)

        elif assertion == "citations.orphans":
            orphans = []
            for led in ledgers:
                for a in led["atoms"]:
                    for c in a["checks"]:
                        if c["check"] == "citation.resolution" and c["result"] == "fail":
                            orphans.append("%s:%d %s" % (led["document"], a["line"],
                                                         _trunc(a["text"], 60)))
            add(tid, not orphans, "verified",
                "%d citation(s) resolve to nothing supplied" % len(orphans), orphans)

        else:
            add(tid, True, "unavailable",
                "assertion %r is not implemented in this tier; not evaluated"
                % assertion)

    return results


# --------------------------------------------------------------------------
# Proof-carrying release bundles (.wiab).
# --------------------------------------------------------------------------

WIAB_EPOCH = (1980, 1, 1, 0, 0, 0)


def _jsonl(rows):
    return "\n".join(json.dumps(r, sort_keys=True, ensure_ascii=False)
                     for r in rows) + ("\n" if rows else "")


def build_bundle(ws, out_path, project, policy, artifacts, ledgers, verdict,
                 profile="hash-only"):
    """Write a deterministic archive. Same inputs, same bytes, every time."""
    nodes = ws.nodes()
    edges = ws.edges()
    stale = ws.stale_nodes()

    node_rows = []
    for n in nodes:
        cur = ws.current(n["logical_id"])
        node_rows.append({"logical_id": n["logical_id"], "type": n["node_type"],
                          "state_digest": n.get("state_digest"),
                          "schema": cur["schema_id"] if cur else None,
                          "stale": n["logical_id"] in stale})
    edge_rows = [{"from": e["from_logical_id"], "to": e["to_logical_id"],
                  "relation": e["relation"], "state_digest": e["edge_state_digest"],
                  "payload": json.loads(e["payload_json"] or "{}")}
                 for e in edges]

    check_rows, source_rows = [], []
    for led in ledgers:
        for a in led["atoms"]:
            for c in a["checks"]:
                check_rows.append({"claim": a["logical_id"],
                                   "claim_state": a["state_digest"],
                                   "check": c["check"], "result": c["result"],
                                   "basis": c["basis"], "detail": c.get("detail")})
        for s in led.get("sources", []):
            row = {"logical_id": s["logical_id"],
                   "artifact_id": s.get("artifact_id"), "title": s["title"],
                   "state_digest": s["state_digest"],
                   "blob_digest": s.get("blob_digest"),
                   "readable": s["readable"],
                   "byte_length": s.get("byte_length")}
            if row not in source_rows:
                source_rows.append(row)

    anchor_rows = []
    for led in ledgers:
        for a in led.get("anchors", []):
            anchor_rows.append({"anchor_id": a["anchor_id"],
                                "anchor_type": a["anchor_type"],
                                "source": a["source_logical_id"],
                                "source_state": a["source_state_digest"],
                                "start_byte": a["start_byte"],
                                "end_byte": a["end_byte"],
                                "quote_digest": a["quote_digest"]})

    required = sum(1 for led in ledgers for a in led["atoms"]
                   if a["class"] == "sourced_fact")
    permitted = sum(1 for led in ledgers for a in led["atoms"]
                    if a["class"] == "sourced_fact"
                    and a["status"] in SUPPORTED_STATES)

    entries = []          # (arcname, bytes)
    artifact_entries = []
    for path in artifacts:
        p = Path(path)
        if not p.exists():
            raise WIError("WI_BUILD_FAILED", "artifact %s not found" % p,
                          ["build the target first", "correct the path"])
        raw = p.read_bytes()
        arc = "artifact/%s" % p.name
        entries.append((arc, raw))
        artifact_entries.append({"target": p.stem, "path": arc,
                                 "digest": blob_digest(raw),
                                 "byte_length": len(raw)})

    if profile == "full":
        # Redistributes source bytes. Whoever ships this inherits their licence.
        for row in source_rows:
            if not row.get("blob_digest"):
                continue
            try:
                raw = ws.get_blob(row["blob_digest"])
            except WIError:
                continue
            entries.append(("sources/blobs/%s" % row["blob_digest"].split(":")[1], raw))
    elif profile == "redacted":
        # Approved evidence excerpts only: the anchored spans, nothing else.
        excerpts = []
        for led in ledgers:
            for a in led.get("anchors", []):
                excerpts.append({"anchor_id": a["anchor_id"],
                                 "source": a["source_logical_id"],
                                 "start_byte": a["start_byte"],
                                 "end_byte": a["end_byte"],
                                 "quote": a["quote"],
                                 "quote_digest": a["quote_digest"]})
        entries.append(("evidence/excerpts.jsonl", _jsonl(excerpts).encode("utf-8")))

    entries.append(("graph/nodes.jsonl", _jsonl(node_rows).encode("utf-8")))
    entries.append(("graph/edges.jsonl", _jsonl(edge_rows).encode("utf-8")))
    entries.append(("proof/checks.jsonl", _jsonl(check_rows).encode("utf-8")))
    entries.append(("proof/judgments.jsonl", b""))
    entries.append(("decisions/decisions.jsonl", b""))
    entries.append(("sources/sources.lock", _jsonl(source_rows).encode("utf-8")))
    entries.append(("sources/anchor-index.json",
                    canonical_bytes({"anchors": anchor_rows})))
    entries.append(("policy/wi.policy.json", canonical_bytes(policy or {})))
    entries.append(("build/environment.json", canonical_bytes({
        "core": "wi.py", "core_version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "canonicalization": CANONICALIZATION,
        "reproducibility_class": "deterministic",
        "python_required": ">=3.8", "network": False})))

    proof_closure = content_digest({"nodes": node_rows, "edges": edge_rows,
                                    "checks": check_rows, "sources": source_rows,
                                    "anchors": anchor_rows})
    for a in artifact_entries:
        a["proof_closure_digest"] = proof_closure

    manifest = {
        "format": WIAB_FORMAT,
        "version": SCHEMA_VERSION,
        "profile": profile,
        "release_id": logical_id("release", proof_closure, verdict),
        "project_id": (project or {}).get("project", {}).get("id", "untitled"),
        "project_state_digest": proof_closure,
        "policy_digest": content_digest(policy or {}),
        "core": {"name": "wi.py", "version": VERSION},
        "targets": artifact_entries,
        "gate": {"verdict": verdict["decision"],
                 "reasons": verdict.get("reasons", [])},
        "counts": {"claim_atoms_required": required,
                   "claim_atoms_permitted": permitted,
                   "waivers": 0, "stale_nodes": len(stale),
                   "nodes": len(node_rows), "edges": len(edge_rows)},
        "checks_not_run": ledgers[0].get("checks_not_run", []) if ledgers else [],
        "attestations": [],
    }
    entries.append(("manifest.json", canonical_bytes(manifest)))

    sums = "\n".join("%s  %s" % (sha256_hex(data), arc)
                     for arc, data in sorted(entries)) + "\n"
    entries.append(("checksums.sha256", sums.encode("utf-8")))

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for arc, data in sorted(entries):
            info = zipfile.ZipInfo(arc, date_time=WIAB_EPOCH)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return manifest, out


def verify_bundle(path):
    """Offline verification. No model, no network, no trust in the producer."""
    p = Path(path)
    if not p.exists():
        raise WIError("WI_INPUT_INVALID", "%s not found" % p, ["check the path"])
    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "result": "PASS" if ok else "FAIL",
                       "detail": detail})
        return ok

    try:
        z = zipfile.ZipFile(p)
    except Exception as exc:
        raise WIError("WI_RELEASE_TAMPERED", "archive is unreadable: %s" % exc,
                      ["obtain an intact copy of the bundle"])

    with z:
        names = set(z.namelist())
        add("archive.integrity", z.testzip() is None)
        required = {"manifest.json", "checksums.sha256", "graph/nodes.jsonl",
                    "graph/edges.jsonl", "proof/checks.jsonl"}
        missing = sorted(required - names)
        add("bundle.completeness", not missing, ", ".join(missing))
        if missing:
            return {"ok": False, "checks": checks, "manifest": None}

        manifest = json.loads(z.read("manifest.json").decode("utf-8"))
        add("manifest.format", manifest.get("format") == WIAB_FORMAT,
            manifest.get("format", "absent"))

        # 1. Every file matches the checksum manifest.
        declared = {}
        for line in z.read("checksums.sha256").decode("utf-8").splitlines():
            if not line.strip():
                continue
            h, _, arc = line.partition("  ")
            declared[arc] = h
        bad = []
        for arc in sorted(names):
            if arc == "checksums.sha256":
                continue
            want = declared.get(arc)
            if want is None:
                bad.append("%s is not listed in checksums.sha256" % arc)
                continue
            if sha256_hex(z.read(arc)) != want:
                bad.append("%s does not match its recorded digest" % arc)
        add("object.digests", not bad, "; ".join(bad[:4]))

        # 2. The shipped artifact is the one the manifest approved.
        art_bad = []
        for t in manifest.get("targets", []):
            arc = t.get("path")
            if arc not in names:
                art_bad.append("%s is missing" % arc)
                continue
            if blob_digest(z.read(arc)) != t.get("digest"):
                art_bad.append("%s is not the artifact that was verified" % arc)
        add("release.artifact_digest", not art_bad, "; ".join(art_bad))

        # 3. Graph references resolve.
        nodes = [json.loads(l) for l in
                 z.read("graph/nodes.jsonl").decode("utf-8").splitlines() if l.strip()]
        edges = [json.loads(l) for l in
                 z.read("graph/edges.jsonl").decode("utf-8").splitlines() if l.strip()]
        ids = {n["logical_id"] for n in nodes}
        dangling = [e for e in edges if e["from"] not in ids or e["to"] not in ids]
        add("graph.reference_integrity", not dangling,
            "%d dangling edge(s)" % len(dangling))

        # 4. Proof closure still describes what is in the bundle.
        checks_rows = [json.loads(l) for l in
                       z.read("proof/checks.jsonl").decode("utf-8").splitlines() if l.strip()]
        claim_ids = {n["logical_id"] for n in nodes if n["type"] == "meaning.claim_atom"}
        orphan_checks = [c for c in checks_rows if c["claim"] not in claim_ids]
        add("proof.dependencies", not orphan_checks,
            "%d check(s) reference a claim not in the graph" % len(orphan_checks))

        # 5. Stale closure.
        stale = [n for n in nodes if n.get("stale")]
        add("release.stale_closure", not stale, "%d stale node(s)" % len(stale))

        # 6. Counts in the manifest are the counts in the bundle.
        counts = manifest.get("counts", {})
        add("manifest.counts", counts.get("nodes") == len(nodes)
            and counts.get("edges") == len(edges),
            "manifest says %s nodes / %s edges; bundle has %d / %d"
            % (counts.get("nodes"), counts.get("edges"), len(nodes), len(edges)))

        add("core.version", bool(manifest.get("core", {}).get("version")),
            manifest.get("core", {}).get("version", "absent"))

        signed = "attestations/signature.bundle" in names
        checks.append({"check": "release.signature",
                       "result": "PASS" if signed else "SKIP",
                       "detail": "unsigned bundle" if not signed else ""})

    ok = all(c["result"] != "FAIL" for c in checks)
    return {"ok": ok, "checks": checks, "manifest": manifest}


# --------------------------------------------------------------------------
# Capability negotiation. Law C as protocol.
# --------------------------------------------------------------------------

def capabilities(root="."):
    ws = Workspace.find_or_none(root)
    return {
        "core": VERSION,
        "schema_version": SCHEMA_VERSION,
        "canonicalization": CANONICALIZATION,
        "python": "%d.%d.%d" % sys.version_info[:3],
        "capabilities": {
            "filesystem": True,
            "workspace": bool(ws),
            "workspace_root": str(ws.root) if ws else None,
            "deterministic_checks": [
                "source.digest", "source.quarantine", "anchor.integrity",
                "quote.verbatim", "numeric.value", "date.range",
                "entity.presence", "citation.resolution",
                "graph.reference_integrity", "release.closure",
                "release.artifact_digest"],
            "anchor_types": SUPPORTED_ANCHOR_TYPES,
            "binary_ingest": [],
            "judgment": [],
            "signing": ["local_sha256"],
            "network": False,
            "bundles": ["wiab-full", "wiab-hash-only", "wiab-redacted"],
        },
        "unavailable": {
            "paraphrase_entailment": "no judgment provider is configured",
            "pdf_region": "adapter specified, not executable in this build",
            "sheet_range": "adapter specified, not executable in this build",
            "audio_time": "adapter specified, not executable in this build",
            "video_time": "adapter specified, not executable in this build",
            "image_region": "adapter specified, not executable in this build",
            "external_signing": "Sigstore and C2PA paths are specified, not executable",
        },
    }


# --------------------------------------------------------------------------
# v5 gate: the v4 verdict, extended over atoms and staleness.
# --------------------------------------------------------------------------

BLOCK_STATES = {"unsafe"}
HOLD_STATES = {"needs_source", "conflicted", "candidate_support"}

# Statuses that count as support for coverage arithmetic. `span_supported`
# is included because every checkable component was found inside one span of
# one source — a deterministic result, not an inference. It is not the same
# as `supported`, and the report never merges them.
SUPPORTED_STATES = {"supported", "quote_verified", "span_supported"}


def gate_atoms(ledgers, mode="standard", stale=None):
    blocking, holding, advisory, reasons = [], [], [], []
    stale = stale or {}
    for led in ledgers:
        for a in led["atoms"]:
            st = a["status"]
            if st == "unsafe":
                blocking.append((a, "citation does not resolve to a supplied source"))
            elif st == "conflicted":
                (blocking if mode == "regulated" else holding).append(
                    (a, "source conflict or misquotation"))
            elif st == "span_supported":
                if mode == "regulated":
                    holding.append((a, "components co-located in one span; "
                                       "entailment not judged"))
            elif st == "candidate_support":
                if mode in ("strict", "regulated"):
                    holding.append((a, "components located but not co-located "
                                       "in a single span"))
                elif mode == "standard":
                    advisory.append((a, "components located but not co-located "
                                       "in a single span"))
            elif st == "needs_source":
                if mode in ("strict", "regulated"):
                    holding.append((a, "no verbatim support found"))
                elif mode == "standard":
                    advisory.append((a, "no verbatim support found"))
            if a["logical_id"] in stale:
                (blocking if mode == "regulated" else holding).append(
                    (a, "verified against an earlier source version"))

    if blocking:
        decision = "BLOCK"
    elif holding:
        decision = "HOLD"
    else:
        decision = "RELEASE"
    for _a, why in blocking + holding:
        reasons.append(why)
    return {"decision": decision, "mode": mode, "blocking": blocking,
            "holding": holding, "advisory": advisory,
            "reasons": sorted(set(reasons))}


# --------------------------------------------------------------------------
# v4 CLI
# --------------------------------------------------------------------------

def cmd_preserve(args):
    src = Path(args.path)
    if not src.exists():
        print("error: %s not found" % src, file=sys.stderr)
        return 2
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    ws = Workspace.find_or_none(src.parent)
    raw = src.read_bytes()
    if ws:
        # Content-addressed, so the same bytes are stored once however many
        # times you snapshot them, and the snapshot is addressable later.
        digest = ws.put_blob(raw, "text/plain")
        ws.commit()
        dst = ws.dir / "snapshots" / ("%s-%s%s" % (src.stem, stamp, src.suffix))
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(raw)
        print("preserved: %s" % dst)
        print("object:    %s" % digest)
        return 0
    dst = src.with_suffix(src.suffix + ".original-%s" % stamp)
    dst.write_bytes(raw)
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


def resolve_mode(args, default="standard"):
    """An explicit --mode wins; otherwise the project file decides.

    A tool that silently runs at `standard` while the project declares
    `regulated` is reporting a verdict the project did not ask for.
    """
    if getattr(args, "mode", None):
        return args.mode
    ws = Workspace.find_or_none(getattr(args, "root", ".") or ".")
    project = _load_project(ws.root if ws else ".")
    ev = project.get("evidence") or {}
    mode = ev.get("default_mode") if isinstance(ev, dict) else None
    if mode in ("light", "standard", "strict", "regulated"):
        return mode
    if mode == "off":
        return "light"
    return default


def cmd_gate(args):
    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    args.mode = resolve_mode(args)
    if "atoms" in ledger:
        # A v5 atom ledger. Same verdict words, finer unit of judgment, and
        # staleness from the workspace if one is present.
        ws = Workspace.find_or_none(getattr(args, "root", ".") or ".")
        stale = ws.stale_nodes() if ws else {}
        result = gate_atoms([ledger], mode=args.mode, stale=stale)
        report = render_atom_gate(result, [ledger], stale)
    else:
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


# --------------------------------------------------------------------------
# v5 CLI
# --------------------------------------------------------------------------

DEFAULT_PROJECT = """# Writing Intelligence v5 project file.
# Everything here is data. Nothing here is an instruction to a model.
project:
  id: %(id)s
  title: %(title)s
  language: en-US

inputs:
  - "drafts/**/*.md"

sources:
  - "sources/**/*"

evidence:
  default_mode: %(mode)s
  truth_claim: prohibited

release:
  block_on:
    - unresolved_citation
    - source_contradiction
    - invalid_anchor
  hold_on:
    - stale_claim
    - judgment_missing

privacy:
  network_default: deny
  telemetry_content: never

# Concepts that must not drift across artifacts. `wi test` enforces these.
concepts: {}

# Writing tests. Small, composable, and visible in the release report.
tests:
  - id: every_sourced_claim_has_support
    assert: evidence.coverage
    equals: 1.0
  - id: no_orphan_citations
    assert: citations.orphans
"""


def write_lock(ws, project=None):
    """Pin exactly what produced this state.

    Not a claim that anything remote is reproducible. A record of what was used.
    """
    sources = []
    for n in ws.nodes("source.version"):
        pay = ws.payload(n["logical_id"]) or {}
        art = ws.payload(pay.get("artifact")) or {}
        sources.append({"artifact": art.get("path"), "version": n["logical_id"],
                        "blob_digest": pay.get("blob_digest"),
                        "byte_length": pay.get("byte_length")})
    lock = {
        "lockfile_version": 1,
        "core": {"name": "wi.py", "version": VERSION},
        "schema_version": SCHEMA_VERSION,
        "canonicalization": CANONICALIZATION,
        "normalization": NORMALIZATION,
        "anchor_types": SUPPORTED_ANCHOR_TYPES,
        "judgment_providers": [],
        "reproducibility_class": "deterministic",
        "project_digest": content_digest(project or {}),
        "sources": sorted(sources, key=lambda r: (r["artifact"] or "")),
    }
    (ws.root / "wi.lock").write_text(
        json.dumps(lock, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8")
    return lock


def _load_project(root):
    p = Path(root) / PROJECT_FILE
    if p.exists():
        return load_yaml_file(p)
    return {}


def _ledger_path(ws, doc):
    key = sha256_hex(str(Path(doc).as_posix()).encode("utf-8"))[:16]
    return ws.dir / "graph" / ("ledger-%s.json" % key)


def _all_ledgers(ws):
    out = []
    for f in sorted((ws.dir / "graph").glob("ledger-*.json")):
        try:
            out.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:
            continue
    return out


def cmd_init(args):
    root = Path(args.dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    ws = Workspace(root)
    if ws.db_path.exists() and not args.force:
        print("workspace already exists at %s" % (root / WI_DIR))
        return 0
    title = args.title or root.name
    ws.create(title, args.mode)
    proj = root / PROJECT_FILE
    if not proj.exists():
        proj.write_text(DEFAULT_PROJECT % {
            "id": re.sub(r"[^a-z0-9\-]+", "-", title.lower()).strip("-") or "project",
            "title": title, "mode": args.mode}, encoding="utf-8")
    for d in ("sources", "drafts", "outputs"):
        (root / d).mkdir(exist_ok=True)
    write_lock(ws, _load_project(root))
    print("initialized workspace: %s" % (root / WI_DIR))
    print("  index    %s" % (root / WI_DIR / "workspace.db"))
    print("  objects  %s" % (root / WI_DIR / "objects" / "sha256"))
    print("  project  %s" % proj)
    print("  mode     %s" % args.mode)
    print("\nNext: `wi ingest sources/` then `wi atomize drafts/your-draft.md`")
    return 0


def cmd_ingest(args):
    ws = Workspace.find(args.root)
    sources = load_sources(args.paths)
    rows = register_sources(ws, sources)
    write_lock(ws, _load_project(ws.root))
    readable = [r for r in rows if r["readable"]]
    print("ingested %d file(s); %d readable, %d need extraction first"
          % (len(rows), len(readable), len(rows) - len(readable)))
    for r in rows:
        if not r["readable"]:
            print("  %-44s  %s" % (Path(r["path"]).name, r.get("note") or "unreadable"))
            continue
        flag = "new" if r["new"] else ("supersedes %d" % len(r["superseded"])
                                       if r["superseded"] else "unchanged")
        print("  %-44s  %s  %8d B  %s"
              % (Path(r["path"]).name, r["blob_digest"][:19], r["bytes"], flag))
    print("\nSources are stored by content digest. The raw bytes are hashed before")
    print("any normalization, so an extractor upgrade is a separate, visible change.")
    return 0


def cmd_atomize(args):
    ws = Workspace.find_or_none(args.root)
    project = _load_project(ws.root if ws else ".")
    ledger = atomize_document(args.document, project)
    if args.out:
        out = Path(args.out)
    elif ws:
        out = _ledger_path(ws, args.document)
        out.parent.mkdir(parents=True, exist_ok=True)
    else:
        out = Path(args.document).with_suffix(".atoms.json")
    out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")

    by_class = {}
    for a in ledger["atoms"]:
        by_class[a["class"]] = by_class.get(a["class"], 0) + 1
    multi = sum(1 for a in ledger["atoms"]
                if fold_ws(a["text"]) != fold_ws(a["sentence"]))
    print("%d claim atom(s) from %d paragraph(s) -> %s"
          % (len(ledger["atoms"]), len(ledger["paragraphs"]), out))
    for k in sorted(by_class):
        print("  %-16s %d" % (k, by_class[k]))
    print("  %d atom(s) came from splitting a compound sentence" % multi)
    print("script tier: %s (%s)" % (ledger["script_tier"], ledger["script_note"]))
    if ws:
        write_ledger_to_graph(ws, ledger)
        register_targets(ws, project)
        print("graph: %s" % ", ".join("%s %d" % (k, v)
                                      for k, v in sorted(ws.counts().items())))
    return 0


def cmd_anchor(args):
    ws = Workspace.find_or_none(args.root)
    ledger = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    sources = load_sources(args.sources)
    ledger = anchor_and_check(ledger, sources, tolerance=args.tolerance)
    out = Path(args.out or args.ledger)
    out.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = {}
    for a in ledger["atoms"]:
        counts[a["status"]] = counts.get(a["status"], 0) + 1
    print("anchored %d atom(s) against %d readable source(s) -> %s"
          % (len(ledger["atoms"]), ledger["sources_readable"], out))
    print("%d evidence anchor(s) bound (%s)"
          % (len(ledger["anchors"]), ", ".join(SUPPORTED_ANCHOR_TYPES)))
    for k in sorted(counts):
        print("  %-18s %d" % (k, counts[k]))
    print("\nChecks not run:")
    for n in ledger["checks_not_run"]:
        print("  - %s" % n)
    if ws:
        register_sources(ws, sources)
        write_ledger_to_graph(ws, ledger)
        register_targets(ws, _load_project(ws.root))
        print("\ngraph: %s" % ", ".join("%s %d" % (k, v)
                                        for k, v in sorted(ws.counts().items())))
    return 0


def cmd_graph(args):
    ws = Workspace.find(args.root)
    if args.json:
        print(json.dumps({"nodes": ws.nodes(), "edges": ws.edges(),
                          "stale": ws.stale_nodes()}, indent=2))
        return 0
    counts = ws.counts()
    stale = ws.stale_nodes()
    print("Authorship graph — %s" % ws.root)
    print("")
    print("| Node type | Count |")
    print("|---|---|")
    for k in sorted(counts):
        print("| `%s` | %d |" % (k, counts[k]))
    print("")
    rel = {}
    for e in ws.edges():
        rel[e["relation"]] = rel.get(e["relation"], 0) + 1
    print("| Edge relation | Count |")
    print("|---|---|")
    for k in sorted(rel):
        print("| `%s` | %d |" % (k, rel[k]))
    print("")
    print("%d node(s), %d edge(s), %d marked stale"
          % (sum(counts.values()), sum(rel.values()), len(stale)))
    if stale:
        print("\nStale:")
        for n, reason in sorted(stale.items()):
            print("  %s  %-22s %s" % (n[:8], ws.node_type(n) or "?", reason))
    return 0


def cmd_impact(args):
    ws = Workspace.find(args.root)
    path = Path(args.source)
    if not path.exists():
        raise WIError("WI_SOURCE_UNREADABLE", "%s not found" % path,
                      ["correct the path", "re-ingest the source"])
    raw = path.read_bytes()
    new_digest = blob_digest(raw)
    art_id = logical_id("source", path.name)
    if not ws.node_type(art_id):
        raise WIError("WI_SOURCE_VERSION_MISSING",
                      "%s has never been ingested" % path.name,
                      ["run `wi ingest %s` first" % path])

    versions = [n["logical_id"] for n in ws.nodes("source.version")
                if (ws.payload(n["logical_id"]) or {}).get("artifact") == art_id]
    new_version = logical_id("source_version", path.name, new_digest)
    prior = [v for v in versions if v != new_version]

    if new_version in versions and not args.force:
        print("%s is unchanged since it was ingested (%s)."
              % (path.name, new_digest[:19]))
        print("Nothing downstream is affected.")
        return 0

    old_text = None
    for v in prior:
        pay = ws.payload(v) or {}
        try:
            old_text = nfc(ws.get_blob(pay["blob_digest"]).decode("utf-8", "replace"))
            break
        except Exception:
            continue
    new_text = nfc(raw.decode("utf-8", "replace"))
    ranges = changed_byte_ranges(old_text, new_text) if old_text is not None else None

    impact = compute_impact(ws, art_id, prior[0] if prior else None,
                            new_version, ranges)
    plan = repair_plan(impact)

    if args.json:
        print(json.dumps({"impact": impact, "repair": plan}, indent=2))
        return 0

    print("Source changed: %s" % path.name)
    print("  was  %s" % (prior[0][:8] if prior else "(no prior version)"))
    print("  now  %s  %s" % (new_version[:8], new_digest[:19]))
    if ranges is not None:
        print("  %d changed byte range(s)" % len(ranges))
    print("")
    label = {"source.segment": "evidence anchor",
             "meaning.claim_atom": "claim atom",
             "structure.paragraph": "paragraph",
             "structure.work": "document",
             "release.target": "release target",
             "verification.result": "verification record"}
    print("Affected:")
    if impact["stale_total"] == 0:
        print("  nothing — every anchor lies outside the changed regions")
    for k in sorted(impact["stale"]):
        print("  %4d  %s" % (len(impact["stale"][k]), label.get(k, k)))
    print("")
    print("Unaffected:")
    print("  %4d  evidence anchor(s) provably outside the change"
          % len(impact["unaffected_anchors"]))
    safe_atoms = impact["totals"].get("meaning.claim_atom", 0) \
        - len(impact["stale"].get("meaning.claim_atom", []))
    print("  %4d  claim atom(s) still verified" % max(safe_atoms, 0))
    print("")
    print("Cheapest safe repair (cost %d):" % plan["cost"])
    for i, step in enumerate(plan["steps"], 1):
        print("  %d. %s" % (i, step["detail"]))
    if not plan["steps"]:
        print("  none required")

    if args.apply:
        for k, ids in impact["stale"].items():
            for n in ids:
                ws.mark_stale(new_digest, n, None, "source_version_changed")
        register_sources(ws, load_sources([str(path)]))
        ws.commit()
        print("\nMarked %d node(s) stale. `wi gate` will hold until they are repaired."
              % impact["stale_total"])
    else:
        print("\n(dry run — pass --apply to record the invalidation)")
    return 0


def cmd_diff(args):
    if not args.semantic:
        print("error: use --semantic; textual diff is what `diff` is for",
              file=sys.stderr)
        return 2
    a = atomize_document(args.before)
    b = atomize_document(args.after)
    result = semantic_diff(a, b)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    changed = result["changed"]
    material = [c for c in changed if c["proof_impact"].get("invalidates")]
    print("# Semantic diff")
    print("")
    print("%s -> %s" % (args.before, args.after))
    print("%d changed · %d added · %d removed · %d change(s) invalidate existing proof"
          % (len(changed), len(result["added"]), len(result["removed"]), len(material)))
    print("")
    for c in changed:
        print("BEFORE  %s" % _trunc(c["before"], 200))
        print("AFTER   %s" % _trunc(c["after"], 200))
        print("EFFECT  %s" % (", ".join(c["deltas"]) or "none detected"))
        inval = c["proof_impact"].get("invalidates") or []
        recheck = c["proof_impact"].get("requires_recheck") or []
        if inval:
            print("PROOF   existing support does not carry forward (%s)"
                  % ", ".join(inval))
        elif recheck:
            print("PROOF   re-check required (%s)" % ", ".join(recheck))
        else:
            print("PROOF   unaffected")
        print("")
    for a2 in result["added"]:
        print("ADDED   %s" % _trunc(a2["text"], 200))
    for r in result["removed"]:
        print("REMOVED %s" % _trunc(r["text"], 200))
    if result["added"] or result["removed"]:
        print("")
    print(result["note"])
    return 0


def cmd_test(args):
    ws = Workspace.find_or_none(args.root)
    root = ws.root if ws else Path(args.root)
    project = _load_project(root)
    tests = project.get("tests") or []
    if args.tests:
        extra = load_yaml_file(args.tests)
        if isinstance(extra, dict):
            tests = extra.get("tests") or tests
            if isinstance(extra.get("concepts"), dict):
                project = dict(project, concepts=dict(
                    (project.get("concepts") or {}) if isinstance(
                        project.get("concepts"), dict) else {},
                    **extra["concepts"]))
        else:
            tests = extra or tests
    ledgers = _all_ledgers(ws) if ws else []
    if args.ledger:
        ledgers = [json.loads(Path(l).read_text(encoding="utf-8")) for l in args.ledger]

    if not tests:
        print("no writing tests defined in %s" % (root / PROJECT_FILE))
        print("add a `tests:` block, or pass --tests <file>")
        return 0

    results = run_writing_tests(root, project, tests, ledgers)
    failed = [r for r in results if r["result"] == "fail"]
    unavailable = [r for r in results if r["basis"] == "unavailable"]
    # An unimplemented assertion is unavailable, never a pass and never a fail.
    # Reporting it either way would be the exact confusion Law C forbids.

    if args.json:
        print(json.dumps({"results": results}, indent=2, ensure_ascii=False))
        return 1 if failed else 0

    print("# Writing tests")
    print("")
    for r in results:
        mark = {"pass": "PASS", "fail": "FAIL"}[r["result"]]
        if r["basis"] == "unavailable":
            mark = "SKIP"
        print("%-5s %-38s %s" % (mark, r["id"], r["detail"]))
        for m in r["members"][:10]:
            print("          %s" % m)
        if len(r["members"]) > 10:
            print("          ... and %d more" % (len(r["members"]) - 10))
    print("")
    passed = [r for r in results
              if r["result"] == "pass" and r["basis"] != "unavailable"]
    print("%d passed · %d failed · %d unavailable"
          % (len(passed), len(failed), len(unavailable)))
    if not ledgers:
        print("\nNote: no claim ledger was available, so evidence-based tests ran")
        print("against nothing. Run `wi atomize` and `wi anchor` first.")
    return 1 if failed else 0


def cmd_explain(args):
    ws = Workspace.find_or_none(args.root)
    target = args.target
    line = None
    if ":" in target and not Path(target).exists():
        target, _, lno = target.rpartition(":")
        line = int(lno)
    ledger = None
    if ws:
        cand = _ledger_path(ws, target)
        if cand.exists():
            ledger = json.loads(cand.read_text(encoding="utf-8"))
    if ledger is None:
        ledger = atomize_document(target)
        print("(no anchored ledger in the workspace; showing structure only)\n")

    atoms = [a for a in ledger["atoms"] if line is None or a["line"] == line]
    if not atoms:
        near = sorted(ledger["atoms"], key=lambda a: abs(a["line"] - (line or 0)))[:3]
        print("No claim atom at %s:%s." % (target, line))
        if near:
            print("Nearest: %s" % ", ".join("line %d" % a["line"] for a in near))
        return 0

    anchors = {a["anchor_id"]: a for a in ledger.get("anchors", [])}
    srcs = {s["logical_id"]: s for s in ledger.get("sources", [])}
    print("%s%s" % (target, ":%d" % line if line else ""))
    print("")
    for a in atoms:
        print("%s  %s" % (a["id"], a["class"]))
        print("  \"%s\"" % _trunc(a["text"], 160))
        print("  status   %s" % a["status"])
        print("  realm    %s" % a["realm"])
        prop = a["proposition"]
        if prop["quantities"]:
            print("  quantity %s" % ", ".join(
                "%s %s" % (_fmt(q["value"]), q["unit"] or "(unitless)")
                for q in prop["quantities"]))
        if prop["temporal_scope"]:
            ts = prop["temporal_scope"]
            print("  when     %s to %s" % (ts.get("start"), ts.get("end") or "open"))
        print("  modality %s%s" % (prop["modality"], " (hedged)" if prop["hedged"] else ""))
        if a["anchors"]:
            print("  anchors:")
            for aid in a["anchors"]:
                an = anchors.get(aid)
                if not an:
                    continue
                s = srcs.get(an["source_logical_id"], {})
                print("    %s  bytes %d-%d  %s" % (s.get("title", "?"),
                                                   an["start_byte"], an["end_byte"],
                                                   an["quote_digest"][:19]))
                print("      > %s" % _trunc(an["quote"], 120))
        if a["checks"]:
            print("  checks:")
            for c in a["checks"]:
                print("    %-22s %-10s %s" % (c["check"], c["result"], c["basis"]))
        for n in a["notes"]:
            print("  note     %s" % n)
        if ws:
            deps = ws.dependents(a["logical_id"])
            if deps:
                kinds = {}
                for d in deps:
                    t = ws.node_type(d) or "?"
                    kinds[t] = kinds.get(t, 0) + 1
                print("  used by  %s" % ", ".join("%d %s" % (v, k)
                                                  for k, v in sorted(kinds.items())))
        print("")
    print("Support is verified within the sources you supplied. It does not mean")
    print("the sources are correct.")
    return 0


def cmd_bundle(args):
    ws = Workspace.find(args.root)
    project = _load_project(ws.root)
    ledgers = _all_ledgers(ws)
    if not ledgers:
        raise WIError("WI_BUILD_FAILED", "no claim ledger in this workspace",
                      ["run `wi atomize` then `wi anchor` before bundling"])
    stale = ws.stale_nodes()
    verdict = gate_atoms(ledgers, mode=args.mode, stale=stale)
    if verdict["decision"] == "BLOCK" and not args.allow_block:
        print(render_atom_gate(verdict, ledgers, stale))
        print("\nRefusing to build a bundle at BLOCK. Pass --allow-block to record")
        print("the blocked state in the manifest instead of resolving it.")
        return 2

    policy = {"evidence": project.get("evidence"), "release": project.get("release"),
              "privacy": project.get("privacy"), "mode": args.mode}
    manifest, out = build_bundle(ws, args.out, project, policy, args.artifact or [],
                                 ledgers, verdict, profile=args.profile)
    size = out.stat().st_size
    print("built %s (%d bytes, profile: %s)" % (out, size, args.profile))
    print("  verdict          %s" % manifest["gate"]["verdict"])
    print("  claim atoms      %d required, %d permitted"
          % (manifest["counts"]["claim_atoms_required"],
             manifest["counts"]["claim_atoms_permitted"]))
    print("  graph            %d nodes, %d edges"
          % (manifest["counts"]["nodes"], manifest["counts"]["edges"]))
    print("  stale nodes      %d" % manifest["counts"]["stale_nodes"])
    print("  proof closure    %s" % manifest["project_state_digest"][:23])
    print("  sha256           sha256:%s" % sha256_hex(out.read_bytes()))
    if args.profile == "hash-only":
        print("\nThis is a hash-only bundle. A reviewer who does not already hold the")
        print("sources cannot inspect them from it, and the manifest says so.")
    print("\nVerify anywhere: python3 wi.py verify-release %s" % out)
    return 0


def cmd_verify_release(args):
    result = verify_bundle(args.bundle)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 2
    m = result["manifest"] or {}
    print("# Release verification: %s" % Path(args.bundle).name)
    print("")
    if m:
        print("project   %s" % m.get("project_id"))
        print("built by  %s %s" % (m.get("core", {}).get("name"),
                                   m.get("core", {}).get("version")))
        print("profile   %s" % m.get("profile"))
        print("verdict   %s" % m.get("gate", {}).get("verdict"))
        print("")
    for c in result["checks"]:
        print("%-5s %-28s %s" % (c["result"], c["check"], c["detail"]))
    print("")
    if m.get("checks_not_run"):
        print("Checks the producer states were NOT run:")
        for n in m["checks_not_run"]:
            print("  - %s" % n)
        print("")
    if result["ok"]:
        print("RELEASE MANIFEST VALID")
        print("")
        print("Verified by recomputing digests. No model, no network, no trust in")
        print("whoever produced this bundle. It does not mean the sources are correct.")
        return 0
    print("RELEASE MANIFEST INVALID — %s" % "WI_RELEASE_TAMPERED")
    print("Do not publish or rely on this artifact until the failure is explained.")
    return 2


def cmd_doctor(args):
    caps = capabilities(args.root)
    if args.json:
        print(json.dumps(caps, indent=2))
        return 0
    print("Writing Intelligence %s — capability report" % caps["core"])
    print("")
    print("python            %s" % caps["python"])
    print("schema            %s" % caps["schema_version"])
    print("canonicalization  %s" % caps["canonicalization"])
    c = caps["capabilities"]
    print("workspace         %s" % (c["workspace_root"] or "none found"))
    print("network           %s" % ("enabled" if c["network"] else "disabled"))
    print("")
    print("Deterministic checks available (%d):" % len(c["deterministic_checks"]))
    for k in c["deterministic_checks"]:
        print("  %s" % k)
    print("")
    print("Evidence anchor types available: %s" % ", ".join(c["anchor_types"]))
    print("")
    print("Not available here — and therefore never reported as done:")
    for k, v in sorted(caps["unavailable"].items()):
        print("  %-22s %s" % (k, v))
    print("")
    print("This report is Law C as protocol: a surface states what it cannot do")
    print("rather than degrading quietly into looking like it did it.")
    return 0


def render_atom_gate(result, ledgers, stale=None):
    L = []
    stale = stale or {}
    counts, total_atoms, sources = {}, 0, 0
    for led in ledgers:
        total_atoms += len(led["atoms"])
        sources += led.get("sources_readable", 0)
        for a in led["atoms"]:
            counts[a["status"]] = counts.get(a["status"], 0) + 1

    L.append("# Release gate: %s" % result["decision"])
    L.append("")
    L.append("Evidence mode: `%s` · %d claim atom(s) · %d readable source(s) · %d stale node(s)"
             % (result["mode"], total_atoms, sources, len(stale)))
    L.append("")
    L.append("Checks run: anchor integrity · quotation · numeric · date · entity · "
             "citation resolution.")
    for n in (ledgers[0].get("checks_not_run") if ledgers else []) or []:
        L.append("Not run: %s" % n)
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
        for a, reason in items:
            L.append("**%s** — %s" % (a["id"], reason))
            L.append("")
            L.append("> %s" % _trunc(a["text"], 300))
            L.append("")
            for n in a["notes"]:
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
        L.append("Every claim atom is supported *within the sources you supplied*, ")
        L.append("marked as your own assertion, or classified as reasoning rather ")
        L.append("than fact. It does not mean the sources are correct.")
    return "\n".join(L)


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="wi",
        description="Writing Intelligence %s — deterministic authorship checks. "
                    "Offline, stdlib only, no model." % VERSION)
    p.add_argument("--version", action="version", version="wi %s" % VERSION)
    p.add_argument("--offline", action="store_true",
                   help="assert no network is used; this build never opens one")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("preserve",
                        help="snapshot a file before editing (Law B)")
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
    sp.add_argument("--mode", default=None,
                    choices=["light", "standard", "strict", "regulated"],
                    help="default: the project's evidence.default_mode, "
                         "or `standard` if there is no project file")
    sp.add_argument("--out")
    sp.add_argument("--exit-code", action="store_true",
                    help="exit 0/1/2 for RELEASE/HOLD/BLOCK (for CI and git hooks)")
    sp.add_argument("--root", default=".",
                    help="workspace root, for staleness (v5 atom ledgers)")
    sp.set_defaults(func=cmd_gate)

    # ---------------------------------------------------------------- v5 ---
    def root_arg(sp):
        sp.add_argument("--root", default=".",
                        help="workspace root (default: search upward from here)")
        return sp

    sp = sub.add_parser("init", help="create a .wi workspace and project file")
    sp.add_argument("dir", nargs="?", default=".")
    sp.add_argument("--title")
    sp.add_argument("--mode", default="standard",
                    choices=["off", "light", "standard", "strict", "regulated"])
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_init)

    sp = root_arg(sub.add_parser("ingest", help="content-address sources into the workspace"))
    sp.add_argument("paths", nargs="+")
    sp.set_defaults(func=cmd_ingest)

    sp = root_arg(sub.add_parser("atomize", help="split sentences into claim atoms"))
    sp.add_argument("document")
    sp.add_argument("--out")
    sp.set_defaults(func=cmd_atomize)

    sp = root_arg(sub.add_parser("anchor", help="bind atoms to evidence anchors and check them"))
    sp.add_argument("ledger")
    sp.add_argument("sources", nargs="+")
    sp.add_argument("--out")
    sp.add_argument("--tolerance", type=float, default=0.0,
                    help="relative numeric tolerance, e.g. 0.01 for 1%%")
    sp.set_defaults(func=cmd_anchor)

    sp = root_arg(sub.add_parser("graph", help="show the authorship graph"))
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_graph)

    sp = root_arg(sub.add_parser("impact", help="minimum repair frontier for a changed source"))
    sp.add_argument("source")
    sp.add_argument("--apply", action="store_true",
                    help="record the invalidation instead of only reporting it")
    sp.add_argument("--force", action="store_true")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_impact)

    sp = sub.add_parser("diff", help="classify what a rewrite did to meaning")
    sp.add_argument("before")
    sp.add_argument("after")
    sp.add_argument("--semantic", action="store_true", required=False)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_diff)

    sp = root_arg(sub.add_parser("test", help="run writing tests and concept contracts"))
    sp.add_argument("--tests")
    sp.add_argument("--ledger", action="append")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_test)

    sp = root_arg(sub.add_parser("explain", help="why is this sentence here (path[:line])"))
    sp.add_argument("target")
    sp.set_defaults(func=cmd_explain)

    sp = root_arg(sub.add_parser("bundle", help="build a .wiab proof-carrying release"))
    sp.add_argument("out")
    sp.add_argument("--artifact", action="append",
                    help="a built output to seal into the bundle (repeatable)")
    sp.add_argument("--profile", default="hash-only",
                    choices=["full", "hash-only", "redacted"])
    sp.add_argument("--mode", default="strict",
                    choices=["light", "standard", "strict", "regulated"])
    sp.add_argument("--allow-block", action="store_true")
    sp.set_defaults(func=cmd_bundle)

    sp = sub.add_parser("verify-release", help="verify a .wiab offline, with no model")
    sp.add_argument("bundle")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_verify_release)

    sp = root_arg(sub.add_parser("doctor", help="what this surface can and cannot do"))
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_doctor)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except WIError as exc:
        print(exc.render(), file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `wi graph | head` is a normal thing to do. A traceback here would be
        # the tool complaining about the user's shell.
        try:
            sys.stdout.close()
        finally:
            os._exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
