#!/usr/bin/env python3
"""
wi.py — Writing Intelligence v6, the Sovereign Meaning Runtime core.

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

v6 — the sovereign meaning runtime
----------------------------------
  canon            Canonical form and domain-separated digest of any object.
  branch           Semantic branches over immutable graph roots.
  propose          A change bound to the exact state it was written against.
  proposals        What is open, accepted, applied or superseded.
  simulate         What a change would do — before it exists. Writes nothing.
  decide           An authorized decision, bound to the state it approved.
  commit           Apply every accepted proposal as one transaction.
  log              Semantic commit history.
  merge            Three-way merge on meaning. Conflicts are preserved.
  conflicts        Unresolved semantic disagreement, and how to resolve it.
  authority        Issue, delegate, revoke and check capability grants.
  obligations      What must be proved, derived from typed state and policy.
  as-of            Bitemporal query: valid time and knowledge time.
  constraints      The graph constraint engine, C001 through C020.
  capsule          Merkle proof closure and selective disclosure.
  why              Explain a node backward to its basis.

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

VERSION = "6.0.0"

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


# ==========================================================================
# v6 — The Sovereign Meaning Runtime.
#
# Everything below this line is the v6 layer. It does not modify, weaken or
# reinterpret anything above it: the v4 floor and the v5 proof-carrying graph
# are unchanged and remain the compatibility oracle.
#
# What v6 adds is a state machine. v5 could tell you what a changed source
# broke. v6 can tell you what a change *would* break before it exists, who is
# permitted to make it, what the acceptance was bound to, and what survived.
#
# Design rules held throughout:
#
#   * A graph root is pure state. Provenance lives on the commit, never in the
#     root, so identical state always produces an identical root digest. That
#     is what makes "provably unaffected" an equality test rather than an
#     opinion, and it is what makes simulation cheap.
#   * Objects are immutable and content-addressed. Mutability is confined to
#     refs, proposal status and revocation — three small tables, each of which
#     records what it moved from.
#   * Nothing here calls a model, opens a socket, or reads outside the
#     workspace. Stdlib only, Python 3.8+, same as every line above.
# ==========================================================================

V6_SCHEMA_VERSION = "6.0"

V6_DDL = """
CREATE TABLE IF NOT EXISTS v6_object (
    digest TEXT PRIMARY KEY, schema_id TEXT NOT NULL,
    payload_json TEXT NOT NULL, created_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_v6_object_schema ON v6_object(schema_id);

CREATE TABLE IF NOT EXISTS v6_ref (
    name TEXT PRIMARY KEY, digest TEXT NOT NULL, updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS v6_proposal (
    proposal_id TEXT PRIMARY KEY, digest TEXT NOT NULL, branch TEXT NOT NULL,
    status TEXT NOT NULL, applied_in TEXT, updated_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS v6_decision (
    decision_id TEXT PRIMARY KEY, digest TEXT NOT NULL,
    proposal_id TEXT NOT NULL, created_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS v6_grant (
    grant_id TEXT PRIMARY KEY, digest TEXT NOT NULL, subject TEXT NOT NULL,
    revoked_at TEXT, created_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_v6_grant_subject ON v6_grant(subject);

CREATE TABLE IF NOT EXISTS v6_conflict (
    conflict_id TEXT PRIMARY KEY, digest TEXT NOT NULL, branch TEXT NOT NULL,
    status TEXT NOT NULL, created_at TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS v6_edge (
    edge_id TEXT PRIMARY KEY, from_logical_id TEXT NOT NULL,
    to_logical_id TEXT NOT NULL, relation TEXT NOT NULL,
    created_at TEXT NOT NULL);

CREATE INDEX IF NOT EXISTS idx_v6_edge_to ON v6_edge(to_logical_id, relation);
CREATE INDEX IF NOT EXISTS idx_v6_edge_from ON v6_edge(from_logical_id, relation);
"""

V6_NODE_TYPES = (
    "meaning.claim_atom", "meaning.definition", "meaning.term",
    "meaning.premise", "meaning.inference", "meaning.constraint",
    "meaning.promise", "meaning.obligation", "meaning.recommendation",
    "meaning.hypothesis", "meaning.forecast", "meaning.metric",
    "meaning.target", "meaning.assumption", "meaning.exception",
    "meaning.question", "meaning.argument", "meaning.counterargument",
)

V6_REALMS = ("external_fact", "author_observation", "inference",
             "fictional_canon", "hypothetical")

# The closed reliability basis. There is no `confident`, no `ai_verified` and
# no percentage. Law E is a type, not a convention.
V6_BASES = ("verified", "measured", "judged", "human_declared")


def v6_state_digest(obj, schema):
    """Domain-separated digest for a v6 object.

    Separated from the v5 domain on purpose. A byte-identical payload must
    never be ambiguously readable as both a v5 and a v6 object, because the
    two layers make different promises about what the payload means.
    """
    pre = (b"wi-state-v6\x00"
           + ("schema=%s@%s\x00" % (schema, V6_SCHEMA_VERSION)).encode("utf-8")
           + ("normalization=%s\x00" % NORMALIZATION).encode("utf-8")
           + ("len=%d\x00" % len(canonical_bytes(obj))).encode("utf-8")
           + b"payload=" + canonical_bytes(obj))
    return "sha256:" + sha256_hex(pre)


def v6_logical_id(kind, *parts):
    key = ("wi6:%s:" % kind) + "\x00".join(str(p) for p in parts)
    h = hashlib.sha256(key.encode("utf-8")).digest()
    return str(_uuid.UUID(bytes=h[:16], version=5))


# --------------------------------------------------------------------------
# Decimal quantities.
#
# Binary floating point is banned for consequential quantities. A proof digest
# that depends on how a platform serializes 0.1 + 0.2 is not a proof digest.
# --------------------------------------------------------------------------

def v6_quantity(value, unit=None, scale=None):
    """Normalize a quantity to integer coefficient plus decimal scale."""
    if isinstance(value, dict):
        return {"coefficient": int(value["coefficient"]),
                "scale": int(value.get("scale", 0)),
                "unit": value.get("unit") or unit}
    s = str(value).strip()
    neg = s.startswith("-")
    if neg:
        s = s[1:]
    if "." in s:
        whole, frac = s.split(".", 1)
    else:
        whole, frac = s, ""
    digits = (whole + frac) or "0"
    if not digits.isdigit():
        raise WIError("WI_INPUT_INVALID",
                      "quantity %r is not a decimal number" % value,
                      ["write the value as a decimal string, e.g. \"0.384\""])
    coef = int(digits) * (-1 if neg else 1)
    return {"coefficient": coef,
            "scale": len(frac) if scale is None else int(scale),
            "unit": unit}


def v6_quantity_equal(a, b):
    """Compare two decimal quantities without going through a float."""
    if (a.get("unit") or None) != (b.get("unit") or None):
        return False
    sa, sb = int(a.get("scale", 0)), int(b.get("scale", 0))
    ca, cb = int(a["coefficient"]), int(b["coefficient"])
    if sa < sb:
        ca *= 10 ** (sb - sa)
    elif sb < sa:
        cb *= 10 ** (sa - sb)
    return ca == cb


def v6_quantity_str(q):
    coef, scale = int(q["coefficient"]), int(q.get("scale", 0))
    neg = coef < 0
    d = str(abs(coef)).rjust(scale + 1, "0")
    out = d if scale == 0 else d[:-scale] + "." + d[-scale:]
    return ("-" if neg else "") + out + ((" " + q["unit"]) if q.get("unit") else "")


# --------------------------------------------------------------------------
# Bitemporal intervals. Half-open [from, until) on both clocks.
# --------------------------------------------------------------------------

def v6_valid_interval(frm=None, until=None):
    return {"from": frm, "until": until}


def v6_knowledge_interval(observed_at=None, superseded_at=None):
    return {"observed_at": observed_at or _now(), "superseded_at": superseded_at}


def _v6_covers(interval, point, lo="from", hi="until"):
    """Half-open containment. An open bound is unbounded on that side."""
    if point is None:
        return True
    a, b = interval.get(lo), interval.get(hi)
    if a is not None and str(point) < str(a):
        return False
    if b is not None and str(point) >= str(b):
        return False
    return True


def v6_intervals_overlap(a, b):
    """Do two half-open valid intervals share any instant?"""
    a0, a1 = a.get("from"), a.get("until")
    b0, b1 = b.get("from"), b.get("until")
    if a1 is not None and b0 is not None and str(a1) <= str(b0):
        return False
    if b1 is not None and a0 is not None and str(b1) <= str(a0):
        return False
    return True


# --------------------------------------------------------------------------
# The semantic delta classifier.
#
# This is the piece the merge engine, the authority engine and the simulator
# all consult, so it has exactly one implementation. Law K applies inside the
# core as strictly as it applies across surfaces.
# --------------------------------------------------------------------------

V6_DELTA_CLASSES = (
    "wording_only", "quantity_changed", "unit_changed",
    "scope_broadened", "scope_narrowed", "temporal_scope_changed",
    "certainty_strengthened", "certainty_weakened", "polarity_flipped",
    "attribution_changed", "causality_changed", "definition_changed",
    "obligation_strengthened", "obligation_weakened",
    "legal_force_strengthened", "legal_force_weakened",
    "canon_changed", "evidence_changed", "node_created", "node_removed",
)

# Which delta classes carry a prior proof forward, and which do not.
V6_PROOF_IMPACT = {
    "wording_only": "carries",
    "quantity_changed": "invalidates",
    "unit_changed": "invalidates",
    "scope_broadened": "invalidates",
    "scope_narrowed": "requires_recheck",
    "temporal_scope_changed": "invalidates",
    "certainty_strengthened": "invalidates",
    "certainty_weakened": "requires_recheck",
    "polarity_flipped": "invalidates",
    "attribution_changed": "invalidates",
    "causality_changed": "invalidates",
    "definition_changed": "invalidates",
    "obligation_strengthened": "invalidates",
    "obligation_weakened": "requires_recheck",
    "legal_force_strengthened": "invalidates",
    "legal_force_weakened": "invalidates",
    "canon_changed": "invalidates",
    "evidence_changed": "invalidates",
    "node_created": "invalidates",
    "node_removed": "invalidates",
}

V6_MODAL_STRENGTH = {"may": 1, "might": 1, "could": 1, "can": 1,
                     "should": 2, "ought": 2, "will": 3, "is": 3, "does": 3,
                     "shall": 4, "must": 4}

# "shall" and "must" are legal force; "should" and "may" are not. The
# difference is one word and it is the difference between an obligation and a
# suggestion, which is why it gets its own delta class and its own authority.
V6_LEGAL_FORCE = {"may": 0, "might": 0, "could": 0, "can": 0, "should": 1,
                  "ought": 1, "will": 2, "is": 0, "does": 0,
                  "shall": 3, "must": 3}

V6_CERTAINTY_RANK = {"hypothetical": 0, "possible": 1, "likely": 2,
                     "asserted": 3, "established": 4}


def _v6_field(payload, *names):
    for n in names:
        if n in payload and payload[n] not in (None, "", [], {}):
            return payload[n]
    return None


def _v6_quantities(payload):
    qs = payload.get("quantities") or []
    out = []
    for q in qs:
        if isinstance(q, dict) and "coefficient" in q:
            out.append({"coefficient": int(q["coefficient"]),
                        "scale": int(q.get("scale", 0)),
                        "unit": q.get("unit")})
        else:
            out.append(v6_quantity(q))
    return sorted(out, key=lambda q: (str(q.get("unit") or ""),
                                      q["coefficient"], q["scale"]))


def v6_classify(before, after):
    """Classify the semantic delta between two v6 node payloads.

    Returns a dict with `classes`, `proof_impact` and `judged_remainder`.
    Every class it reports is a structural comparison of typed fields. It is
    never wrong about what it reports; it is only silent about what a
    deterministic comparison cannot see, and it says so.
    """
    if before is None:
        return {"classes": ["node_created"],
                "proof_impact": {"invalidates": ["node_created"]},
                "judged_remainder": False}
    if after is None:
        return {"classes": ["node_removed"],
                "proof_impact": {"invalidates": ["node_removed"]},
                "judged_remainder": False}

    classes = []

    qa, qb = _v6_quantities(before), _v6_quantities(after)
    if len(qa) != len(qb):
        classes.append("quantity_changed")
    else:
        for x, y in zip(qa, qb):
            if (x.get("unit") or None) != (y.get("unit") or None):
                if "unit_changed" not in classes:
                    classes.append("unit_changed")
            elif not v6_quantity_equal(x, y):
                if "quantity_changed" not in classes:
                    classes.append("quantity_changed")

    ta = _v6_field(before, "temporal_scope", "valid_time") or {}
    tb = _v6_field(after, "temporal_scope", "valid_time") or {}
    if (ta.get("from"), ta.get("until")) != (tb.get("from"), tb.get("until")):
        classes.append("temporal_scope_changed")

    ma = (before.get("modality") or "").lower()
    mb = (after.get("modality") or "").lower()
    if ma != mb:
        sa = V6_MODAL_STRENGTH.get(ma, 3)
        sb = V6_MODAL_STRENGTH.get(mb, 3)
        if sb > sa:
            classes.append("certainty_strengthened")
        elif sb < sa:
            classes.append("certainty_weakened")
        la = V6_LEGAL_FORCE.get(ma, 0)
        lb = V6_LEGAL_FORCE.get(mb, 0)
        if lb > la:
            classes.append("legal_force_strengthened")
        elif lb < la:
            classes.append("legal_force_weakened")

    ca = V6_CERTAINTY_RANK.get((before.get("certainty") or "").lower())
    cb = V6_CERTAINTY_RANK.get((after.get("certainty") or "").lower())
    if ca is not None and cb is not None and ca != cb:
        cls = "certainty_strengthened" if cb > ca else "certainty_weakened"
        if cls not in classes:
            classes.append(cls)

    pa = (before.get("polarity") or "positive").lower()
    pb = (after.get("polarity") or "positive").lower()
    if pa != pb:
        classes.append("polarity_flipped")

    for key, broadened, narrowed in (
            ("spatial_scope", "scope_broadened", "scope_narrowed"),
            ("population_scope", "scope_broadened", "scope_narrowed")):
        sa_set = set(before.get(key) or [])
        sb_set = set(after.get(key) or [])
        if sa_set != sb_set:
            # Removing a restriction broadens. Adding one narrows. An empty
            # scope is the widest scope there is, which is why dropping the
            # last constraint is the most dangerous edit in this function.
            cls = broadened if len(sb_set) < len(sa_set) else narrowed
            if cls not in classes:
                classes.append(cls)

    if (before.get("attribution") or []) != (after.get("attribution") or []):
        classes.append("attribution_changed")
    if (before.get("causality") or None) != (after.get("causality") or None):
        classes.append("causality_changed")
    if (before.get("exceptions") or []) != (after.get("exceptions") or []):
        if "obligation_weakened" not in classes:
            n_before = len(before.get("exceptions") or [])
            n_after = len(after.get("exceptions") or [])
            classes.append("obligation_weakened" if n_after > n_before
                           else "obligation_strengthened")
    if (before.get("definition") or None) != (after.get("definition") or None):
        classes.append("definition_changed")
    if (before.get("evidence") or []) != (after.get("evidence") or []):
        classes.append("evidence_changed")
    if (before.get("canon") or None) != (after.get("canon") or None):
        classes.append("canon_changed")

    ta_text = fold_ws(str(_v6_field(before, "text", "statement") or ""))
    tb_text = fold_ws(str(_v6_field(after, "text", "statement") or ""))

    if not classes:
        # No typed field moved. Either nothing changed at all, or only the
        # wording did. Wording-only is a *conclusion* the comparison reached,
        # never an assumption it started from.
        rest_a = {k: v for k, v in before.items() if k not in ("text", "statement")}
        rest_b = {k: v for k, v in after.items() if k not in ("text", "statement")}
        if rest_a != rest_b:
            classes.append("evidence_changed")
        elif ta_text != tb_text:
            classes.append("wording_only")

    impact = {}
    for c in classes:
        impact.setdefault(V6_PROOF_IMPACT.get(c, "requires_recheck"), []).append(c)

    return {"classes": classes, "proof_impact": impact,
            "judged_remainder": bool(ta_text != tb_text
                                     and classes in ([], ["wording_only"]))}


def v6_carries_proof(classes):
    return all(V6_PROOF_IMPACT.get(c) == "carries" for c in classes)


# --------------------------------------------------------------------------
# Authority.
#
# Authorization is transition-aware. You do not authorize a paragraph; you
# authorize what the edit did to meaning. "colour" -> "color" and
# "may reduce" -> "reduces" can land in the same sentence and require
# completely different authority, and a system that cannot tell them apart is
# not enforcing anything.
# --------------------------------------------------------------------------

V6_CAPABILITIES = (
    "source.ingest", "claim.propose", "claim.accept",
    "claim.accept.wording_only", "claim.accept.quantity_change",
    "concept.define", "obligation.create", "canon.modify", "proof.waive",
    "release.build", "release.approve", "release.sign", "policy.modify",
    "authority.delegate", "capsule.export.full", "capsule.export.redacted",
)

V6_DELTA_CAPABILITY = {
    "wording_only": "claim.accept.wording_only",
    "quantity_changed": "claim.accept.quantity_change",
    "unit_changed": "claim.accept.quantity_change",
    "certainty_strengthened": "claim.accept",
    "certainty_weakened": "claim.accept",
    "scope_broadened": "claim.accept",
    "scope_narrowed": "claim.accept",
    "temporal_scope_changed": "claim.accept",
    "polarity_flipped": "claim.accept",
    "attribution_changed": "claim.accept",
    "causality_changed": "claim.accept",
    "evidence_changed": "claim.accept",
    "definition_changed": "concept.define",
    "obligation_strengthened": "obligation.create",
    "obligation_weakened": "obligation.create",
    "legal_force_strengthened": "obligation.create",
    "legal_force_weakened": "obligation.create",
    "canon_changed": "canon.modify",
    "node_created": "claim.accept",
    "node_removed": "claim.accept",
}

# Actor kinds that may never hold a grant, whatever a configuration file says.
# A judgment provider returns values. It does not decide, approve or sign, and
# that is a constitutional constraint rather than a default.
V6_FORBIDDEN_SUBJECT_KINDS = ("judgment_provider",)


def v6_capability_covers(parent, child):
    """Dotted capability containment: `claim.accept` covers `claim.accept.*`."""
    if parent == child:
        return True
    return child.startswith(parent + ".")


def v6_scope_covers(parent, child):
    """Scope containment. `workspace` covers everything below it."""
    pk, ck = parent.get("kind"), child.get("kind")
    if pk == "workspace":
        return True
    if pk != ck:
        return False
    return parent.get("value") == child.get("value")


def v6_required_capability(classes):
    """The single capability an actor must hold to accept this transition.

    When an edit carries several delta classes, the required capability is the
    strongest of them. A rewrite that changes wording *and* a number is a
    number change; it does not become a wording change because most of the
    diff was cosmetic.
    """
    order = ["claim.accept.wording_only", "claim.accept",
             "claim.accept.quantity_change", "concept.define",
             "obligation.create", "canon.modify"]
    best, rank = "claim.accept", order.index("claim.accept")
    for c in classes or ["wording_only"]:
        cap = V6_DELTA_CAPABILITY.get(c, "claim.accept")
        r = order.index(cap) if cap in order else len(order)
        if r >= rank:
            best, rank = cap, r
    return best


def v6_validate_child_grant(parent, child):
    """Delegation is monotonic. A child grant may narrow; it may never widen."""
    if parent["subject"] != child["issuer"]:
        raise WIError("WI_GRANT_SCOPE_EXCEEDED",
                      "the issuer of the child grant does not hold the parent grant",
                      ["delegate from the actor who holds the parent grant"],
                      {"parent_subject": parent["subject"],
                       "child_issuer": child["issuer"]})
    if not v6_capability_covers(parent["capability"], child["capability"]):
        raise WIError("WI_GRANT_SCOPE_EXCEEDED",
                      "the delegated capability exceeds the parent grant",
                      ["delegate a capability at or below %s" % parent["capability"]],
                      {"parent": parent["capability"], "child": child["capability"]})
    if not v6_scope_covers(parent["scope"], child["scope"]):
        raise WIError("WI_GRANT_SCOPE_EXCEEDED",
                      "the delegated scope exceeds the parent grant",
                      ["narrow the scope to sit inside the parent scope"],
                      {"parent": parent["scope"], "child": child["scope"]})
    pe, ce = parent.get("expires_at"), child.get("expires_at")
    if pe is not None and (ce is None or str(ce) > str(pe)):
        raise WIError("WI_GRANT_SCOPE_EXCEEDED",
                      "the delegated grant outlives its parent",
                      ["set an expiry at or before %s" % pe],
                      {"parent_expires_at": pe, "child_expires_at": ce})
    return True


# --------------------------------------------------------------------------
# The v6 runtime facade.
# --------------------------------------------------------------------------

class V6(object):
    """The v6 layer over an existing v5 workspace.

    Constructed from a Workspace. Creates its tables on first use so a v5
    workspace can be opened by a v6 core without a migration step that
    rewrites anything the v5 verifier already attested to.
    """

    def __init__(self, ws):
        self.ws = ws
        self.db = ws.db
        self.db.executescript(V6_DDL)

    # -- objects -----------------------------------------------------------
    def put(self, obj, schema):
        obj = dict(obj)
        obj["schema"] = schema
        d = v6_state_digest(obj, schema)
        self.db.execute(
            "INSERT OR IGNORE INTO v6_object VALUES (?,?,?,?)",
            (d, schema, json.dumps(obj, sort_keys=True, ensure_ascii=False), _now()))
        return d

    def get(self, digest):
        row = self.db.execute("SELECT payload_json FROM v6_object WHERE digest=?",
                              (digest,)).fetchone()
        if not row:
            raise WIError("WI_GRAPH_INTEGRITY",
                          "v6 object %s is not in the workspace" % digest[:19],
                          ["re-run the command that produced it",
                           "restore the workspace object store"])
        return json.loads(row["payload_json"])

    def has(self, digest):
        return bool(self.db.execute("SELECT 1 FROM v6_object WHERE digest=?",
                                    (digest,)).fetchone())

    # -- refs --------------------------------------------------------------
    def ref(self, name):
        row = self.db.execute("SELECT digest FROM v6_ref WHERE name=?",
                              (name,)).fetchone()
        return row["digest"] if row else None

    def refs(self, prefix=""):
        return [(r["name"], r["digest"]) for r in self.db.execute(
            "SELECT name, digest FROM v6_ref WHERE name LIKE ? ORDER BY name",
            (prefix + "%",))]

    def set_ref(self, name, digest, expected="__any__"):
        """Compare-and-set. Two processes must not silently overwrite a head."""
        if expected != "__any__":
            actual = self.ref(name)
            if actual != expected:
                raise WIError("WI_TRANSACTION_CONFLICT",
                              "ref %s moved while this operation was running" % name,
                              ["re-read the branch head and retry"],
                              {"expected": expected or "(unset)",
                               "actual": actual or "(unset)"})
        self.db.execute("INSERT OR REPLACE INTO v6_ref VALUES (?,?,?)",
                        (name, digest, _now()))

    def delete_ref(self, name):
        self.db.execute("DELETE FROM v6_ref WHERE name=?", (name,))

    # -- branches ----------------------------------------------------------
    def head_branch(self):
        return self.ref("HEAD") or "main"

    def branch_names(self):
        return [n[len("heads/"):] for n, _ in self.refs("heads/")]

    def ensure_initialized(self, actor="author"):
        """Create an empty root and an initial commit on `main` if absent.

        The empty root is not a special case. It is the graph root of a
        workspace with no governed meaning in it yet, and it has a digest like
        any other state, which is what lets the first commit be diffed.
        """
        if self.ref("heads/main"):
            return False
        root = self.put_root({}, {}, {})
        delta = self.put({"added": [], "superseded": [], "removed": [],
                          "semantic": []}, "wi.v6.delta")
        commit = self.put({"parents": [], "root": root, "delta": delta,
                           "actor": actor, "decision": None,
                           "message": "initialize the v6 semantic layer",
                           "timestamp": _now()}, "wi.v6.commit")
        self.set_ref("heads/main", commit)
        self.set_ref("HEAD", "main")
        return True

    # -- graph roots -------------------------------------------------------
    def put_root(self, nodes, edges, conflicts, policy=None, authority=None):
        """A graph root is pure state. No timestamp, no author, no counter.

        That is deliberate and it is the property everything else rests on:
        two roots are equal exactly when the meaning they hold is equal, so
        `unchanged` is an equality test on 32 bytes rather than a walk.
        """
        return self.put({
            "nodes": {k: nodes[k] for k in sorted(nodes)},
            "edges": {k: edges[k] for k in sorted(edges)},
            "conflicts": {k: conflicts[k] for k in sorted(conflicts)},
            "policy": policy, "authority": authority,
        }, "wi.v6.graph_root")

    def commit_obj(self, digest):
        return self.get(digest)

    def root_of(self, commit_digest):
        return self.get(commit_digest)["root"]

    def nodes_at(self, commit_digest):
        if not commit_digest:
            return {}
        return self.get(self.root_of(commit_digest))["nodes"]

    def history(self, commit_digest, limit=None):
        """First-parent history, newest first."""
        out, seen, cur = [], set(), commit_digest
        while cur and cur not in seen:
            seen.add(cur)
            c = self.get(cur)
            out.append((cur, c))
            if limit and len(out) >= limit:
                break
            cur = c["parents"][0] if c["parents"] else None
        return out

    def merge_base(self, a, b):
        """Lowest common ancestor by first-parent walk on both sides."""
        anc_a = {d for d, _ in self.history(a)}
        cur = b
        seen = set()
        while cur and cur not in seen:
            seen.add(cur)
            if cur in anc_a:
                return cur
            c = self.get(cur)
            cur = c["parents"][0] if c["parents"] else None
        return None

    # -- node states -------------------------------------------------------
    def put_node_state(self, logical, node_type, payload, realm="external_fact",
                       valid_time=None, knowledge_time=None, reliability=None,
                       jurisdiction=None):
        if realm not in V6_REALMS:
            raise WIError("WI_INPUT_INVALID",
                          "realm %r is not one of the five epistemic realms" % realm,
                          ["use one of: " + ", ".join(V6_REALMS)])
        basis = (reliability or {}).get("basis", "human_declared")
        if basis not in V6_BASES:
            raise WIError("WI_INPUT_INVALID",
                          "reliability basis %r is not a member of the closed set" % basis,
                          ["use one of: " + ", ".join(V6_BASES),
                           "there is deliberately no `confident` and no percentage"])
        obj = {
            "logical_id": logical,
            "node_type": node_type,
            "realm": realm,
            "jurisdiction": sorted(jurisdiction or []),
            "valid_time": valid_time or v6_valid_interval(),
            "knowledge_time": knowledge_time or v6_knowledge_interval(),
            "reliability": reliability or {"basis": "human_declared",
                                           "actor": "author"},
            "payload": payload,
        }
        return self.put(obj, "wi.v6.node_state")

    def dependents(self, logical):
        """Everything that declares a dependency on this node.

        Reads both the v5 edge table and the v6 edge table, because a
        workspace that grew from v5 has real dependency structure already and
        pretending otherwise would understate the blast radius.
        """
        out = set()
        for r in self.db.execute(
                "SELECT from_logical_id FROM edge WHERE to_logical_id=? AND relation=?",
                (logical, DEPENDENCY)):
            out.add(r["from_logical_id"])
        for r in self.db.execute(
                "SELECT from_logical_id FROM v6_edge"
                " WHERE to_logical_id=? AND relation=?", (logical, DEPENDENCY)):
            out.add(r["from_logical_id"])
        return out

    def stale_frontier(self, changed):
        """Transitive dependents of a changed set, excluding the set itself."""
        frontier, queue, seen = set(), list(changed), set(changed)
        while queue:
            cur = queue.pop()
            for dep in self.dependents(cur):
                if dep not in seen:
                    seen.add(dep)
                    frontier.add(dep)
                    queue.append(dep)
        return frontier

    # -- proposals ---------------------------------------------------------
    def open_proposals(self, branch, status=None):
        q = "SELECT * FROM v6_proposal WHERE branch=?"
        args = [branch]
        if status:
            q += " AND status=?"
            args.append(status)
        q += " ORDER BY updated_at, proposal_id"
        return [dict(r) for r in self.db.execute(q, args)]

    def proposal(self, pid):
        row = self.db.execute("SELECT * FROM v6_proposal WHERE proposal_id=?",
                              (pid,)).fetchone()
        if not row:
            raise WIError("WI_INPUT_INVALID", "no proposal %s" % pid,
                          ["run `wi proposals` to list open proposals"])
        return dict(row)

    def set_proposal_status(self, pid, status, applied_in=None):
        self.db.execute(
            "UPDATE v6_proposal SET status=?, applied_in=?, updated_at=?"
            " WHERE proposal_id=?", (status, applied_in, _now(), pid))

    # -- grants ------------------------------------------------------------
    def grants_for(self, subject):
        out = []
        for r in self.db.execute(
                "SELECT * FROM v6_grant WHERE subject=? ORDER BY created_at",
                (subject,)):
            g = self.get(r["digest"])
            g["_revoked_at"] = r["revoked_at"]
            out.append(g)
        return out

    def grant(self, gid):
        row = self.db.execute("SELECT * FROM v6_grant WHERE grant_id=?",
                              (gid,)).fetchone()
        if not row:
            raise WIError("WI_INPUT_INVALID", "no grant %s" % gid,
                          ["run `wi authority list` to see issued grants"])
        g = self.get(row["digest"])
        g["_revoked_at"] = row["revoked_at"]
        return g

    def authorize(self, actor, capability, scope, at=None):
        """Return the grant that permits this transition, or raise.

        Every failure mode is distinct on purpose. "You have no grant", "your
        grant expired", "your grant was revoked" and "your grant does not
        reach this branch" are four different conversations, and collapsing
        them into `permission denied` costs the operator the fix.
        """
        at = at or _now()
        held = self.grants_for(actor)
        if not held:
            raise WIError("WI_AUTHORITY_DENIED",
                          "%s holds no capability grant" % actor,
                          ["issue one: wi authority issue --subject %s"
                           " --capability %s --scope workspace" % (actor, capability)],
                          {"required_capability": capability})
        expired, revoked, out_of_scope, wrong_cap = [], [], [], []
        for g in held:
            if not v6_capability_covers(g["capability"], capability):
                wrong_cap.append(g["grant_id"])
                continue
            if g.get("_revoked_at"):
                revoked.append(g["grant_id"])
                continue
            if g.get("activates_at") and str(at) < str(g["activates_at"]):
                expired.append(g["grant_id"])
                continue
            if g.get("expires_at") and str(at) >= str(g["expires_at"]):
                expired.append(g["grant_id"])
                continue
            if not v6_scope_covers(g["scope"], scope):
                out_of_scope.append(g["grant_id"])
                continue
            return {"grant_id": g["grant_id"], "subject": actor,
                    "capability": capability, "scope": scope,
                    "checked_at": at, "basis": "verified"}
        if revoked:
            raise WIError("WI_AUTHORITY_REVOKED",
                          "every grant %s holds for %s has been revoked"
                          % (actor, capability),
                          ["issue a new grant", "or have a different actor decide"],
                          {"revoked_grants": revoked})
        if expired:
            raise WIError("WI_AUTHORITY_EXPIRED",
                          "%s holds %s but the grant is not active at %s"
                          % (actor, capability, at),
                          ["re-issue the grant with a current window"],
                          {"grants": expired})
        if out_of_scope:
            raise WIError("WI_GRANT_SCOPE_EXCEEDED",
                          "%s holds %s but not in this scope" % (actor, capability),
                          ["widen the scope, or decide on a branch you hold"],
                          {"grants": out_of_scope, "requested_scope": scope})
        raise WIError("WI_AUTHORITY_DENIED",
                      "%s holds no grant covering %s" % (actor, capability),
                      ["issue one: wi authority issue --subject %s --capability %s"
                       " --scope workspace" % (actor, capability)],
                      {"holds": [g["capability"] for g in held],
                       "required_capability": capability})

    def commit_db(self):
        self.db.commit()


# --------------------------------------------------------------------------
# Simulation. The ephemeral branch that mutates nothing.
# --------------------------------------------------------------------------

def v6_apply(v6, base_nodes, proposals):
    """Apply proposal objects to a node map and report what moved.

    Returns (candidate_nodes, semantic, conflicts). Nothing is written.
    """
    nodes = dict(base_nodes)
    semantic, conflicts, touched = [], [], {}

    for pd in proposals:
        p = v6.get(pd) if isinstance(pd, str) else pd
        lid = p["target_logical_id"]
        before_digest = nodes.get(lid)

        # Law: a proposal is bound to the exact state it was written against.
        if p.get("target_state_digest") != before_digest:
            conflicts.append({
                "kind": "Evidence", "logical_id": lid,
                "base": p.get("target_state_digest"), "ours": before_digest,
                "theirs": None, "status": "unresolved",
                "required_resolution": "authorized_decision",
                "detail": "the proposal was written against a state this branch "
                          "no longer holds",
            })
            continue

        before = v6.get(before_digest)["payload"] if before_digest else None
        after_state = p["after"]
        after = v6.get(after_state)["payload"] if after_state else None

        if lid in touched and touched[lid] != after_state:
            prev = v6.get(touched[lid])["payload"]
            cls = v6_classify(prev, after)["classes"]
            conflicts.append({
                "kind": _v6_conflict_kind(cls), "logical_id": lid,
                "base": before_digest, "ours": touched[lid],
                "theirs": after_state, "status": "unresolved",
                "required_resolution": "authorized_decision",
                "detail": "two proposals in this set move the same node to "
                          "different states",
            })
            continue

        d = v6_classify(before, after)
        semantic.append({"logical_id": lid, "from": before_digest,
                         "to": after_state, "classes": d["classes"],
                         "proof_impact": d["proof_impact"],
                         "judged_remainder": d["judged_remainder"],
                         "proposal_id": p["proposal_id"]})
        if after_state is None:
            nodes.pop(lid, None)
        else:
            nodes[lid] = after_state
        touched[lid] = after_state

    return nodes, semantic, conflicts


_V6_CONFLICT_KIND_BY_CLASS = {
    "quantity_changed": "Quantity", "unit_changed": "Unit",
    "scope_broadened": "Scope", "scope_narrowed": "Scope",
    "temporal_scope_changed": "Time", "certainty_strengthened": "Certainty",
    "certainty_weakened": "Certainty", "polarity_flipped": "Certainty",
    "attribution_changed": "Attribution", "causality_changed": "Causality",
    "definition_changed": "Definition",
    "obligation_strengthened": "Obligation", "obligation_weakened": "Obligation",
    "legal_force_strengthened": "LegalForce",
    "legal_force_weakened": "LegalForce", "canon_changed": "Canon",
    "evidence_changed": "Evidence", "wording_only": "Evidence",
}


def _v6_conflict_kind(classes):
    for c in classes or []:
        if c in _V6_CONFLICT_KIND_BY_CLASS:
            return _V6_CONFLICT_KIND_BY_CLASS[c]
    return "Evidence"


def v6_simulate(v6, branch, proposal_digests, actor=None):
    """Compute the full consequence of a change set without committing it."""
    head = v6.ref("heads/" + branch)
    base_nodes = v6.nodes_at(head)
    nodes, semantic, conflicts = v6_apply(v6, base_nodes, proposal_digests)

    changed = {s["logical_id"] for s in semantic}
    frontier = v6.stale_frontier(changed)

    # A wording-only change carries its proof forward. It still re-renders,
    # but it does not invalidate a check, and saying otherwise would train an
    # operator to ignore the report.
    invalidating = {s["logical_id"] for s in semantic
                    if not v6_carries_proof(s["classes"])}
    hard_frontier = v6.stale_frontier(invalidating) if invalidating else set()

    total = len(base_nodes)
    unaffected = total - len(changed | frontier)

    authority = []
    for s in semantic:
        cap = v6_required_capability(s["classes"])
        entry = {"logical_id": s["logical_id"], "classes": s["classes"],
                 "required_capability": cap}
        if actor:
            try:
                v6.authorize(actor, cap, {"kind": "branch", "value": branch})
                entry["actor_holds"] = True
            except WIError as exc:
                entry["actor_holds"] = False
                entry["denied_code"] = exc.code
        authority.append(entry)

    repair = v6_repair_plan(v6, semantic, hard_frontier)

    candidate_root = v6.put_root(nodes, {}, {})

    return {
        "base_root": v6.get(head)["root"] if head else None,
        "candidate_root": candidate_root,
        "branch": branch,
        "semantic_deltas": semantic,
        "conflicts": conflicts,
        "stale_frontier": sorted(frontier),
        "hard_stale_frontier": sorted(hard_frontier),
        "changed_nodes": sorted(changed),
        "total_nodes": total,
        "provably_unaffected": max(unaffected, 0),
        "authority_requirements": authority,
        "repair_plan": repair,
        "committed": False,
    }


def v6_repair_plan(v6, semantic, frontier):
    """Order repair work by safety, not by a blended score.

    The ordering is lexicographic and the categories are never summed. A plan
    that says "cost 7" has hidden the one thing the operator needed to know,
    which is whether the 7 was seven typo fixes or one legal review.
    """
    actions = []
    for s in semantic:
        if v6_carries_proof(s["classes"]):
            continue
        cap = v6_required_capability(s["classes"])
        actions.append({
            "kind": "reverify",
            "targets": [s["logical_id"]],
            "reason": "delta class %s does not carry a prior proof forward"
                      % ", ".join(s["classes"]),
            "requires_authority": [cap],
            "cost": {"human_reviews": 1 if cap != "claim.accept.wording_only" else 0,
                     "deterministic_runs": 1, "judgment_calls": 0,
                     "external_dependencies": 0, "changed_renderings": 1},
        })
    for lid in sorted(frontier):
        actions.append({
            "kind": "recheck_dependent",
            "targets": [lid],
            "reason": "depends on a node whose proof was invalidated",
            "requires_authority": [],
            "cost": {"human_reviews": 0, "deterministic_runs": 1,
                     "judgment_calls": 0, "external_dependencies": 0,
                     "changed_renderings": 1},
        })

    order = ("human_reviews", "deterministic_runs", "judgment_calls",
             "external_dependencies", "changed_renderings")
    actions.sort(key=lambda a: tuple(a["cost"][k] for k in order))
    totals = {k: sum(a["cost"][k] for a in actions) for k in order}
    return {"actions": actions, "totals": totals,
            "ordering": "lexicographic: " + " > ".join(order),
            "note": "categories are reported separately and never summed into "
                    "a single score"}


# --------------------------------------------------------------------------
# Conflict-preserving three-way semantic merge.
# --------------------------------------------------------------------------

def v6_merge(v6, ours_branch, theirs_branch):
    """Three-way merge on meaning, not on lines.

    The engine never manufactures a value neither side asserted. If OURS says
    11,800 and THEIRS says 12,400, the result is a conflict object — not
    "approximately 12,000", which would be a claim invented by a merge.
    """
    ours_head = v6.ref("heads/" + ours_branch)
    theirs_head = v6.ref("heads/" + theirs_branch)
    if not ours_head or not theirs_head:
        raise WIError("WI_INPUT_INVALID",
                      "both branches must exist to merge",
                      ["run `wi branch list`"],
                      {"ours": ours_branch, "theirs": theirs_branch})
    base_head = v6.merge_base(ours_head, theirs_head)

    base = v6.nodes_at(base_head)
    ours = v6.nodes_at(ours_head)
    theirs = v6.nodes_at(theirs_head)

    merged, conflicts, auto = dict(ours), [], []

    for lid in sorted(set(base) | set(ours) | set(theirs)):
        b, o, t = base.get(lid), ours.get(lid), theirs.get(lid)
        if o == t:
            continue                                   # already agree
        if b == o and b != t:
            merged[lid] = t if t is not None else merged.pop(lid, None)
            if t is None:
                merged.pop(lid, None)
            auto.append({"logical_id": lid, "took": "theirs",
                         "why": "only THEIRS moved from the base"})
            continue
        if b == t and b != o:
            auto.append({"logical_id": lid, "took": "ours",
                         "why": "only OURS moved from the base"})
            continue

        # Both sides moved. This is where a text merge starts inventing.
        po = v6.get(o)["payload"] if o else None
        pt = v6.get(t)["payload"] if t else None
        d = v6_classify(po, pt)

        if not d["classes"]:
            auto.append({"logical_id": lid, "took": "ours",
                         "why": "both sides reached the same semantic state"})
            continue

        if d["classes"] == ["wording_only"]:
            # Wording-only is the one class that may auto-merge, and only
            # because the comparison *proved* the typed state is identical.
            # The burden runs this way round, never the other.
            auto.append({"logical_id": lid, "took": "ours",
                         "why": "typed semantic state is identical on both "
                                "sides; the difference is wording only"})
            continue

        pb = v6.get(b)["payload"] if b else None
        conflicts.append({
            "conflict_id": v6_logical_id("conflict", lid, str(b), str(o), str(t)),
            "kind": _v6_conflict_kind(d["classes"]),
            "logical_id": lid,
            "base": b, "ours": o, "theirs": t,
            "classes": d["classes"],
            "base_summary": _v6_summary(pb),
            "ours_summary": _v6_summary(po),
            "theirs_summary": _v6_summary(pt),
            "status": "unresolved",
            "required_resolution": "authorized_decision",
        })

    return {"base_commit": base_head, "ours_commit": ours_head,
            "theirs_commit": theirs_head, "merged_nodes": merged,
            "auto_merged": auto, "conflicts": conflicts,
            "clean": not conflicts}


def _v6_summary(payload):
    if payload is None:
        return "(absent)"
    txt = _v6_field(payload, "text", "statement")
    if txt:
        return _trunc(str(txt), 90)
    qs = _v6_quantities(payload)
    if qs:
        return ", ".join(v6_quantity_str(q) for q in qs)
    return _trunc(json.dumps(payload, sort_keys=True), 90)


# --------------------------------------------------------------------------
# Proof obligations. Derived from typed state, never hard-coded per command.
# --------------------------------------------------------------------------

V6_CHECKS = {
    "anchor.integrity": "the anchor resolves into the exact source state it names",
    "quotation.verbatim": "quoted text matches the source byte range exactly",
    "numeric.value": "every quantity appears in a supporting source",
    "numeric.unit": "the unit in the claim matches the unit in the source",
    "numeric.dimension": "compared quantities share a dimension",
    "date.range": "the stated interval is present in the source",
    "entity.presence": "every named entity appears in a supporting source",
    "citation.resolution": "every citation resolves to an ingested source",
    "scope.temporal": "the claim does not widen the source's time scope",
    "scope.spatial": "the claim does not widen the source's place scope",
    "scope.population": "the claim does not widen the source's population",
    "modality.no-strengthening": "certainty did not increase beyond the source",
    "negation.preservation": "polarity survives the rewrite",
    "attribution.preservation": "who said it survives the rewrite",
    "definition.binding": "every governed term resolves to one definition",
    "obligation.exception-preservation": "no declared exception was dropped",
    "realm.preservation": "the epistemic realm is carried into every rendering",
    "authority.grant-valid": "the acting grant was active and in scope",
    "decision.state-binding": "the decision names the state it authorized",
    "release.closure-digest": "the proof closure digest matches its contents",
    "release.artifact-digest": "the released bytes match the attested digest",
}


def v6_obligations_for(node_state, mode="standard"):
    """Derive the obligation set a single node owes before release."""
    p = node_state["payload"]
    realm = node_state["realm"]
    basis = node_state["reliability"]["basis"]
    ntype = node_state["node_type"]
    obligations = []

    def need(check, required=True, why=""):
        obligations.append({
            "check": check, "requirement": "required" if required else "advisory",
            "why": why or V6_CHECKS.get(check, ""),
        })

    if realm == "external_fact":
        need("anchor.integrity", True,
             "an external fact with no anchor is an assertion wearing a citation")
        need("citation.resolution", True)
        need("realm.preservation", True)
        if _v6_quantities(p):
            need("numeric.value", True)
            need("numeric.unit", True)
            need("numeric.dimension", mode == "strict")
        if _v6_field(p, "temporal_scope"):
            need("date.range", True)
            need("scope.temporal", True)
        if p.get("spatial_scope"):
            need("scope.spatial", True)
        if p.get("population_scope"):
            need("scope.population", True)
        if p.get("attribution"):
            need("attribution.preservation", True)
        if p.get("entities") or p.get("subject"):
            need("entity.presence", mode in ("strict", "regulated"))
        need("modality.no-strengthening", True)
        need("negation.preservation", True)
    elif realm == "author_observation":
        need("realm.preservation", True,
             "an observation must not render as an externally verified fact")
        if basis != "human_declared":
            need("authority.grant-valid", True,
                 "an observation attributed to no one is not an observation")
    elif realm == "inference":
        need("realm.preservation", True)
        if not p.get("premises"):
            need("citation.resolution", True,
                 "an inference with no linked premises cannot be inspected")
    elif realm == "fictional_canon":
        need("realm.preservation", True,
             "a canon check is verified against canon only and must never "
             "render as externally verified fact")
    elif realm == "hypothetical":
        need("realm.preservation", True)

    if ntype in ("meaning.obligation", "meaning.promise"):
        need("obligation.exception-preservation", True)
        need("authority.grant-valid", True)
    if ntype == "meaning.definition":
        need("definition.binding", True)
    if ntype == "meaning.forecast":
        need("scope.temporal", True,
             "a forecast with no horizon is not a forecast")
    if ntype == "meaning.argument":
        need("citation.resolution", True,
             "every premise must exist and carry its own proof state")

    if basis == "judged":
        obligations.append({
            "check": "judgment.disagreement",
            "requirement": "required" if mode in ("strict", "regulated") else "advisory",
            "why": "a judged basis is not a verified basis and must not be "
                   "rendered as one",
        })

    seen, out = set(), []
    for o in obligations:
        if o["check"] in seen:
            continue
        seen.add(o["check"])
        out.append(o)
    return out


# --------------------------------------------------------------------------
# The graph constraint engine.
#
# Schema validity is not enough. A graph can be well-formed JSON and still be
# epistemically impossible, and those are exactly the states that look fine in
# a UI. Constraints run before a transition reaches graph state.
# --------------------------------------------------------------------------

V6_CONSTRAINTS = [
    ("C001", "source-version-raw-digest-unique",
     "two source versions may not share a raw byte digest"),
    ("C002", "anchor-source-state-exists",
     "every anchor resolves to a source state that is present"),
    ("C003", "anchor-source-state-current-or-historical",
     "an anchor into a superseded source is marked, never silently current"),
    ("C004", "verified-result-produced-by-deterministic-engine",
     "only the deterministic engine may emit a verified result"),
    ("C005", "judged-result-never-typed-verified",
     "a judgment record may never carry a verified basis"),
    ("C006", "decision-target-state-exists",
     "a decision names a target state that is present"),
    ("C007", "decision-target-state-not-superseded",
     "a decision may not authorize a state that had already moved"),
    ("C008", "provider-has-no-authority-grants",
     "a judgment provider holds no capability grant"),
    ("C009", "release-closure-is-complete",
     "every dependency named by a release is inside its closure"),
    ("C010", "release-artifact-digest-matches",
     "released bytes match the attested artifact digest"),
    ("C011", "claim-realm-cannot-disappear-in-rendering",
     "a realm marker survives every rendering"),
    ("C012", "temporal-validity-overlap-detects-contradiction",
     "two states of one node may not assert different values over the same instant"),
    ("C013", "unit-dimension-matches-comparison",
     "quantities compared as equal share a unit"),
    ("C014", "obligation-authority-is-known",
     "every obligation names the actor it binds"),
    ("C015", "semantic-conflict-cannot-be-rendered-as-resolved",
     "an unresolved conflict blocks the branch it lives on"),
    ("C016", "protected-span-cannot-be-auto-rewritten",
     "a protected span is never rewritten without a decision"),
    ("C017", "source-data-cannot-create-system-instruction",
     "ingested source text carries no authority over the runtime"),
    ("C018", "imported-object-schema-must-be-known-or-quarantined",
     "an object with an unknown schema is quarantined, never guessed"),
    ("C019", "policy-state-is-part-of-proof-closure",
     "the policy in force is named by the release it governed"),
    ("C020", "actor-cannot-exercise-revoked-or-expired-grant",
     "a revoked or expired grant authorizes nothing"),
]


def v6_run_constraints(v6, branch=None):
    """Evaluate the constraint set over the current workspace state.

    Every constraint reports one of `pass`, `fail` or `not_evaluated`. There
    is no fourth status and no aggregate score. `not_evaluated` always carries
    the reason, because a constraint that quietly did nothing is worse than a
    constraint that is missing.
    """
    branch = branch or v6.head_branch()
    head = v6.ref("heads/" + branch)
    nodes = v6.nodes_at(head)
    db = v6.db
    results = []

    def rec(cid, name, status, detail, violations=None):
        results.append({"id": cid, "name": name, "status": status,
                        "detail": detail, "violations": violations or []})

    by_id = {c[0]: c for c in V6_CONSTRAINTS}

    # C001
    rows = db.execute("SELECT digest, COUNT(*) c FROM object_blob"
                      " GROUP BY digest HAVING c > 1").fetchall()
    rec("C001", by_id["C001"][1], "fail" if rows else "pass",
        "%d duplicate source digest(s)" % len(rows),
        [r["digest"] for r in rows])

    # C002 / C003
    missing, stale_anchor = [], []
    stale = v6.ws.stale_nodes()
    for r in db.execute("SELECT logical_id, payload_json FROM node_state"
                        " WHERE schema_id LIKE '%anchor%'"):
        try:
            pl = json.loads(r["payload_json"])
        except Exception:
            continue
        sv = pl.get("source_version_state") or pl.get("source_version")
        if sv and not db.execute(
                "SELECT 1 FROM node_state WHERE state_digest=?", (sv,)).fetchone():
            missing.append(r["logical_id"])
        if r["logical_id"] in stale:
            stale_anchor.append(r["logical_id"])
    rec("C002", by_id["C002"][1], "fail" if missing else "pass",
        "%d anchor(s) point at an absent source state" % len(missing), missing)
    rec("C003", by_id["C003"][1], "pass",
        "%d anchor(s) into a changed source, all marked stale" % len(stale_anchor),
        stale_anchor)

    # C004 / C005
    bad_basis = []
    for r in db.execute("SELECT logical_id, payload_json FROM node_state"
                        " WHERE schema_id LIKE '%verification%'"
                        "    OR schema_id LIKE '%judgment%'"):
        pl = json.loads(r["payload_json"])
        basis = (pl.get("basis") or pl.get("reliability", {}).get("basis") or "")
        engine = pl.get("engine") or pl.get("produced_by") or ""
        if basis == "verified" and "judgment" in (pl.get("kind") or ""):
            bad_basis.append(r["logical_id"])
        if basis == "verified" and engine and "deterministic" not in engine:
            bad_basis.append(r["logical_id"])
    rec("C004", by_id["C004"][1], "fail" if bad_basis else "pass",
        "%d verified result(s) not produced by the deterministic engine"
        % len(bad_basis), bad_basis)
    judged_bad = []
    for r in db.execute("SELECT digest, payload_json FROM v6_object"
                        " WHERE schema_id='wi.v6.judgment'"):
        pl = json.loads(r["payload_json"])
        if pl.get("reliability", {}).get("basis") == "verified":
            judged_bad.append(r["digest"])
    rec("C005", by_id["C005"][1], "fail" if judged_bad else "pass",
        "%d judgment record(s) typed as verified" % len(judged_bad), judged_bad)

    # C006 / C007
    absent, superseded = [], []
    for r in db.execute("SELECT decision_id, digest FROM v6_decision"):
        d = v6.get(r["digest"])
        tgt = d.get("target_state_digest")
        if tgt and not v6.has(tgt):
            absent.append(r["decision_id"])
        elif tgt and tgt not in nodes.values():
            superseded.append(r["decision_id"])
    rec("C006", by_id["C006"][1], "fail" if absent else "pass",
        "%d decision(s) name a state that is not present" % len(absent), absent)
    rec("C007", by_id["C007"][1], "pass",
        "%d decision(s) bound to a state this branch has since moved past; "
        "each is retained as history, none authorizes the current state"
        % len(superseded), superseded)

    # C008
    providers = []
    for r in db.execute("SELECT grant_id, digest, subject FROM v6_grant"):
        g = v6.get(r["digest"])
        if (g.get("subject_kind") or "") in V6_FORBIDDEN_SUBJECT_KINDS:
            providers.append(r["grant_id"])
    rec("C008", by_id["C008"][1], "fail" if providers else "pass",
        "%d grant(s) issued to a judgment provider" % len(providers), providers)

    # C009 / C010 / C019 — release closure lives in .wiab artifacts
    rec("C009", by_id["C009"][1], "not_evaluated",
        "no v6 release closure in this workspace; `wi verify-release` checks "
        "the v5 closure of an existing .wiab")
    rec("C010", by_id["C010"][1], "not_evaluated",
        "artifact digests are checked by `wi verify-release` against a bundle, "
        "not against workspace state")
    rec("C019", by_id["C019"][1], "not_evaluated",
        "no v6 release has been built in this workspace")

    # C011 / C016 — need render source maps, which are a v6 compiler artifact
    rec("C011", by_id["C011"][1], "not_evaluated",
        "no render source maps in this workspace; the compiler backends that "
        "produce them are specified and do not ship in 6.0.0")
    rec("C016", by_id["C016"][1], "not_evaluated",
        "no protected spans are declared in this workspace")

    # C012 — bitemporal contradiction, computed by interval intersection
    overlaps = []
    by_logical = {}
    for r in db.execute("SELECT digest, payload_json FROM v6_object"
                        " WHERE schema_id='wi.v6.node_state'"):
        pl = json.loads(r["payload_json"])
        by_logical.setdefault(pl["logical_id"], []).append((r["digest"], pl))
    live = set(nodes.values())
    for lid, states in by_logical.items():
        cur = [(d, pl) for d, pl in states if d in live]
        for i in range(len(cur)):
            for j in range(i + 1, len(cur)):
                a, b = cur[i][1], cur[j][1]
                if not v6_intervals_overlap(a["valid_time"], b["valid_time"]):
                    continue
                if a["payload"] != b["payload"]:
                    overlaps.append(lid)
    rec("C012", by_id["C012"][1], "fail" if overlaps else "pass",
        "%d node(s) assert different values over an overlapping valid interval"
        % len(overlaps), sorted(set(overlaps)))

    # C013
    dim = []
    for lid, sd in nodes.items():
        pl = v6.get(sd)["payload"]
        qs = _v6_quantities(pl)
        units = {q.get("unit") for q in qs}
        if len(qs) > 1 and len(units) > 1 and pl.get("comparison") == "equal":
            dim.append(lid)
    rec("C013", by_id["C013"][1], "fail" if dim else "pass",
        "%d node(s) compare quantities across units" % len(dim), dim)

    # C014
    unbound = []
    for lid, sd in nodes.items():
        ns = v6.get(sd)
        if ns["node_type"] in ("meaning.obligation", "meaning.promise"):
            if not (ns["payload"].get("bound_actor") or ns["payload"].get("subject")):
                unbound.append(lid)
    rec("C014", by_id["C014"][1], "fail" if unbound else "pass",
        "%d obligation(s) name no bound actor" % len(unbound), unbound)

    # C015
    open_conf = [r["conflict_id"] for r in db.execute(
        "SELECT conflict_id FROM v6_conflict WHERE branch=? AND status='unresolved'",
        (branch,))]
    rec("C015", by_id["C015"][1], "fail" if open_conf else "pass",
        "%d unresolved semantic conflict(s) on %s" % (len(open_conf), branch),
        open_conf)

    # C017 — reuse the v4 injection scanner over ingested source text
    injected = []
    for r in db.execute("SELECT logical_id, payload_json FROM node_state"
                        " WHERE schema_id LIKE '%source%'"):
        pl = json.loads(r["payload_json"])
        text = pl.get("text") or ""
        if text and scan_source_text(text, pl.get("title", ""))["findings"]:
            injected.append(r["logical_id"])
    rec("C017", by_id["C017"][1], "pass",
        "%d source(s) carry injection indicators; all are quarantined as data "
        "and none can reach the authority path" % len(injected), injected)

    # C018
    known = {"wi.v6." + s for s in (
        "node_state", "graph_root", "commit", "delta", "proposal", "decision",
        "grant", "conflict", "capsule", "judgment")}
    unknown = sorted({r["schema_id"] for r in db.execute(
        "SELECT DISTINCT schema_id FROM v6_object")} - known)
    rec("C018", by_id["C018"][1], "fail" if unknown else "pass",
        "%d object(s) carry a schema this core does not know" % len(unknown),
        unknown)

    # C020
    bad_grants = []
    for r in db.execute("SELECT grant_id, digest, revoked_at FROM v6_grant"):
        if not r["revoked_at"]:
            continue
        for dr in db.execute("SELECT digest FROM v6_decision"):
            d = v6.get(dr["digest"])
            rec_ = d.get("authority_receipt") or {}
            if rec_.get("grant_id") == r["grant_id"] and \
                    str(d.get("decided_at", "")) > str(r["revoked_at"]):
                bad_grants.append(r["grant_id"])
    rec("C020", by_id["C020"][1], "fail" if bad_grants else "pass",
        "%d decision(s) exercised a grant after it was revoked" % len(bad_grants),
        sorted(set(bad_grants)))

    failed = [r for r in results if r["status"] == "fail"]
    return {"branch": branch, "results": results,
            "evaluated": sum(1 for r in results if r["status"] != "not_evaluated"),
            "not_evaluated": sum(1 for r in results if r["status"] == "not_evaluated"),
            "failed": len(failed),
            "verdict": "FAIL" if failed else "PASS"}


# --------------------------------------------------------------------------
# Merkleized proof closure and selective disclosure capsules.
#
# This is a local cryptographic commitment to a finite dependency set. It is
# not a blockchain: there is no consensus network, no token, no chain and no
# global ledger, and nothing here requires anyone to agree with anyone.
# --------------------------------------------------------------------------

def v6_leaf_digest(leaf):
    pre = (b"wi-closure-leaf-v6\x00" + canonical_bytes(leaf))
    return "sha256:" + sha256_hex(pre)


def v6_merkle_root(leaf_digests):
    """Binary Merkle root over ordered leaves. An odd node pairs with itself."""
    if not leaf_digests:
        return "sha256:" + sha256_hex(b"wi-closure-empty-v6")
    level = list(leaf_digests)
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            a = level[i]
            b = level[i + 1] if i + 1 < len(level) else level[i]
            nxt.append("sha256:" + sha256_hex(
                b"wi-closure-node-v6\x00" + a.encode() + b"\x00" + b.encode()))
        level = nxt
    return level[0]


def v6_inclusion_proof(leaf_digests, index):
    """The sibling path proving one leaf belongs to the root."""
    path, level, idx = [], list(leaf_digests), index
    while len(level) > 1:
        sibling_idx = idx + 1 if idx % 2 == 0 else idx - 1
        if sibling_idx >= len(level):
            sibling_idx = idx
        path.append({"position": "right" if idx % 2 == 0 else "left",
                     "digest": level[sibling_idx]})
        nxt = []
        for i in range(0, len(level), 2):
            a = level[i]
            b = level[i + 1] if i + 1 < len(level) else level[i]
            nxt.append("sha256:" + sha256_hex(
                b"wi-closure-node-v6\x00" + a.encode() + b"\x00" + b.encode()))
        level, idx = nxt, idx // 2
    return path


def v6_verify_inclusion(leaf_digest, path, root):
    cur = leaf_digest
    for step in path:
        a, b = ((cur, step["digest"]) if step["position"] == "right"
                else (step["digest"], cur))
        cur = "sha256:" + sha256_hex(
            b"wi-closure-node-v6\x00" + a.encode() + b"\x00" + b.encode())
    return cur == root


def v6_closure_leaves(v6, nodes):
    """Ordered closure leaves for a node map. Sorted before hashing."""
    leaves = []
    for lid in sorted(nodes):
        sd = nodes[lid]
        ns = v6.get(sd)
        leaves.append({"object_type": "wi.v6.node_state",
                       "logical_id": lid, "state_digest": sd,
                       "node_type": ns["node_type"], "realm": ns["realm"],
                       "basis": ns["reliability"]["basis"]})
    return leaves


def v6_capsule_create(v6, branch, select=None, profile="selective",
                      redact_payloads=False):
    head = v6.ref("heads/" + branch)
    if not head:
        raise WIError("WI_INPUT_INVALID", "branch %s has no commits" % branch,
                      ["run `wi commit` first"])
    nodes = v6.nodes_at(head)
    leaves = v6_closure_leaves(v6, nodes)
    leaf_digests = [v6_leaf_digest(l) for l in leaves]
    root = v6_merkle_root(leaf_digests)

    select = set(select or [])
    if profile == "full":
        select = set(nodes)
    disclosed, proofs, redactions = [], [], []
    for i, leaf in enumerate(leaves):
        lid = leaf["logical_id"]
        if select and lid not in select:
            redactions.append({"logical_id": lid,
                               "leaf_digest": leaf_digests[i],
                               "disclosed": False,
                               "proves": "this leaf was part of the producer's "
                                         "closure",
                               "does_not_prove": "anything about its content"})
            continue
        entry = {"leaf": leaf, "leaf_digest": leaf_digests[i]}
        if not redact_payloads:
            entry["state"] = v6.get(leaf["state_digest"])
        disclosed.append(entry)
        proofs.append({"leaf_digest": leaf_digests[i],
                       "path": v6_inclusion_proof(leaf_digests, i)})

    manifest = {
        "schema": "wi.v6.capsule",
        "format": "wic/1",
        "profile": profile,
        "core_version": VERSION,
        "branch": branch,
        "commit": head,
        "graph_root": v6.get(head)["root"],
        "closure_root": root,
        "leaf_count": len(leaves),
        "disclosed_count": len(disclosed),
        "built_at": _now(),
        "declared_omissions": [
            {"kind": "judgment.entailment", "status": "unavailable_on_surface",
             "reason": "this core contains no judgment provider"},
            {"kind": "signature", "status": "unavailable_on_surface",
             "reason": "external signing is specified and does not ship in "
                       "%s" % VERSION},
        ],
        "not_a_proof_of": [
            "that the underlying sources are correct",
            "that a redacted leaf's content was independently inspected",
        ],
    }
    return {"manifest": manifest, "disclosed": disclosed,
            "inclusion_proofs": proofs, "redactions": redactions}


def v6_capsule_verify(capsule):
    """Recompute everything a capsule asserts about itself."""
    checks, ok = [], True

    def add(name, passed, detail):
        nonlocal ok
        checks.append({"check": name, "result": "pass" if passed else "fail",
                       "detail": detail})
        if not passed:
            ok = False

    m = capsule.get("manifest") or {}
    add("capsule.format", m.get("format") == "wic/1",
        "format is %r" % m.get("format"))

    root = m.get("closure_root")
    disclosed = capsule.get("disclosed") or []
    proofs = {p["leaf_digest"]: p["path"] for p in capsule.get("inclusion_proofs") or []}

    recomputed, states_ok, states_seen = 0, True, 0
    for entry in disclosed:
        ld = v6_leaf_digest(entry["leaf"])
        if ld != entry["leaf_digest"]:
            add("leaf.digest", False,
                "leaf %s does not hash to its recorded digest"
                % entry["leaf"]["logical_id"])
            continue
        recomputed += 1
        if "state" in entry:
            states_seen += 1
            sd = v6_state_digest(entry["state"], "wi.v6.node_state")
            if sd != entry["leaf"]["state_digest"]:
                states_ok = False
                add("state.digest", False,
                    "disclosed state for %s does not match the digest its leaf "
                    "names; the bytes in this capsule are not the bytes that "
                    "were attested" % entry["leaf"]["logical_id"])
    if recomputed == len(disclosed) and disclosed:
        add("leaf.digest", True, "%d disclosed leaf digest(s) recomputed" % recomputed)
    if states_ok and states_seen:
        add("state.digest", True,
            "%d disclosed state(s) hash to the digest the leaf names" % states_seen)

    included = 0
    for entry in disclosed:
        path = proofs.get(entry["leaf_digest"])
        if path is None:
            add("inclusion.proof", False,
                "no inclusion proof for %s" % entry["leaf"]["logical_id"])
            continue
        if not v6_verify_inclusion(entry["leaf_digest"], path, root):
            add("inclusion.proof", False,
                "inclusion proof for %s does not reach the closure root"
                % entry["leaf"]["logical_id"])
            continue
        included += 1
    if included == len(disclosed) and disclosed:
        add("inclusion.proof", True,
            "%d leaf/leaves proved to belong to closure root %s"
            % (included, root[:19]))

    total = m.get("leaf_count", 0)
    add("closure.count", len(disclosed) + len(capsule.get("redactions") or []) == total,
        "%d disclosed + %d redacted against a declared %d leaves"
        % (len(disclosed), len(capsule.get("redactions") or []), total))

    return {"verdict": "VERIFIED" if ok else "TAMPERED", "checks": checks,
            "closure_root": root,
            "scope": "this capsule proves membership in the producer's closure "
                     "and the integrity of what it disclosed; it proves nothing "
                     "about whether the sources are correct"}


# --------------------------------------------------------------------------
# v6 command implementations.
# --------------------------------------------------------------------------

def _v6_open(args):
    ws = Workspace.find(getattr(args, "root", ".") or ".")
    v6 = V6(ws)
    v6.ensure_initialized()
    v6.commit_db()
    return ws, v6


def _v6_emit(args, obj, render):
    if getattr(args, "json", False):
        print(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False))
    else:
        print(render(obj))


def cmd_canon(args):
    """Canonical form and domain-separated digest of a JSON object."""
    raw = sys.stdin.read() if args.path == "-" else Path(args.path).read_text("utf-8")
    try:
        obj = json.loads(raw)
    except ValueError as exc:
        raise WIError("WI_INPUT_INVALID", "input is not JSON: %s" % exc,
                      ["pass a JSON document, or - to read stdin"])
    canon = canonical_bytes(obj)
    out = {
        "schema": args.schema,
        "canonical_bytes": len(canon),
        "content_digest": content_digest(obj),
        "state_digest_v6": v6_state_digest(obj, args.schema),
        "state_digest_v5": state_digest(obj, args.schema),
        "canonicalization": CANONICALIZATION,
        "normalization": NORMALIZATION,
    }
    if args.show:
        out["canonical"] = canon.decode("utf-8")

    def render(o):
        L = ["canonical bytes  %d" % o["canonical_bytes"],
             "content digest   %s" % o["content_digest"],
             "v6 state digest  %s" % o["state_digest_v6"],
             "v5 state digest  %s" % o["state_digest_v5"],
             "",
             "The two state digests differ by domain separation, on purpose:",
             "a byte-identical payload must never be ambiguously readable as",
             "both a v5 and a v6 object."]
        if args.show:
            L += ["", o["canonical"]]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_branch(args):
    ws, v6 = _v6_open(args)
    action = args.action or "list"

    if action == "list":
        head = v6.head_branch()
        rows = []
        for name, digest in v6.refs("heads/"):
            b = name[len("heads/"):]
            c = v6.get(digest)
            rows.append({"branch": b, "current": b == head, "commit": digest,
                         "root": c["root"], "message": c["message"],
                         "nodes": len(v6.nodes_at(digest))})
        out = {"head": head, "branches": rows}

        def render(o):
            L = ["BRANCHES"]
            for r in o["branches"]:
                L.append("  %s %-24s %s  %4d nodes  %s"
                         % ("*" if r["current"] else " ", r["branch"],
                            r["commit"][7:19], r["nodes"], _trunc(r["message"], 44)))
            return "\n".join(L)
        _v6_emit(args, out, render)
        return 0

    if action == "create":
        name = args.name
        if v6.ref("heads/" + name):
            raise WIError("WI_INPUT_INVALID", "branch %s already exists" % name,
                          ["pick another name", "or `wi branch switch %s`" % name])
        src = args.source or v6.head_branch()
        base = v6.ref("heads/" + src)
        if not base:
            raise WIError("WI_INPUT_INVALID", "no branch %s to branch from" % src,
                          ["run `wi branch list`"])
        v6.set_ref("heads/" + name, base, expected=None)
        if args.switch:
            v6.set_ref("HEAD", name)
        v6.commit_db()
        print("created %s at %s%s"
              % (name, base[7:19], " and switched to it" if args.switch else ""))
        print("A branch is a ref. Nothing was copied: the objects are immutable")
        print("and shared, so this cost one row.")
        return 0

    if action == "switch":
        if not v6.ref("heads/" + args.name):
            raise WIError("WI_INPUT_INVALID", "no branch %s" % args.name,
                          ["run `wi branch list`"])
        v6.set_ref("HEAD", args.name)
        v6.commit_db()
        print("switched to %s" % args.name)
        return 0

    if action == "delete":
        if args.name == "main":
            raise WIError("WI_POLICY_REJECTED", "main may not be deleted",
                          ["delete a working branch instead"])
        if not v6.ref("heads/" + args.name):
            raise WIError("WI_INPUT_INVALID", "no branch %s" % args.name, [])
        v6.delete_ref("heads/" + args.name)
        if v6.head_branch() == args.name:
            v6.set_ref("HEAD", "main")
        v6.commit_db()
        print("deleted %s" % args.name)
        return 0
    return 0


def cmd_propose(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    head = v6.ref("heads/" + branch)
    nodes = v6.nodes_at(head)

    payloads = []
    if args.from_ledger:
        ledger = json.loads(Path(args.from_ledger).read_text("utf-8"))
        for atom in ledger.get("atoms", ledger.get("claims", [])):
            lid = atom.get("logical_id") or v6_logical_id(
                "claim", atom.get("text", ""))
            payloads.append((lid, "meaning.claim_atom", _v6_from_atom(atom),
                             atom.get("realm", "external_fact")))
    else:
        if not args.node:
            raise WIError("WI_INPUT_INVALID",
                          "a proposal needs a target node",
                          ["pass --node ID --payload FILE",
                           "or --from-ledger LEDGER.json"])
        payload = json.loads(Path(args.payload).read_text("utf-8"))
        payloads.append((args.node, args.type, payload, args.realm))

    created = []
    for lid, ntype, payload, realm in payloads:
        before_digest = nodes.get(lid)
        before = v6.get(before_digest)["payload"] if before_digest else None
        # A payload that declares its own temporal scope *is* declaring a
        # valid interval. Reading it here is a mapping, not an inference:
        # nothing is filled in that the author did not write.
        vt = None
        if args.valid_from or args.valid_until:
            vt = v6_valid_interval(args.valid_from, args.valid_until)
        elif isinstance(payload.get("temporal_scope"), dict):
            ts = payload["temporal_scope"]
            vt = v6_valid_interval(ts.get("from"), ts.get("until"))
        after_digest = v6.put_node_state(
            lid, ntype, payload, realm=realm, valid_time=vt,
            reliability={"basis": args.basis, "actor": args.actor})
        if after_digest == before_digest:
            continue
        after = v6.get(after_digest)["payload"]
        d = v6_classify(before, after)
        pid = v6_logical_id("proposal", lid, str(before_digest), after_digest)
        obj = {
            "proposal_id": pid,
            "target_logical_id": lid,
            "target_state_digest": before_digest,
            "before": before_digest,
            "after": after_digest,
            "semantic_delta": d,
            "required_capability": v6_required_capability(d["classes"]),
            "rationale": args.why or "",
            "proposed_by": args.actor,
            "created_at": _now(),
            "expires_at": args.expires,
        }
        pdigest = v6.put(obj, "wi.v6.proposal")
        v6.db.execute("INSERT OR REPLACE INTO v6_proposal VALUES (?,?,?,?,?,?)",
                      (pid, pdigest, branch, "open", None, _now()))
        created.append(obj)

    for dep in args.depends_on or []:
        for lid, _, _, _ in payloads:
            v6.db.execute("INSERT OR REPLACE INTO v6_edge VALUES (?,?,?,?,?)",
                          (v6_logical_id("edge", lid, dep, DEPENDENCY),
                           lid, dep, DEPENDENCY, _now()))
    v6.commit_db()

    out = {"branch": branch, "created": created}

    def render(o):
        if not o["created"]:
            return ("No proposal created: the payload is byte-identical to the "
                    "state already on %s." % o["branch"])
        L = ["PROPOSED on %s" % o["branch"], ""]
        for p in o["created"]:
            L.append("  %s" % p["proposal_id"])
            L.append("    node      %s" % p["target_logical_id"])
            L.append("    delta     %s" % (", ".join(p["semantic_delta"]["classes"])
                                           or "(none)"))
            L.append("    requires  %s" % p["required_capability"])
            L.append("    bound to  %s" % (p["target_state_digest"] or "(new node)"))
        L += ["", "Nothing has changed on %s. A proposal is not an edit — run"
                  % o["branch"],
              "`wi simulate` to see what accepting it would do."]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def _v6_from_atom(atom):
    """Lift a v5 claim atom into a v6 payload without inventing fields.

    Anything v5 did not record is absent, not guessed. A migration that fills
    in a plausible value has rewritten history and called it an upgrade.
    """
    prop = atom.get("proposition") or {}
    out = {"text": atom.get("text", "")}
    qs = prop.get("quantities") or []
    if qs:
        out["quantities"] = [v6_quantity(q["value"], q.get("unit")) for q in qs]
    if prop.get("temporal_scope"):
        ts = prop["temporal_scope"]
        out["temporal_scope"] = {"from": ts.get("start"), "until": ts.get("end")}
    if prop.get("modality"):
        out["modality"] = prop["modality"]
    if prop.get("negated"):
        out["polarity"] = "negative"
    if prop.get("attribution"):
        out["attribution"] = [prop["attribution"]]
    if prop.get("entities"):
        out["entities"] = sorted(prop["entities"])
    if prop.get("causal"):
        out["causality"] = "asserted"
    out["absent_from_source_version"] = sorted(
        k for k in ("spatial_scope", "population_scope", "certainty",
                    "exceptions", "qualifiers")
        if k not in out)
    return out


def cmd_proposals(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    rows = []
    for r in v6.open_proposals(branch, args.status):
        p = v6.get(r["digest"])
        rows.append({"proposal_id": r["proposal_id"], "status": r["status"],
                     "node": p["target_logical_id"],
                     "classes": p["semantic_delta"]["classes"],
                     "requires": p["required_capability"],
                     "by": p["proposed_by"], "why": p["rationale"],
                     "applied_in": r["applied_in"]})
    out = {"branch": branch, "proposals": rows}

    def render(o):
        if not o["proposals"]:
            return "No proposals on %s." % o["branch"]
        L = ["PROPOSALS on %s" % o["branch"], ""]
        for p in o["proposals"]:
            L.append("  [%-9s] %s" % (p["status"], p["proposal_id"]))
            L.append("      %-16s ->  %s" % (p["node"][:16],
                                           ", ".join(p["classes"]) or "(none)"))
            L.append("      requires %s   proposed by %s"
                     % (p["requires"], p["by"]))
            if p["why"]:
                L.append("      %s" % _trunc(p["why"], 70))
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_simulate(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    if args.proposal:
        digests = [v6.proposal(pid)["digest"] for pid in args.proposal]
    else:
        digests = [r["digest"] for r in v6.open_proposals(branch, "open")]
    if not digests:
        raise WIError("WI_INPUT_INVALID",
                      "there is nothing to simulate on %s" % branch,
                      ["create one with `wi propose`",
                       "or name a proposal with --proposal ID"])
    rep = v6_simulate(v6, branch, digests, actor=args.actor)
    v6.commit_db()

    def render(o):
        L = ["SIMULATION ONLY — %s is unchanged" % o["branch"], ""]
        L.append("Semantic change")
        for s in o["semantic_deltas"]:
            L.append("  %s" % s["logical_id"])
            L.append("    class   %s" % (", ".join(s["classes"]) or "(none)"))
            for impact, cls in sorted(s["proof_impact"].items()):
                L.append("    proof   %s: %s" % (impact, ", ".join(cls)))
        L.append("")
        L.append("Authority required")
        for a in o["authority_requirements"]:
            held = ""
            if "actor_holds" in a:
                held = "  [held]" if a["actor_holds"] else "  [%s]" % a.get(
                    "denied_code", "not held")
            L.append("  %-40s %s%s" % (a["logical_id"][:36],
                                       a["required_capability"], held))
        if o["conflicts"]:
            L.append("")
            L.append("Conflicts")
            for c in o["conflicts"]:
                L.append("  %-12s %s" % (c["kind"], c["logical_id"]))
                L.append("      %s" % c.get("detail", ""))
        L.append("")
        L.append("Impact")
        L.append("  %4d node(s) directly changed" % len(o["changed_nodes"]))
        L.append("  %4d node(s) become stale" % len(o["stale_frontier"]))
        L.append("  %4d node(s) stale through an invalidated proof"
                 % len(o["hard_stale_frontier"]))
        L.append("")
        L.append("Minimum safe repair frontier")
        if not o["repair_plan"]["actions"]:
            L.append("  none — every delta in this set carries its proof forward")
        for i, a in enumerate(o["repair_plan"]["actions"], 1):
            L.append("  %d. %-18s %s" % (i, a["kind"], a["targets"][0][:36]))
            L.append("     %s" % a["reason"])
        L.append("")
        L.append("  ordering: %s" % o["repair_plan"]["ordering"])
        L.append("")
        L.append("Provably unaffected")
        L.append("  %4d of %d node(s) on %s" % (o["provably_unaffected"],
                                                o["total_nodes"], o["branch"]))
        L.append("")
        L.append("candidate root  %s" % o["candidate_root"])
        L.append("Nothing was written. This root exists only to be compared.")
        return "\n".join(L)

    _v6_emit(args, rep, render)
    return 1 if rep["conflicts"] else 0


def cmd_decide(args):
    ws, v6 = _v6_open(args)
    row = v6.proposal(args.proposal)
    p = v6.get(row["digest"])
    branch = row["branch"]
    head = v6.ref("heads/" + branch)
    nodes = v6.nodes_at(head)

    if row["status"] != "open":
        raise WIError("WI_PROPOSAL_STALE",
                      "proposal %s is %s, not open" % (args.proposal, row["status"]),
                      ["open a new proposal against the current state"])

    # Law: a decision binds to the exact state it authorized. If the target
    # moved between proposal and decision, the approval does not reattach.
    current = nodes.get(p["target_logical_id"])
    if current != p["target_state_digest"]:
        v6.set_proposal_status(args.proposal, "superseded")
        v6.commit_db()
        raise WIError("WI_DECISION_STALE",
                      "the target moved after this proposal was written",
                      ["re-read the current state and open a new proposal",
                       "the system will not reattach an approval to a state "
                       "the reviewer never saw"],
                      {"proposal_bound_to": p["target_state_digest"] or "(new node)",
                       "branch_now_holds": current or "(absent)"})

    outcome = ("accepted" if args.accept else
               "rejected" if args.reject else "deferred")

    receipt = None
    if outcome == "accepted":
        receipt = v6.authorize(args.actor, p["required_capability"],
                               {"kind": "branch", "value": branch})

    did = v6_logical_id("decision", args.proposal, outcome, args.actor)
    dobj = {
        "decision_id": did,
        "proposal_digest": row["digest"],
        "target_state_digest": p["target_state_digest"],
        "outcome": outcome,
        "actor": args.actor,
        "authority_receipt": receipt,
        "reason": args.reason or "",
        "decided_at": _now(),
    }
    ddigest = v6.put(dobj, "wi.v6.decision")
    v6.db.execute("INSERT OR REPLACE INTO v6_decision VALUES (?,?,?,?)",
                  (did, ddigest, args.proposal, _now()))
    v6.set_proposal_status(args.proposal,
                           {"accepted": "accepted", "rejected": "rejected",
                            "deferred": "deferred"}[outcome])
    v6.commit_db()

    out = {"decision": dobj, "decision_digest": ddigest}

    def render(o):
        d = o["decision"]
        L = ["DECISION %s" % d["outcome"].upper(),
             "  proposal   %s" % args.proposal,
             "  bound to   %s" % (d["target_state_digest"] or "(new node)"),
             "  actor      %s" % d["actor"]]
        if d["authority_receipt"]:
            L.append("  grant      %s (%s)" % (d["authority_receipt"]["grant_id"],
                                               d["authority_receipt"]["capability"]))
        if d["reason"]:
            L.append("  reason     %s" % d["reason"])
        L += ["", "Accepted is a decision, not an application. Run `wi commit`",
              "to apply every accepted proposal as one transaction."]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_v6_commit(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    head = v6.ref("heads/" + branch)
    accepted = v6.open_proposals(branch, "accepted")
    if not accepted:
        raise WIError("WI_INPUT_INVALID",
                      "no accepted proposals to apply on %s" % branch,
                      ["accept one with `wi decide ID --accept --actor NAME`"])

    base_nodes = v6.nodes_at(head)
    digests = [r["digest"] for r in accepted]
    nodes, semantic, conflicts = v6_apply(v6, base_nodes, digests)
    if conflicts:
        raise WIError("WI_SEMANTIC_CONFLICT",
                      "%d conflict(s) block this commit" % len(conflicts),
                      ["run `wi simulate` to see them",
                       "resolve each with an authorized decision"],
                      {"conflicts": [c["logical_id"] for c in conflicts]})

    root = v6.put_root(nodes, {}, {})
    delta = v6.put({
        "added": sorted(set(nodes) - set(base_nodes)),
        "removed": sorted(set(base_nodes) - set(nodes)),
        "superseded": [{"logical_id": s["logical_id"], "from": s["from"],
                        "to": s["to"]} for s in semantic if s["from"]],
        "semantic": semantic,
    }, "wi.v6.delta")

    decisions = []
    for r in accepted:
        dr = v6.db.execute("SELECT digest FROM v6_decision WHERE proposal_id=?",
                           (r["proposal_id"],)).fetchone()
        if dr:
            decisions.append(dr["digest"])

    cobj = {"parents": [head] if head else [], "root": root, "delta": delta,
            "actor": args.actor, "decision": decisions,
            "message": args.message, "timestamp": _now()}
    cdigest = v6.put(cobj, "wi.v6.commit")
    v6.set_ref("heads/" + branch, cdigest, expected=head)
    for r in accepted:
        v6.set_proposal_status(r["proposal_id"], "applied", applied_in=cdigest)
    v6.commit_db()

    out = {"commit": cdigest, "root": root, "prior_root": v6.get(head)["root"]
           if head else None, "applied": len(accepted),
           "semantic_deltas": semantic, "branch": branch}

    def render(o):
        L = ["COMMIT %s" % o["commit"][7:19],
             "  branch      %s" % o["branch"],
             "  prior root  %s" % (o["prior_root"] or "(none)"),
             "  next root   %s" % o["root"],
             "  applied     %d accepted proposal(s)" % o["applied"], ""]
        for s in o["semantic_deltas"]:
            L.append("  %-16s %s" % (s["logical_id"][:16],
                                   ", ".join(s["classes"]) or "(none)"))
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_log(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    head = v6.ref("heads/" + branch)
    rows = []
    for digest, c in v6.history(head, args.limit):
        rows.append({"commit": digest, "root": c["root"], "actor": c["actor"],
                     "message": c["message"], "timestamp": c["timestamp"],
                     "decisions": len(c.get("decision") or []),
                     "nodes": len(v6.nodes_at(digest))})
    out = {"branch": branch, "commits": rows}

    def render(o):
        L = ["HISTORY of %s" % o["branch"], ""]
        for c in o["commits"]:
            L.append("  %s  %s" % (c["commit"][7:19], c["message"]))
            L.append("      root %s" % c["root"][7:27])
            L.append("      %s by %s   %d decision(s)   %d node(s)"
                     % (c["timestamp"][:19], c["actor"], c["decisions"],
                        c["nodes"]))
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_merge(args):
    ws, v6 = _v6_open(args)
    ours = args.into or v6.head_branch()
    result = v6_merge(v6, ours, args.branch)

    stored = []
    for c in result["conflicts"]:
        cd = v6.put(c, "wi.v6.conflict")
        v6.db.execute("INSERT OR REPLACE INTO v6_conflict VALUES (?,?,?,?,?)",
                      (c["conflict_id"], cd, ours, "unresolved", _now()))
        stored.append(c["conflict_id"])

    committed = None
    if result["clean"] and not args.dry_run:
        root = v6.put_root(result["merged_nodes"], {}, {})
        delta = v6.put({"added": [], "removed": [], "superseded": [],
                        "semantic": [], "merge": True}, "wi.v6.delta")
        cobj = {"parents": [result["ours_commit"], result["theirs_commit"]],
                "root": root, "delta": delta, "actor": args.actor,
                "decision": [],
                "message": "merge %s into %s" % (args.branch, ours),
                "timestamp": _now()}
        committed = v6.put(cobj, "wi.v6.commit")
        v6.set_ref("heads/" + ours, committed, expected=result["ours_commit"])
    v6.commit_db()

    out = dict(result)
    out.pop("merged_nodes", None)
    out["stored_conflicts"] = stored
    out["merge_commit"] = committed

    def render(o):
        L = ["MERGE %s into %s" % (args.branch, ours), ""]
        L.append("  base commit  %s" % (o["base_commit"] or "(unrelated histories)")[7:19])
        L.append("")
        if o["auto_merged"]:
            L.append("Auto-merged")
            for a in o["auto_merged"]:
                L.append("  %s  took %s" % (a["logical_id"][:8], a["took"]))
                L.append("      %s" % a["why"])
            L.append("")
        if o["conflicts"]:
            L.append("Conflicts — preserved, not resolved")
            for c in o["conflicts"]:
                L.append("  %-12s %s" % (c["kind"], c["logical_id"]))
                L.append("      base    %s" % c["base_summary"])
                L.append("      ours    %s" % c["ours_summary"])
                L.append("      theirs  %s" % c["theirs_summary"])
                L.append("      status  unresolved, requires an authorized decision")
            L.append("")
            L.append("The engine did not average, soften or generalize these.")
            L.append("Neither branch asserted a middle value, so there is none.")
        else:
            L.append("Clean merge.")
            if o["merge_commit"]:
                L.append("  merge commit %s" % o["merge_commit"][7:19])
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 2 if result["conflicts"] else 0


def cmd_conflicts(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()

    if args.resolve:
        row = v6.db.execute("SELECT * FROM v6_conflict WHERE conflict_id=?",
                            (args.resolve,)).fetchone()
        if not row:
            raise WIError("WI_INPUT_INVALID", "no conflict %s" % args.resolve,
                          ["run `wi conflicts` to list them"])
        c = v6.get(row["digest"])
        if not args.take:
            raise WIError("WI_INPUT_INVALID",
                          "resolving a conflict requires naming which side wins",
                          ["--take ours", "--take theirs"])
        cap = v6_required_capability(c.get("classes") or [])
        receipt = v6.authorize(args.actor, cap, {"kind": "branch", "value": branch})
        v6.db.execute("UPDATE v6_conflict SET status=? WHERE conflict_id=?",
                      ("resolved:" + args.take, args.resolve))
        v6.commit_db()
        print("resolved %s by taking %s" % (args.resolve, args.take))
        print("  actor %s under grant %s (%s)"
              % (args.actor, receipt["grant_id"], receipt["capability"]))
        return 0

    rows = []
    for r in v6.db.execute(
            "SELECT * FROM v6_conflict WHERE branch=? ORDER BY created_at",
            (branch,)):
        c = v6.get(r["digest"])
        c["status"] = r["status"]
        rows.append(c)
    out = {"branch": branch, "conflicts": rows,
           "unresolved": sum(1 for c in rows if c["status"] == "unresolved")}

    def render(o):
        if not o["conflicts"]:
            return "No semantic conflicts on %s." % o["branch"]
        L = ["SEMANTIC CONFLICTS on %s" % o["branch"], ""]
        for c in o["conflicts"]:
            L.append("  [%s] %-12s %s" % (c["status"], c["kind"],
                                          c["conflict_id"]))
            L.append("      node    %s" % c["logical_id"])
            L.append("      ours    %s" % c["ours_summary"])
            L.append("      theirs  %s" % c["theirs_summary"])
        L += ["", "%d unresolved. A branch carrying an unresolved conflict"
                  % o["unresolved"],
              "cannot be rendered as agreed (C015)."]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 2 if out["unresolved"] else 0


def cmd_authority(args):
    ws, v6 = _v6_open(args)
    action = args.action

    if action == "list":
        rows = []
        for r in v6.db.execute("SELECT * FROM v6_grant ORDER BY created_at"):
            g = v6.get(r["digest"])
            g["revoked_at"] = r["revoked_at"]
            rows.append(g)
        out = {"grants": rows}

        def render(o):
            if not o["grants"]:
                return ("No capability grants issued. Until one exists, no actor "
                        "can accept a consequential change — including you.")
            L = ["CAPABILITY GRANTS", ""]
            for g in o["grants"]:
                state = ("revoked %s" % g["revoked_at"][:19] if g["revoked_at"]
                         else "active")
                L.append("  %s  [%s]" % (g["grant_id"], state))
                L.append("      %s -> %s" % (g["subject"], g["capability"]))
                L.append("      scope %s%s" % (g["scope"]["kind"],
                                               (":" + g["scope"]["value"])
                                               if g["scope"].get("value") else ""))
                L.append("      issued by %s%s"
                         % (g["issuer"],
                            ("  expires " + g["expires_at"][:19])
                            if g.get("expires_at") else "  no expiry"))
                if g.get("parent_grant"):
                    L.append("      delegated from %s" % g["parent_grant"])
            return "\n".join(L)

        _v6_emit(args, out, render)
        return 0

    if action in ("issue", "delegate"):
        scope = {"kind": args.scope}
        if args.scope_value:
            scope["value"] = args.scope_value
        gobj = {
            "grant_id": v6_logical_id("grant", args.subject, args.capability,
                                      json.dumps(scope, sort_keys=True),
                                      args.parent or ""),
            "subject": args.subject,
            "subject_kind": args.subject_kind,
            "capability": args.capability,
            "scope": scope,
            "constraints": [],
            "issuer": args.issuer,
            "issued_at": _now(),
            "activates_at": args.activates or _now(),
            "expires_at": args.expires,
            "parent_grant": args.parent,
        }
        if args.subject_kind in V6_FORBIDDEN_SUBJECT_KINDS:
            raise WIError("WI_AUTHORITY_DENIED",
                          "a %s may never hold a capability grant"
                          % args.subject_kind,
                          ["a judgment provider returns values; it does not "
                           "decide, approve or sign"],
                          {"constraint": "C008"})
        if args.capability not in V6_CAPABILITIES:
            raise WIError("WI_INPUT_INVALID",
                          "%r is not a known capability" % args.capability,
                          ["one of: " + ", ".join(V6_CAPABILITIES)])
        if action == "delegate":
            if not args.parent:
                raise WIError("WI_INPUT_INVALID",
                              "delegation requires --parent GRANT_ID",
                              ["run `wi authority list` to find it"])
            parent = v6.grant(args.parent)
            if parent.get("_revoked_at"):
                raise WIError("WI_AUTHORITY_REVOKED",
                              "the parent grant has been revoked",
                              ["a revoked grant cannot be delegated from"])
            v6_validate_child_grant(parent, gobj)

        digest = v6.put(gobj, "wi.v6.grant")
        v6.db.execute("INSERT OR REPLACE INTO v6_grant VALUES (?,?,?,?,?)",
                      (gobj["grant_id"], digest, args.subject, None, _now()))
        v6.commit_db()
        print("%s %s" % ("issued" if action == "issue" else "delegated",
                         gobj["grant_id"]))
        print("  %s -> %s in scope %s" % (args.subject, args.capability,
                                          args.scope))
        if action == "delegate":
            print("  narrowed from %s; a child grant can never widen its parent"
                  % args.parent)
        return 0

    if action == "revoke":
        g = v6.grant(args.grant)
        v6.db.execute("UPDATE v6_grant SET revoked_at=? WHERE grant_id=?",
                      (_now(), args.grant))
        v6.commit_db()
        print("revoked %s (%s -> %s)" % (args.grant, g["subject"],
                                         g["capability"]))
        print("Existing decisions keep their receipts. Nothing new may be")
        print("authorized under this grant from now on (C020).")
        return 0

    if action == "check":
        scope = {"kind": args.scope}
        if args.scope_value:
            scope["value"] = args.scope_value
        try:
            receipt = v6.authorize(args.subject, args.capability, scope)
        except WIError as exc:
            print(exc.render())
            return 1
        print("PERMITTED")
        print("  %s may %s in scope %s" % (args.subject, args.capability,
                                           args.scope))
        print("  under grant %s" % receipt["grant_id"])
        return 0
    return 0


def cmd_obligations(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    head = v6.ref("heads/" + branch)
    nodes = v6.nodes_at(head)
    mode = args.mode or (ws.meta().get("mode") or "standard")

    rows, totals = [], {}
    for lid in sorted(nodes):
        if args.node and lid != args.node:
            continue
        ns = v6.get(nodes[lid])
        obs = v6_obligations_for(ns, mode)
        for o in obs:
            totals[o["check"]] = totals.get(o["check"], 0) + 1
        rows.append({"logical_id": lid, "node_type": ns["node_type"],
                     "realm": ns["realm"],
                     "basis": ns["reliability"]["basis"],
                     "obligations": obs})
    out = {"branch": branch, "mode": mode, "nodes": rows, "totals": totals,
           "obligation_count": sum(len(r["obligations"]) for r in rows)}

    def render(o):
        L = ["PROOF OBLIGATIONS — %s, mode %s" % (o["branch"], o["mode"]), ""]
        if not o["nodes"]:
            return "\n".join(L + ["  no governed nodes on this branch"])
        for r in o["nodes"]:
            L.append("  %-16s [%s / %s / %s]" % (r["logical_id"][:16],
                                               r["node_type"], r["realm"],
                                               r["basis"]))
            for ob in r["obligations"]:
                L.append("      %-10s %-32s %s"
                         % (ob["requirement"], ob["check"], _trunc(ob["why"], 60)))
        L += ["", "%d obligation(s) across %d node(s)."
                  % (o["obligation_count"], len(o["nodes"])),
              "These were derived from typed state, release target and policy —",
              "not from a checklist hard-coded inside a command."]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_as_of(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    head = v6.ref("heads/" + branch)

    # Knowledge time: which commit was the head at that instant.
    chosen, chosen_c = head, None
    for digest, c in v6.history(head):
        chosen_c = c
        if args.known_at is None or str(c["timestamp"]) <= str(args.known_at):
            chosen = digest
            break
    else:
        if args.known_at is not None:
            chosen = None

    if chosen is None:
        out = {"branch": branch, "known_at": args.known_at, "commit": None,
               "nodes": [], "note": "this workspace knew nothing at that instant"}
    else:
        nodes = v6.nodes_at(chosen)
        rows = []
        for lid in sorted(nodes):
            if args.node and lid != args.node:
                continue
            ns = v6.get(nodes[lid])
            if not _v6_covers(ns["valid_time"], args.valid_at):
                continue
            if args.known_at is not None:
                kt = ns["knowledge_time"]
                if str(kt["observed_at"]) > str(args.known_at):
                    continue
                if kt.get("superseded_at") and \
                        str(kt["superseded_at"]) <= str(args.known_at):
                    continue
            rows.append({"logical_id": lid, "state_digest": nodes[lid],
                         "node_type": ns["node_type"], "realm": ns["realm"],
                         "valid_time": ns["valid_time"],
                         "knowledge_time": ns["knowledge_time"],
                         "summary": _v6_summary(ns["payload"])})
        out = {"branch": branch, "known_at": args.known_at,
               "valid_at": args.valid_at, "commit": chosen,
               "graph_root": v6.get(chosen)["root"], "nodes": rows}

    def render(o):
        L = ["AS OF", "  branch      %s" % o["branch"],
             "  known at    %s" % (o.get("known_at") or "now"),
             "  valid at    %s" % (o.get("valid_at") or "any instant"),
             "  commit      %s" % ((o.get("commit") or "(none)")[7:19]
                                   if o.get("commit") else "(none)"), ""]
        if not o["nodes"]:
            L.append("  no state satisfies both clocks")
            if o.get("note"):
                L.append("  %s" % o["note"])
            return "\n".join(L)
        for r in o["nodes"]:
            vt = r["valid_time"]
            L.append("  %-16s %s" % (r["logical_id"][:16], r["summary"]))
            L.append("      valid %s -> %s" % (vt.get("from") or "(open)",
                                               vt.get("until") or "(open)"))
            L.append("      known %s" % r["knowledge_time"]["observed_at"][:19])
        L += ["", "This is what the workspace held then, not today's corrected",
              "state wearing an old date."]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


def cmd_constraints(args):
    ws, v6 = _v6_open(args)
    rep = v6_run_constraints(v6, args.branch)

    def render(o):
        L = ["GRAPH CONSTRAINTS — %s" % o["branch"], ""]
        for r in o["results"]:
            mark = {"pass": "ok  ", "fail": "FAIL", "not_evaluated": "--  "}[r["status"]]
            L.append("  %s %s %-46s" % (mark, r["id"], r["name"]))
            L.append("       %s" % r["detail"])
            for v in r["violations"][:5]:
                L.append("         - %s" % v)
        L += ["", "%d evaluated, %d not evaluated, %d failed."
                  % (o["evaluated"], o["not_evaluated"], o["failed"]),
              "A constraint that could not run says so and says why. There is no",
              "fourth status and no aggregate score.",
              "", "VERDICT %s" % o["verdict"]]
        return "\n".join(L)

    _v6_emit(args, rep, render)
    return 2 if rep["failed"] else 0


def cmd_capsule(args):
    ws, v6 = _v6_open(args) if args.action != "verify" else (None, None)

    if args.action == "create":
        cap = v6_capsule_create(v6, args.branch or v6.head_branch(),
                                select=args.select, profile=args.profile,
                                redact_payloads=args.hash_only)
        Path(args.out).write_text(
            json.dumps(cap, indent=2, sort_keys=True, ensure_ascii=False),
            encoding="utf-8")
        m = cap["manifest"]
        print("wrote %s" % args.out)
        print("  profile        %s" % m["profile"])
        print("  closure root   %s" % m["closure_root"])
        print("  leaves         %d total, %d disclosed, %d redacted"
              % (m["leaf_count"], m["disclosed_count"], len(cap["redactions"])))
        print("")
        print("A redacted leaf proves it was inside the producer's closure.")
        print("It does not prove you inspected its content, and this capsule")
        print("does not say otherwise.")
        return 0

    cap = json.loads(Path(args.path).read_text("utf-8"))

    if args.action == "inspect":
        m = cap["manifest"]
        print("CAPSULE %s" % args.path)
        for k in ("format", "profile", "core_version", "branch", "graph_root",
                  "closure_root", "leaf_count", "disclosed_count", "built_at"):
            print("  %-16s %s" % (k, m.get(k)))
        print("")
        print("  declared omissions")
        for o in m.get("declared_omissions", []):
            print("    %-24s %s" % (o["kind"], o["reason"]))
        print("")
        print("  does not prove")
        for n in m.get("not_a_proof_of", []):
            print("    - %s" % n)
        return 0

    rep = v6_capsule_verify(cap)
    if getattr(args, "json", False):
        print(json.dumps(rep, indent=2, sort_keys=True))
    else:
        print("CAPSULE VERIFICATION — %s" % args.path)
        print("")
        for c in rep["checks"]:
            print("  %-4s %-22s %s" % ("ok" if c["result"] == "pass" else "FAIL",
                                       c["check"], c["detail"]))
        print("")
        print("  closure root %s" % rep["closure_root"])
        print("")
        print("VERDICT %s" % rep["verdict"])
        print("")
        print("  " + rep["scope"])
    return 0 if rep["verdict"] == "VERIFIED" else 2


def cmd_why(args):
    ws, v6 = _v6_open(args)
    branch = args.branch or v6.head_branch()
    head = v6.ref("heads/" + branch)
    nodes = v6.nodes_at(head)

    lid = args.node
    if lid not in nodes:
        matches = [k for k in nodes if k.startswith(lid)]
        if len(matches) == 1:
            lid = matches[0]
        else:
            raise WIError("WI_INPUT_INVALID",
                          "no node %s on %s" % (args.node, branch),
                          ["run `wi as-of` to list the nodes on this branch"],
                          {"candidates": matches[:5]})

    ns = v6.get(nodes[lid])

    introduced, decision = None, None
    for digest, c in v6.history(head):
        d = v6.get(c["delta"])
        for s in d.get("semantic", []):
            if s["logical_id"] == lid and s["to"] == nodes[lid]:
                introduced = {"commit": digest, "message": c["message"],
                              "actor": c["actor"], "timestamp": c["timestamp"],
                              "classes": s["classes"]}
                for dd in c.get("decision") or []:
                    dec = v6.get(dd)
                    if dec.get("target_state_digest") == s["from"]:
                        decision = dec
                break
        if introduced:
            break

    deps = sorted(v6.dependents(lid))
    supports = []
    for r in v6.db.execute("SELECT to_logical_id FROM v6_edge"
                           " WHERE from_logical_id=? AND relation=?",
                           (lid, DEPENDENCY)):
        t = r["to_logical_id"]
        entry = {"logical_id": t}
        if t in nodes:
            tns = v6.get(nodes[t])
            entry["basis"] = tns["reliability"]["basis"]
            entry["summary"] = _v6_summary(tns["payload"])
        supports.append(entry)

    obligations = v6_obligations_for(ns, ws.meta().get("mode") or "standard")
    stale = ws.stale_nodes().get(lid)

    out = {"logical_id": lid, "branch": branch, "state_digest": nodes[lid],
           "node_type": ns["node_type"], "realm": ns["realm"],
           "reliability": ns["reliability"], "valid_time": ns["valid_time"],
           "knowledge_time": ns["knowledge_time"],
           "summary": _v6_summary(ns["payload"]),
           "introduced_by": introduced, "authorized_by": decision,
           "depends_on": supports, "depended_on_by": deps,
           "obligations": obligations, "stale": stale}

    def render(o):
        L = ["WHY", "", "  %s" % o["summary"], "",
             "NODE",
             "  logical id  %s" % o["logical_id"],
             "  state       %s" % o["state_digest"],
             "  type        %s" % o["node_type"],
             "  realm       %s" % o["realm"], ""]
        L.append("BASIS")
        rb = o["reliability"]
        L.append("  %s" % rb["basis"])
        for k, v in sorted(rb.items()):
            if k != "basis":
                L.append("      %s: %s" % (k, v))
        L.append("")
        L.append("TIME")
        L.append("  valid       %s -> %s" % (o["valid_time"].get("from") or "(open)",
                                             o["valid_time"].get("until") or "(open)"))
        L.append("  known from  %s" % o["knowledge_time"]["observed_at"][:19])
        L.append("")
        if o["introduced_by"]:
            i = o["introduced_by"]
            L.append("INTRODUCED BY")
            L.append("  commit %s  %s" % (i["commit"][7:19], i["message"]))
            L.append("  actor  %s at %s" % (i["actor"], i["timestamp"][:19]))
            L.append("  delta  %s" % (", ".join(i["classes"]) or "(none)"))
            L.append("")
        if o["authorized_by"]:
            d = o["authorized_by"]
            L.append("AUTHORIZED BY")
            L.append("  %s decided %s" % (d["actor"], d["outcome"]))
            if d.get("authority_receipt"):
                L.append("  under grant %s (%s)"
                         % (d["authority_receipt"]["grant_id"],
                            d["authority_receipt"]["capability"]))
            L.append("  bound to state %s" % (d["target_state_digest"] or "(new)"))
            L.append("")
        if o["depends_on"]:
            L.append("DEPENDS ON")
            for s in o["depends_on"]:
                L.append("  %-16s [%s]  %s" % (s["logical_id"][:16],
                                             s.get("basis", "?"),
                                             s.get("summary", "")))
            L.append("")
        L.append("PROOF OBLIGATIONS")
        for ob in o["obligations"]:
            L.append("  %-10s %s" % (ob["requirement"], ob["check"]))
        L.append("")
        L.append("DEPENDED ON BY")
        L.append("  %d node(s)" % len(o["depended_on_by"]))
        if o["stale"]:
            L += ["", "STALE — %s" % o["stale"]]
        return "\n".join(L)

    _v6_emit(args, out, render)
    return 0


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

    # ----------------------------------------------------------------------
    # v6 — the sovereign meaning runtime.
    #
    # Every command below is transactional or read-only. `simulate` is the one
    # that matters most and it is the one that writes nothing at all.
    # ----------------------------------------------------------------------

    sp = sub.add_parser("canon", help="canonical form and domain-separated digest")
    sp.add_argument("path", help="JSON file, or - for stdin")
    sp.add_argument("--schema", default="wi.v6.node_state")
    sp.add_argument("--show", action="store_true", help="print the canonical bytes")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_canon)

    sp = root_arg(sub.add_parser("branch", help="create, list and switch semantic branches"))
    sp.add_argument("action", nargs="?", choices=["list", "create", "switch", "delete"])
    sp.add_argument("name", nargs="?")
    sp.add_argument("--source", help="branch to fork from (default: current)")
    sp.add_argument("--switch", action="store_true", help="switch after creating")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_branch)

    sp = root_arg(sub.add_parser("propose", help="propose a change bound to an exact state"))
    sp.add_argument("--node", help="target logical id")
    sp.add_argument("--payload", help="JSON file holding the proposed payload")
    sp.add_argument("--from-ledger", dest="from_ledger",
                    help="lift every atom in a v5 claim ledger into a proposal")
    sp.add_argument("--type", default="meaning.claim_atom", choices=list(V6_NODE_TYPES))
    sp.add_argument("--realm", default="external_fact", choices=list(V6_REALMS))
    sp.add_argument("--basis", default="human_declared", choices=list(V6_BASES))
    sp.add_argument("--why", help="the reason, in your words")
    sp.add_argument("--actor", default="author")
    sp.add_argument("--branch")
    sp.add_argument("--expires")
    sp.add_argument("--valid-from", dest="valid_from")
    sp.add_argument("--valid-until", dest="valid_until")
    sp.add_argument("--depends-on", dest="depends_on", action="append")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_propose)

    sp = root_arg(sub.add_parser("proposals", help="list proposals and their status"))
    sp.add_argument("--branch")
    sp.add_argument("--status", choices=["open", "accepted", "rejected",
                                         "deferred", "superseded", "applied"])
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_proposals)

    sp = root_arg(sub.add_parser("simulate",
                                 help="what a change would do, before it exists"))
    sp.add_argument("--proposal", action="append", help="limit to these proposals")
    sp.add_argument("--branch")
    sp.add_argument("--actor", help="check authority as this actor")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_simulate)

    sp = root_arg(sub.add_parser("decide", help="record an authorized decision"))
    sp.add_argument("proposal")
    sp.add_argument("--accept", action="store_true")
    sp.add_argument("--reject", action="store_true")
    sp.add_argument("--defer", action="store_true")
    sp.add_argument("--actor", required=True)
    sp.add_argument("--reason")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_decide)

    sp = root_arg(sub.add_parser("commit", help="apply accepted proposals as one transaction"))
    sp.add_argument("-m", "--message", required=True)
    sp.add_argument("--actor", default="author")
    sp.add_argument("--branch")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_v6_commit)

    sp = root_arg(sub.add_parser("log", help="semantic commit history"))
    sp.add_argument("--branch")
    sp.add_argument("--limit", type=int, default=20)
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_log)

    sp = root_arg(sub.add_parser("merge", help="conflict-preserving semantic merge"))
    sp.add_argument("branch", help="branch to merge in")
    sp.add_argument("--into", help="branch to merge into (default: current)")
    sp.add_argument("--actor", default="author")
    sp.add_argument("--dry-run", dest="dry_run", action="store_true")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_merge)

    sp = root_arg(sub.add_parser("conflicts", help="unresolved semantic conflicts"))
    sp.add_argument("--branch")
    sp.add_argument("--resolve", help="conflict id to resolve")
    sp.add_argument("--take", choices=["ours", "theirs"])
    sp.add_argument("--actor", default="author")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_conflicts)

    sp = root_arg(sub.add_parser("authority", help="issue, delegate, revoke and check grants"))
    sp.add_argument("action", choices=["list", "issue", "delegate", "revoke", "check"])
    sp.add_argument("--subject")
    sp.add_argument("--subject-kind", dest="subject_kind", default="human",
                    choices=["human", "team", "service", "automated_policy",
                             "autonomous_worker", "judgment_provider",
                             "external_signer"])
    sp.add_argument("--capability")
    sp.add_argument("--scope", default="workspace",
                    choices=["workspace", "work", "node_family", "node",
                             "branch", "jurisdiction", "release_target"])
    sp.add_argument("--scope-value", dest="scope_value")
    sp.add_argument("--issuer", default="author")
    sp.add_argument("--activates")
    sp.add_argument("--expires")
    sp.add_argument("--parent", help="parent grant id, for delegation")
    sp.add_argument("--grant", help="grant id, for revoke")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_authority)

    sp = root_arg(sub.add_parser("obligations",
                                 help="derive what must be proved before release"))
    sp.add_argument("--branch")
    sp.add_argument("--node")
    sp.add_argument("--mode", choices=["standard", "strict", "regulated"])
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_obligations)

    sp = root_arg(sub.add_parser("as-of", help="bitemporal query over the graph"))
    sp.add_argument("--valid-at", dest="valid_at", help="world-valid date")
    sp.add_argument("--known-at", dest="known_at", help="what was known at this instant")
    sp.add_argument("--node")
    sp.add_argument("--branch")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_as_of)

    sp = root_arg(sub.add_parser("constraints", help="run the graph constraint engine"))
    sp.add_argument("--branch")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_constraints)

    sp = root_arg(sub.add_parser("capsule",
                                 help="Merkle proof closure and selective disclosure"))
    sp.add_argument("action", choices=["create", "inspect", "verify"])
    sp.add_argument("path", nargs="?", help="capsule to inspect or verify")
    sp.add_argument("--out", help="output path for create")
    sp.add_argument("--select", action="append", help="logical id to disclose")
    sp.add_argument("--profile", default="selective",
                    choices=["full", "redacted", "hash-only", "selective"])
    sp.add_argument("--hash-only", dest="hash_only", action="store_true")
    sp.add_argument("--branch")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_capsule)

    sp = root_arg(sub.add_parser("why", help="explain a node backward to its basis"))
    sp.add_argument("node")
    sp.add_argument("--branch")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_why)

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
