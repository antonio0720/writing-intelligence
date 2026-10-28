#!/usr/bin/env python3
"""WI9-05C structural diagnostics: repeated openings, hollow contrast, template paragraphs.

Project owner: Antonio T. Smith Jr. / Density6 LLC

The phrase catalog looks at words. These checks look at shape: sentences that
all start the same way, a contrast whose two halves are both abstractions,
paragraphs poured into one mould, three-item lists on every page, and a
sentence that says the previous one again. Each finding is a question for
the writer with an exact span. None is a verdict on who wrote the text, none
is a quality score, and nothing here rewrites anything. A contrast with a
concrete difference in it, or a list the content actually has three of, is
left alone.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCHEMA = "wi9.structure.report/1"
MAX_CHARS = 500_000
MAX_FINDINGS_PER_CHECK = 200
REPEATED_OPENING_MIN = 3
TEMPLATE_MIN_PARAGRAPHS = 4
TRIAD_MIN = 3
RESTATEMENT_JACCARD = 0.6

TRANSITIONS = {"first", "firstly", "second", "secondly", "third", "thirdly", "moreover", "additionally",
               "furthermore", "finally", "also", "next", "lastly", "however", "importantly", "ultimately"}
CLOSERS = re.compile(r"^(?:this|ultimately|in short|in the end|that is why|that's why|in summary|"
                     r"ultimately,|the result|the takeaway|the lesson)\b", re.I)
CONTRAST = [
    re.compile(r"\b(?:it|this|that)(?:'s| is| was)? not (?:about |just |only |merely )?(?P<x>[^.,;:!?]{2,60})"
               r"[,;.\-— ]+(?:but |it(?:'s| is| was) )(?:about )?(?P<y>[^.,;:!?]{2,60})", re.I),
    re.compile(r"\bless about (?P<x>[^.,;:!?]{2,60}) and more about (?P<y>[^.,;:!?]{2,60})", re.I),
    re.compile(r"\bnot (?:because of )?(?P<x>[^.,;:!?]{2,40}), but (?:because of )?(?P<y>[^.,;:!?]{2,40})", re.I),
]
CONCRETE = re.compile(r"\d|[A-Z][a-z]+\s[A-Z][a-z]+|\b(?:percent|dollars?|days?|hours?|weeks?|months?|"
                      r"years?|miles?|pounds?|kg|km|cm|minutes?)\b")
TRIAD = re.compile(r"\b(\w+(?:\s\w+){0,2}), (\w+(?:\s\w+){0,2}),? and (\w+(?:\s\w+){0,2})\b")
WORD = re.compile(r"[A-Za-z][A-Za-z'-]+")
STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "at", "by", "is", "was", "are",
        "were", "be", "it", "this", "that", "as", "from", "but", "so", "its", "we", "our", "you", "your"}


def _sentence_spans(text):
    out, start = [], 0
    for m in re.finditer(r"(?<=[.!?])[\"”’)\]]*\s+(?=[A-Z0-9\"“(\[])|\n\s*\n", text):
        piece = text[start:m.start()].strip()
        if piece:
            s = text.index(piece, start)
            out.append((s, s + len(piece)))
        start = m.end()
    tail = text[start:].strip()
    if tail:
        s = text.index(tail, start)
        out.append((s, s + len(tail)))
    return out


def _paragraph_spans(text):
    out = []
    for m in re.finditer(r"[^\n](?:.|\n(?!\s*\n))*", text):
        if m.group(0).strip() and not m.group(0).lstrip().startswith(("#", "```", ">", "|", "- ", "* ")):
            out.append((m.start(), m.end()))
    return out


def _opening(text, n=2):
    words = [w.lower() for w in WORD.findall(text)[:n]]
    return " ".join(words) if len(words) == n else None


def _content(text):
    return {w.lower() for w in WORD.findall(text) if w.lower() not in STOP and len(w) > 2}


def _finding(code, start, end, text, question, **extra):
    item = {"code": code, "start": start, "end": end, "excerpt": text[start:end][:240], "question": question}
    item.update(extra)
    return item


def repeated_openings(text, sentences):
    groups = defaultdict(list)
    for start, end in sentences:
        key = _opening(text[start:end])
        if key:
            groups[key].append((start, end))
    out = []
    for key, spans in groups.items():
        if len(spans) >= REPEATED_OPENING_MIN:
            for start, end in spans[:MAX_FINDINGS_PER_CHECK]:
                out.append(_finding("REPEATED_OPENING", start, end, text,
                                    "%d sentences open with \"%s\". Does each one need that start?"
                                    % (len(spans), key), opening=key, count=len(spans)))
    return out


def hollow_contrasts(text):
    out = []
    for pattern in CONTRAST:
        for m in pattern.finditer(text):
            x, y = m.group("x"), m.group("y")
            if CONCRETE.search(x) or CONCRETE.search(y):
                continue  # a contrast with a concrete difference in it is doing work
            if len(_content(x)) > 4 or len(_content(y)) > 4:
                continue
            out.append(_finding("HOLLOW_CONTRAST", m.start(), m.end(), text,
                                "Both sides are abstractions. What is the concrete difference, if there is one?"))
            if len(out) >= MAX_FINDINGS_PER_CHECK:
                return out
    return out


def template_paragraphs(text, sentences):
    paragraphs = _paragraph_spans(text)
    if len(paragraphs) < TEMPLATE_MIN_PARAGRAPHS:
        return []
    counts, openers, closers = [], 0, 0
    for p_start, p_end in paragraphs:
        inside = [(s, e) for s, e in sentences if p_start <= s < p_end]
        counts.append(len(inside))
        first = WORD.findall(text[p_start:p_end])[:1]
        if first and first[0].lower() in TRANSITIONS:
            openers += 1
        if inside and CLOSERS.match(text[inside[-1][0]:inside[-1][1]]):
            closers += 1
    uniform = max(counts) - min(counts) <= 1 and min(counts) >= 2
    if uniform and (openers >= 3 or closers >= 3):
        return [_finding("TEMPLATE_PARAGRAPHS", paragraphs[0][0], paragraphs[-1][1], text,
                         "%d paragraphs of %d-%d sentences, %d opening on a transition word and %d closing on "
                         "a summary line. Is the shape coming from the argument, or from a mould?"
                         % (len(paragraphs), min(counts), max(counts), openers, closers),
                         sentence_counts=counts, transition_openings=openers, summary_closings=closers)]
    return []


def triads(text):
    hits = list(TRIAD.finditer(text))
    if len(hits) < TRIAD_MIN:
        return []
    return [_finding("TRIAD_RHYTHM", m.start(), m.end(), text,
                     "%d three-item lists. Does the content have three of each, or is the rhythm doing the work?"
                     % len(hits), count=len(hits)) for m in hits[:MAX_FINDINGS_PER_CHECK]]


def restatements(text, sentences):
    out = []
    for (a_start, a_end), (b_start, b_end) in zip(sentences, sentences[1:]):
        a, b = _content(text[a_start:a_end]), _content(text[b_start:b_end])
        if len(a) >= 4 and len(b) >= 4 and len(a & b) / len(a | b) >= RESTATEMENT_JACCARD:
            out.append(_finding("RESTATEMENT", b_start, b_end, text,
                                "This sentence says much of the previous one again. What does it add?"))
            if len(out) >= MAX_FINDINGS_PER_CHECK:
                break
    return out


def analyze(text):
    if not isinstance(text, str):
        raise TypeError("INPUT_NOT_TEXT")
    if len(text) > MAX_CHARS:
        raise ValueError("INPUT_EXCEEDS_%d_CHARS" % MAX_CHARS)
    sentences = _sentence_spans(text)
    findings = (repeated_openings(text, sentences) + hollow_contrasts(text) + template_paragraphs(text, sentences)
                + triads(text) + restatements(text, sentences))
    findings.sort(key=lambda f: (f["start"], f["end"], f["code"]))
    by_code = defaultdict(int)
    for f in findings:
        by_code[f["code"]] += 1
    return {"schema": SCHEMA, "status": "REVIEW", "sentence_count": len(sentences),
            "finding_count": len(findings), "by_code": dict(sorted(by_code.items())), "findings": findings,
            "release_authorized": False,
            "scope": "Editorial questions about shape. Not authorship classification, not a quality score, "
                     "and never a rewrite."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="a UTF-8 text file")
    args = parser.parse_args(argv)
    try:
        path = Path(args.input)
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_CHARS * 4:
            raise ValueError("INPUT_NOT_A_BOUNDED_FILE")
        result = analyze(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError, TypeError) as exc:
        result = {"status": "HOLD", "error": str(exc), "release_authorized": False}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 3 if result["status"] == "HOLD" else 0


if __name__ == "__main__":
    sys.exit(main())
