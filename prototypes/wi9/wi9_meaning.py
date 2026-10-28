#!/usr/bin/env python3
"""WI9-04 thought inventory and meaning diff: no silent change to what a writer meant.

Project owner: Antonio T. Smith Jr. / Density6 LLC

A revision can read better and say something else. This compares a writer's
own text with a candidate revision, sentence by sentence, and lists every
material change in meaning so the writer can accept or reject each one:

  NUMBER_CHANGED            a quantity differs
  DATE_CHANGED              a date or year differs
  PLANNED_TO_COMPLETED      something planned now reads as done
  ESTIMATE_TO_MEASURED      an approximate figure now reads as exact (and the reverse)
  NEGATION_FLIPPED          a statement now says the opposite
  STANCE_REVERSED           an opinion now points the other way
  CAUSE_ADDED / CAUSE_REMOVED / CAUSE_CHANGED   the stated reason moved
  UNCERTAINTY_REMOVED       a hedge was dropped, so the claim is stronger (and UNCERTAINTY_ADDED)
  CONCESSION_DROPPED        the writer's concession disappeared
  CHRONOLOGY_REVERSED       before became after
  OUTCOME_ADDED             a result appears that the writer never stated
  QUOTE_ALTERED             a quotation is not word for word, or was invented
  CLAIM_DROPPED             a sentence carrying a number, date, cause, stance or first person is gone
  NEW_AUTOBIOGRAPHICAL_FACT a new first-person sentence; accepting it needs a source in the writer's vault
  NEW_UNSOURCED_CLAIM       a new number, date or cause

The comparison is lexical and deterministic. It does not understand meaning;
it finds the places where meaning most often moves silently and puts each in
front of the writer. Decisions are recorded in the review ledger under the
writer's own v6 grant (wi9_ledger.py).

  inventory  the propositions in one text
  diff       every material delta between an original and a candidate (exit 3 if any)
  review     REVIEW only when every delta was accepted under a grant (and every
             new first-person fact is anchored in the vault)
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

SCHEMA = "wi9.meaning-diff/1"
MAX_CHARS = 500_000
MAX_SENTENCES = 5_000
ALIGN_THRESHOLD = 0.3
RESTRUCTURED = 0.8

WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*|\d[\d,]*(?:\.\d+)?")
NUMBER = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)(?![\w])")
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
                "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
                "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
                "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000, "dozen": 12, "half": 0.5}
MONTHS = ("january", "february", "march", "april", "may", "june", "july", "august", "september",
          "october", "november", "december")
ISO_DATE = re.compile(r"\b(1[6-9]\d\d|20\d\d|2100)(?:-(\d\d)(?:-(\d\d))?)?\b")
MONTH_DATE = re.compile(r"\b(" + "|".join(MONTHS) + r")(?:\s+(\d{1,2}))?(?:,?\s+(\d{4}))?\b", re.I)
PLANNED = re.compile(r"\b(?:will|shall|plan(?:s|ned)? to|intend(?:s|ed)? to|going to|aim(?:s|ed)? to|"
                     r"hope(?:s|d)? to|expect(?:s|ed)? to|next (?:spring|summer|autumn|fall|winter|year|month|"
                     r"week|quarter)|on (?:the|our|my) roadmap|roadmap|someday|eventually)\b", re.I)
ESTIMATE = re.compile(r"\b(?:about|around|roughly|approximately|nearly|almost|estimated|an estimated|"
                      r"or so|some|close to|upwards of|more than|less than|under|over)\b|~", re.I)
EXACT = re.compile(r"\b(?:exactly|precisely|measured|counted|recorded|to the day)\b", re.I)
HEDGE = re.compile(r"\b(?:may|might|could|perhaps|possibly|likely|unlikely|probably|seems?|appears?|"
                   r"suggests?|i think|i suspect|i believe|in my view|it is possible|maybe|tends? to)\b", re.I)
NEGATION = re.compile(r"\b(?:not|no|never|none|nothing|neither|nor|without|cannot)\b|n['’]t\b", re.I)
STANCE_POS = re.compile(r"\b(?:support|supports|agree|agrees|favou?r|recommend|recommends|endorse|"
                        r"right|worth|should|works|helps|better|best|good idea|in favou?r)\b", re.I)
STANCE_NEG = re.compile(r"\b(?:oppose|opposes|disagree|disagrees|against|reject|rejects|doubt|doubts|"
                        r"wrong|worse|worst|bad idea|shouldn['’]t|fails|hurts|mistake)\b", re.I)
CAUSE = re.compile(r"\b(?:because|due to|caused|causes|cause|led to|leads to|lead to|resulted in|"
                   r"results in|as a result|therefore|thus|so that|drove|drives|owing to|thanks to)\b", re.I)
# "still" and "while" are left out: they are far more often time words than concessions.
CONCESSION = re.compile(r"\b(?:although|though|admittedly|granted|to be fair|even so|"
                        r"on the other hand|that said|even if)\b", re.I)
BEFORE = re.compile(r"\b(?:before|earlier|prior to|first|until)\b", re.I)
AFTER = re.compile(r"\b(?:after|later|afterwards|subsequently|following|then)\b", re.I)
OUTCOME = re.compile(r"\b(?:doubled|tripled|halved|increased|decreased|grew|fell|rose|boosted|saved|won|"
                     r"cut|improved|reduced|lifted|dropped|sold out|succeeded|failed)\b", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{2,})[\"”]")
FIRST_PERSON = re.compile(r"\bI\b|\bI['’](?:m|ve|d|ll)\b|\b(?:me|my|mine|myself|we|our|ours|us)\b", re.I)
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "at", "by", "is", "was", "are",
        "were", "be", "been", "it", "this", "that", "as", "from", "but", "so", "its", "into", "than", "then",
        "these", "those", "there", "their", "they", "them", "has", "have", "had", "which", "who", "whom",
        "what", "when", "where", "also", "just", "very", "only", "own", "can", "did", "does", "our", "your",
        "his", "her", "she", "him", "you", "all", "any", "each", "more", "most", "such", "too"}

CAPABILITY = {
    "NUMBER_CHANGED": "claim.accept.quantity_change",
    "ESTIMATE_TO_MEASURED": "claim.accept.quantity_change",
    "MEASURED_TO_ESTIMATE": "claim.accept.quantity_change",
}
QUESTIONS = {
    "NUMBER_CHANGED": "Is the new number the one you mean, and where does it come from?",
    "DATE_CHANGED": "Did this happen on the new date?",
    "PLANNED_TO_COMPLETED": "Did this happen, or is it still a plan?",
    "ESTIMATE_TO_MEASURED": "Was this measured, or was it an estimate?",
    "MEASURED_TO_ESTIMATE": "Your figure was exact; should it now read as an estimate?",
    "NEGATION_FLIPPED": "The sentence now says the opposite. Is that what you mean?",
    "STANCE_REVERSED": "Your opinion now points the other way. Is that your view?",
    "CAUSE_ADDED": "A reason was added. Is it yours, and is it true?",
    "CAUSE_REMOVED": "Your reason was removed. Should it stay?",
    "CAUSE_CHANGED": "The reason changed. Which one is right?",
    "UNCERTAINTY_REMOVED": "You were unsure; the revision is certain. Are you?",
    "UNCERTAINTY_ADDED": "You were certain; the revision hedges. Should it?",
    "OUTCOME_ADDED": "A result was added. Did it happen, and how do you know?",
    "CONCESSION_DROPPED": "Your concession is gone. Did you mean to drop it?",
    "CHRONOLOGY_REVERSED": "The order of events changed. Which came first?",
    "QUOTE_ALTERED": "The quotation is not word for word. Quote exactly or paraphrase without quotation marks.",
    "CLAIM_DROPPED": "This sentence of yours is gone. Did you mean to cut it?",
    "NEW_AUTOBIOGRAPHICAL_FACT": "This is new first-person material. Did it happen, and is it in your vault?",
    "NEW_UNSOURCED_CLAIM": "This is a new factual claim. Where does it come from?",
}


def _sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sentences(text):
    """Sentence spans with exact offsets; decimals do not split, closing quotes stay attached."""
    out = []
    start = 0
    for m in re.finditer(r"(?<=[.!?])([\"”’)\]]*)\s+(?=[A-Z0-9\"“(\[])|\n\s*\n", text):
        cut = m.start() + len(m.group(1) or "")
        piece = text[start:cut].strip()
        if piece:
            s = text.index(piece, start)
            out.append((s, s + len(piece), piece))
        start = m.end()
    tail = text[start:].strip()
    if tail:
        s = text.index(tail, start)
        out.append((s, s + len(tail), tail))
    return out


def _numbers(text):
    years = {m.group(1) for m in ISO_DATE.finditer(text)}
    values = set()
    for m in NUMBER.finditer(text):
        raw = m.group(1).replace(",", "")
        if raw in years:
            continue
        try:
            values.add(float(raw))
        except ValueError:
            continue
    for word in re.findall(r"[a-z]+", text.lower()):
        if word in NUMBER_WORDS:
            values.add(float(NUMBER_WORDS[word]))
    return values


def _dates(text):
    found = set()
    for m in ISO_DATE.finditer(text):
        found.add("-".join(x for x in m.groups() if x))
    for m in MONTH_DATE.finditer(text):
        month = m.group(1).lower()
        if month == "may" and not (m.group(2) or m.group(3)):
            continue
        found.add(" ".join(x for x in (month, m.group(2), m.group(3)) if x))
    return found


IRREGULAR = {"built": "build", "made": "make", "took": "take", "wrote": "write", "ran": "run", "went": "go",
             "did": "do", "done": "do", "said": "say", "found": "find", "gave": "give", "got": "get",
             "began": "begin", "bought": "buy", "kept": "keep", "held": "hold", "led": "lead", "sold": "sell",
             "taught": "teach", "thought": "think", "won": "win", "left": "leave", "met": "meet", "paid": "pay",
             "spent": "spend", "sent": "send", "told": "tell", "knew": "know", "saw": "see", "came": "come"}
# Words that mark a plan, a hedge or an approximation are compared as features,
# not as content, so "we will build it" and "we built it" align and the change
# shows up as PLANNED_TO_COMPLETED rather than as two unrelated sentences.
MARKERS = {"will", "shall", "next", "plan", "plans", "planned", "going", "intend", "intends", "aim", "aims",
           "hope", "hopes", "expect", "expects", "roadmap", "about", "around", "roughly", "approximately",
           "nearly", "almost", "exactly", "precisely", "may", "might", "could", "perhaps", "possibly", "likely",
           "probably", "maybe", "think", "suspect", "seems", "appears", "because", "due", "caused", "causes",
           "therefore", "thus", "although", "though", "admittedly", "granted", "before", "after", "earlier",
           "later", "afterwards", "while", "still", "not", "never", "none", "nothing", "without"}


def _stem(word):
    word = IRREGULAR.get(word, word)
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 3 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word


def _content(text):
    return {_stem(w.lower()) for w in WORD.findall(text)
            if w.lower() not in STOP and w.lower() not in MARKERS and len(w) > 2}


def _cause_clause(text):
    m = CAUSE.search(text)
    return _content(text[m.end():]) if m else set()


def _stance(text):
    score = len(STANCE_POS.findall(text)) - len(STANCE_NEG.findall(text))
    if len(NEGATION.findall(text)) % 2:
        score = -score
    return (score > 0) - (score < 0)


def proposition(span):
    start, end, text = span
    return {"start": start, "end": end, "text": text,
            "numbers": sorted(_numbers(text)), "dates": sorted(_dates(text)),
            "planned": bool(PLANNED.search(text)), "estimate": bool(ESTIMATE.search(text)),
            "exact": bool(EXACT.search(text)), "hedged": bool(HEDGE.search(text)),
            "negations": len(NEGATION.findall(text)), "stance": _stance(text),
            "causal": bool(CAUSE.search(text)), "concession": bool(CONCESSION.search(text)),
            "before": bool(BEFORE.search(text)), "after": bool(AFTER.search(text)),
            "outcomes": sorted({w.lower() for w in OUTCOME.findall(text)}),
            "quotes": QUOTE.findall(text), "first_person": bool(FIRST_PERSON.search(text))}


def inventory(text):
    if len(text) > MAX_CHARS:
        raise ValueError("INPUT_EXCEEDS_%d_CHARS" % MAX_CHARS)
    spans = sentences(text)
    if len(spans) > MAX_SENTENCES:
        raise ValueError("TOO_MANY_SENTENCES")
    return [proposition(s) for s in spans]


def _protected(p):
    return bool(p["numbers"] or p["dates"] or p["causal"] or p["stance"] or p["first_person"] or p["quotes"]
                or p["planned"])


def _jaccard(a, b):
    return len(a & b) / len(a | b) if a and b else 0.0


def align(orig, cand):
    words_o = [_content(p["text"]) for p in orig]
    words_c = [_content(p["text"]) for p in cand]
    scored = sorted(((_jaccard(a, b), i, j) for i, a in enumerate(words_o) for j, b in enumerate(words_c)),
                    reverse=True)
    pairs, used_o, used_c = [], set(), set()
    for score, i, j in scored:
        if score < ALIGN_THRESHOLD:
            break
        if i in used_o or j in used_c:
            continue
        used_o.add(i)
        used_c.add(j)
        pairs.append((i, j))
    return sorted(pairs), [i for i in range(len(orig)) if i not in used_o], \
        [j for j in range(len(cand)) if j not in used_c]


def _delta(kind, o, c, detail):
    key = json.dumps([kind, o and o["text"], c and c["text"], detail], sort_keys=True)
    return {"id": hashlib.sha256(key.encode("utf-8")).hexdigest()[:16], "kind": kind, "material": True,
            "detail": detail, "question": QUESTIONS[kind],
            "original": {"start": o["start"], "end": o["end"], "text": o["text"]} if o else None,
            "candidate": {"start": c["start"], "end": c["end"], "text": c["text"]} if c else None,
            "required_capability": CAPABILITY.get(kind, "claim.accept"),
            "requires_source": kind == "NEW_AUTOBIOGRAPHICAL_FACT"}


def compare(original, candidate):
    orig, cand = inventory(original), inventory(candidate)
    all_orig_numbers = set().union(*[set(p["numbers"]) for p in orig]) if orig else set()
    all_cand_numbers = set().union(*[set(p["numbers"]) for p in cand]) if cand else set()
    all_orig_dates = set().union(*[set(p["dates"]) for p in orig]) if orig else set()
    all_orig_words = set().union(*[_content(p["text"]) for p in orig]) if orig else set()
    pairs, lost, added = align(orig, cand)
    deltas = []
    for i, j in pairs:
        o, c = orig[i], cand[j]
        on, cn = set(o["numbers"]), set(c["numbers"])
        if on != cn and ((on - cn) - all_cand_numbers or (cn - on) - all_orig_numbers):
            deltas.append(_delta("NUMBER_CHANGED", o, c, "%s -> %s" % (sorted(on), sorted(cn))))
        if set(o["dates"]) != set(c["dates"]) and (set(c["dates"]) - all_orig_dates or
                                                   set(o["dates"]) - set().union(*[set(p["dates"]) for p in cand])):
            deltas.append(_delta("DATE_CHANGED", o, c, "%s -> %s" % (o["dates"], c["dates"])))
        if o["planned"] and not c["planned"]:
            deltas.append(_delta("PLANNED_TO_COMPLETED", o, c, "the plan marker is gone"))
        if (on or cn) and o["estimate"] and not c["estimate"]:
            deltas.append(_delta("ESTIMATE_TO_MEASURED", o, c, "the approximation is gone"))
        elif (on or cn) and not o["exact"] and c["exact"]:
            deltas.append(_delta("ESTIMATE_TO_MEASURED", o, c, "the figure now reads as exact"))
        elif (on or cn) and o["exact"] and not o["estimate"] and c["estimate"]:
            deltas.append(_delta("MEASURED_TO_ESTIMATE", o, c, "an exact figure now reads as approximate"))
        if o["stance"] and c["stance"] and o["stance"] != c["stance"]:
            deltas.append(_delta("STANCE_REVERSED", o, c, "stance %+d -> %+d" % (o["stance"], c["stance"])))
        elif o["negations"] % 2 != c["negations"] % 2:
            deltas.append(_delta("NEGATION_FLIPPED", o, c, "negations %d -> %d" % (o["negations"], c["negations"])))
        if o["causal"] and not c["causal"]:
            deltas.append(_delta("CAUSE_REMOVED", o, c, "the stated reason is gone"))
        elif c["causal"] and not o["causal"]:
            deltas.append(_delta("CAUSE_ADDED", o, c, "a reason appears that was not there"))
        elif o["causal"] and _jaccard(_cause_clause(o["text"]), _cause_clause(c["text"])) < 0.5:
            deltas.append(_delta("CAUSE_CHANGED", o, c, "the reason after the causal word differs"))
        if set(c["outcomes"]) - set(o["outcomes"]):
            deltas.append(_delta("OUTCOME_ADDED", o, c, "a result appears: %s" % ", ".join(
                sorted(set(c["outcomes"]) - set(o["outcomes"])))))
        if o["hedged"] and not c["hedged"]:
            deltas.append(_delta("UNCERTAINTY_REMOVED", o, c, "the hedge is gone"))
        elif c["hedged"] and not o["hedged"]:
            deltas.append(_delta("UNCERTAINTY_ADDED", o, c, "a hedge appears"))
        if o["concession"] and not c["concession"]:
            deltas.append(_delta("CONCESSION_DROPPED", o, c, "the concession word is gone"))
        if (o["before"] and not o["after"] and c["after"] and not c["before"]) or \
                (o["after"] and not o["before"] and c["before"] and not c["after"]):
            deltas.append(_delta("CHRONOLOGY_REVERSED", o, c, "before/after swapped"))
        if c["quotes"] and any(q not in original for q in c["quotes"]):
            deltas.append(_delta("QUOTE_ALTERED", o, c, "quoted words that are not in your text"))
        elif o["quotes"] and not c["quotes"] and any(q not in c["text"] for q in o["quotes"]):
            deltas.append(_delta("QUOTE_ALTERED", o, c, "your quotation was paraphrased"))
    for i in lost:
        o = orig[i]
        if o["concession"]:
            deltas.append(_delta("CONCESSION_DROPPED", o, None, "the sentence holding a concession is gone"))
        elif _protected(o):
            deltas.append(_delta("CLAIM_DROPPED", o, None, "a sentence carrying meaning is gone"))
    for j in added:
        c = cand[j]
        new_numbers = set(c["numbers"]) - all_orig_numbers
        new_dates = set(c["dates"]) - all_orig_dates
        contained = (len(_content(c["text"]) & all_orig_words) / max(1, len(_content(c["text"]))))
        if c["first_person"] and (contained < RESTRUCTURED or new_numbers or new_dates):
            deltas.append(_delta("NEW_AUTOBIOGRAPHICAL_FACT", None, c, "first-person material not in your text"))
        elif new_numbers or new_dates or (c["causal"] and contained < RESTRUCTURED):
            deltas.append(_delta("NEW_UNSOURCED_CLAIM", None, c, "new figures, dates or reasons"))
        elif c["quotes"] and any(q not in original for q in c["quotes"]):
            deltas.append(_delta("QUOTE_ALTERED", None, c, "quoted words that are not in your text"))
    return {"schema": SCHEMA, "original_sha256": _sha(original), "candidate_sha256": _sha(candidate),
            "pair_sha256": _sha(_sha(original) + _sha(candidate)),
            "inventory": {"original": len(orig), "candidate": len(cand), "aligned": len(pairs),
                          "dropped": len(lost), "added": len(added)},
            "deltas": deltas, "status": "HOLD" if deltas else "REVIEW",
            "release_authorized": False,
            "limitations": ["Lexical comparison: it finds where meaning often moves, it does not understand it.",
                            "A delta the writer accepts is their decision, not a check that it is true."]}


def review(original, candidate, ledger, store, vault=None, claims=None, now=None):
    from wi9_ledger import verify
    from wi9_fs import StoreRefusal
    report = compare(original, candidate)
    issues = []
    try:
        checked = verify(ledger, store, report["pair_sha256"], "meaning", now=now)
    except StoreRefusal as exc:
        return dict(report, status="HOLD", issues=[{"code": exc.code, "detail": str(exc)}])
    issues.extend({"code": i["code"], "delta": i.get("item"), "detail": i["detail"]} for i in checked["issues"])
    anchored = set()
    if vault and claims:
        from wi9_vault import Vault, check_claims
        doc = json.loads(Path(claims).read_text(encoding="utf-8"))
        v = Vault(vault)
        try:
            vault_report = check_claims(v, doc)
        finally:
            v.close()
        by_id = {c.get("id"): c for c in doc.get("claims", []) if isinstance(c, dict)}
        for r in vault_report["claims"]:
            if r["state"] == "anchored" and r["claim"] in by_id:
                anchored.add(" ".join(str(by_id[r["claim"]].get("text", "")).split()))
    wa = None
    for delta in report["deltas"]:
        entry = checked["effective"].get(("meaning", report["pair_sha256"], delta["id"]))
        if entry is None:
            issues.append({"code": "DELTA_UNDECIDED", "delta": delta["id"], "detail": delta["question"]})
            continue
        if wa is None:
            from wi9_ledger import _authorship
            wa = _authorship()._wi_module()
        if not wa.v6_capability_covers(entry["grant"]["capability"], delta["required_capability"]):
            issues.append({"code": "DELTA_CAPABILITY_INSUFFICIENT", "delta": delta["id"],
                           "detail": "this change needs %s; the decision was made under %s"
                           % (delta["required_capability"], entry["grant"]["capability"])})
            continue
        delta["decision"] = {"outcome": entry["decision"], "actor": entry["actor"], "entry": entry["hash"]}
        if entry["decision"] == "reject":
            issues.append({"code": "DELTA_REJECTED", "delta": delta["id"],
                           "detail": "the writer rejected this change; revise the candidate"})
        elif delta["requires_source"] and " ".join(delta["candidate"]["text"].split()) not in anchored:
            issues.append({"code": "DELTA_NEEDS_SOURCE", "delta": delta["id"],
                           "detail": "accepting new first-person material needs an anchored claim in your vault"})
    report["issues"] = issues
    report["status"] = "HOLD" if issues else "REVIEW"
    return report


def _read(path):
    p = Path(path)
    if p.is_symlink() or not p.is_file():
        raise ValueError("NOT_A_FILE: %s" % path)
    if p.stat().st_size > MAX_CHARS * 4:
        raise ValueError("FILE_TOO_LARGE: %s" % path)
    return p.read_text(encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    inv = sub.add_parser("inventory", help="the propositions in one text")
    inv.add_argument("--input", required=True)
    for name in ("diff", "review"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--original", required=True, help="your text")
        cmd.add_argument("--candidate", required=True, help="the revision")
    rev = sub.choices["review"]
    rev.add_argument("--ledger", required=True)
    rev.add_argument("--authority-store", dest="store", required=True)
    rev.add_argument("--vault", help="your firsthand vault, for new first-person material")
    rev.add_argument("--claims", help="a wi9.vault-claims/1 file naming that material")
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            result = {"schema": "wi9.thought-inventory/1", "status": "REVIEW",
                      "propositions": inventory(_read(args.input))}
        elif args.command == "diff":
            result = compare(_read(args.original), _read(args.candidate))
        else:
            result = review(_read(args.original), _read(args.candidate), args.ledger, args.store,
                            args.vault, args.claims)
    except (OSError, ValueError, UnicodeError, TypeError, KeyError) as exc:
        result = {"status": "HOLD", "issues": [{"code": "MEANING_ERROR", "detail": "%s: %s" % (type(exc).__name__, exc)}],
                  "release_authorized": False}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 3 if result["status"] == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
