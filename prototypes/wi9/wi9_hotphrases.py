#!/usr/bin/env python3
"""Meaning-led hot-phrase editorial diagnostics for Writing Intelligence v9.

Project author: Antonio T. Smith Jr. / Density6 LLC.
Reports cliches and rhetorical patterns; does NOT determine human/AI origin,
rewrite text, bypass detectors, or authorize publication.
"""
import argparse
import bisect
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_PACK = Path(__file__).resolve().parent / 'rules' / 'v9_hotphrases.json'
MAX_CHARS = 500_000
MAX_HITS = 500
MAX_DOCUMENT_CHARS = 20_000_000   # a long manuscript, scanned in chunks
CHUNK_CHARS = 100_000
MIN_CHUNK_CHARS = 2_000
ONE_TO_ONE = str.maketrans({'\u2018': "'", '\u2019': "'", '\u2010': '-', '\u2011': '-', '\u2013': '-', '\u2014': '-', '\u00a0': ' '})


def read_rules(path=DEFAULT_PACK):
    # Only load trusted, local editorial rule packs. An untrusted regex pack can
    # consume excessive CPU. Validate size and rule count before compiling.
    raw = Path(path).read_bytes()
    if len(raw) > 250_000:
        raise ValueError('RULE_PACK_OVERSIZE')
    pack = json.loads(raw.decode('utf-8'))
    if not isinstance(pack, dict) or pack.get('schema') != 'wi9.hotphrases/1':
        raise ValueError('RULE_PACK_SCHEMA_INVALID')
    rules = pack.get('rules')
    if not isinstance(rules, list) or not rules or len(rules) > 1000:
        raise ValueError('RULE_COUNT_INVALID')
    seen = set()
    checked = []
    for r in rules:
        if not isinstance(r, dict):
            raise ValueError('RULE_NOT_OBJECT')
        identifier = r.get('id')
        if not isinstance(identifier, str) or not re.fullmatch(r'[a-z][a-z0-9_]{2,75}', identifier) or identifier in seen:
            raise ValueError('RULE_ID_INVALID_OR_DUPLICATE')
        seen.add(identifier)
        expression, kind = r.get('expression'), r.get('kind')
        if kind not in ('literal', 'regex') or not isinstance(expression, str) or not expression or len(expression) > 260:
            raise ValueError('RULE_PATTERN_INVALID')
        if not isinstance(r.get('category'), str) or not isinstance(r.get('question'), str):
            raise ValueError('RULE_METADATA_INCOMPLETE')
        # Existing patterns are trusted, pre-reviewed local regex. Python's re
        # has no timeout; do not ingest untrusted user-defined regex into this path.
        pattern = (r'(?<!\w)' + re.escape(expression).replace(r'\ ', r'[ \t]+') + r'(?!\w)') if kind == 'literal' else expression
        re.compile(pattern, flags=re.I | re.M)
        checked.append(dict(r, _compiled=re.compile(pattern, flags=re.I | re.M)))
    return checked


def excluded_intervals(text, include_quoted=False):
    """Find Markdown fences/code/URLs; optionally skip quotations and blockquotes.

    This is a *heuristic* Markdown mask, not a conformant CommonMark parser.
    The include_quoted flag intentionally affects quoted/blockquote text only.
    """
    ranges = []
    active = None
    offset = 0
    for line in text.splitlines(keepends=True):
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if active is not None:
            ranges.append((offset, offset + len(line)))
            if marker is not None and marker.group(1)[0] == active[0] and len(marker.group(1)) >= len(active):
                active = None
        elif marker is not None:
            active = marker.group(1)
            ranges.append((offset, offset + len(line)))
        elif not include_quoted and re.match(r'^\s*>', line):
            ranges.append((offset, offset + len(line)))
        offset += len(line)
    # inline snippets, hyperlinks and quotations: remove direct textual data,
    # not the author's surrounding analysis.
    for pattern in (r'`[^`\n]+`', r'https?://[^\s)\]>]+', r'\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b'):
        ranges.extend(m.span() for m in re.finditer(pattern, text))
    if not include_quoted:
        for pattern in (r'\u201c[^\u201d\n]{1,400}\u201d', r'"[^"\n]{1,400}"'):
            ranges.extend(m.span() for m in re.finditer(pattern, text))
    merged = []
    for lo, hi in sorted(ranges):
        if merged and lo <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
    return [tuple(r) for r in merged]


def _masked(span, intervals, starts=None):
    """True when span overlaps a mask interval. Intervals are merged and sorted,
    so one bisect finds the only interval that can overlap: O(log n) per match
    (independent review finding 8)."""
    start, end = span
    if starts is None:
        starts = [lo for lo, _ in intervals]
    i = bisect.bisect_right(starts, start) - 1
    for j in (i, i + 1):
        if 0 <= j < len(intervals):
            lo, hi = intervals[j]
            if hi > start and lo < end:
                return True
    return False


def scan_text(text, pack=DEFAULT_PACK, include_quoted=False, max_hits=MAX_HITS):
    """Structured warnings with original code-point offsets and line/column.

    Rules are never 'AI markers'. All matches are suggestions for human
    editorial judgment and can be retained when genre, facts or voice warrant.
    """
    if not isinstance(text, str):
        raise TypeError('INPUT_NOT_TEXT')
    if len(text) > MAX_CHARS:
        raise ValueError('INPUT_EXCEEDS_500000_CHARS')
    if not isinstance(max_hits, int) or not 1 <= max_hits <= MAX_HITS:
        raise ValueError('MAX_HITS_INVALID')
    rules = read_rules(pack)
    mask = excluded_intervals(text, include_quoted)
    mask_starts = [lo for lo, _ in mask]
    normalized = text.translate(ONE_TO_ONE)  # Code-point offsets remain stable.
    newlines = [-1] + [m.start() for m in re.finditer('\n', text)]
    findings = []
    for rule in rules:
        for match in rule['_compiled'].finditer(normalized):
            if _masked(match.span(), mask, mask_starts):
                continue
            start, end = match.span()
            line_ix = bisect.bisect_left(newlines, start)
            line = max(line_ix, 1)
            col = start - newlines[line - 1]
            findings.append({'id': rule['id'], 'category': rule['category'], 'severity': rule['severity'],
                             'line': line, 'column': col, 'start': start, 'end': end,
                             'excerpt': text[start:end], 'question': rule['question'],
                             'context_note': rule.get('context_note', '')})
            # Bound matching for a pathological repetition-heavy input.
            if len(findings) >= max_hits:
                break
        if len(findings) >= max_hits:
            break
    findings.sort(key=lambda x: (x['start'], x['end'], x['id']))
    cats = Counter(f['category'] for f in findings)
    repeated = defaultdict(list)
    for f in findings:
        repeated[f['id']].append(f['start'])
    repeated_ids = {key: len(positions) for key, positions in repeated.items() if len(positions) >= 2}
    words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    return {'schema': 'wi9.hotphrases.report/1', 'owner': 'Antonio T. Smith Jr.',
            'document_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'rules_sha256': hashlib.sha256(Path(pack).read_bytes()).hexdigest(),
            'word_count': len(words), 'rule_count': len(rules), 'finding_count': len(findings),
            'density_per_1000_words': round(1000 * len(findings) / max(1, len(words)), 2),
            'by_category': dict(sorted(cats.items())), 'repeated_rule_hits': repeated_ids,
            'findings': findings, 'truncated': len(findings) >= max_hits,
            'release_authorized': False,
            'interpretation': 'Editorial review candidates. Phrase matches do not prove machine authorship and do not demand rewriting. No detector optimization.'}


def _cut_points(text, mask, size):
    """Chunk boundaries at paragraph breaks outside any masked span (code fences,
    quotations), so a phrase or a fence is never split between two chunks."""
    starts = [lo for lo, _ in mask]
    cuts, pos = [0], 0
    while len(text) - pos > size:
        window_end = pos + size
        cut = None
        for sep in ('\n\n', '\n', ' '):
            probe = text.rfind(sep, pos + size // 2, window_end)
            while probe != -1 and _masked((probe, probe + len(sep)), mask, starts):
                probe = text.rfind(sep, pos + size // 2, probe)
            if probe != -1:
                cut = probe + len(sep)
                break
        if cut is None:
            # No safe break in the window: never cut inside a masked span (a code
            # fence or quotation longer than the window); end the chunk after it.
            cut = window_end
            i = bisect.bisect_right(starts, window_end) - 1
            if 0 <= i < len(mask) and mask[i][0] < window_end < mask[i][1]:
                cut = mask[i][1]
        if cut <= pos:
            cut = window_end
        cuts.append(cut)
        pos = cut
    cuts.append(len(text))
    return cuts


def scan_document(text, pack=DEFAULT_PACK, include_quoted=False, chunk_chars=CHUNK_CHARS):
    """Scan a long manuscript in chunks with global offsets; never drops findings silently.

    A chunk that reaches the per-scan cap is halved and rescanned. Only a chunk
    still at the cap at MIN_CHUNK_CHARS (pathological repetition) is reported
    as incomplete, by its exact range, and the report says `complete: false`.
    """
    if not isinstance(text, str):
        raise TypeError('INPUT_NOT_TEXT')
    if len(text) > MAX_DOCUMENT_CHARS:
        raise ValueError('INPUT_EXCEEDS_%d_CHARS' % MAX_DOCUMENT_CHARS)
    mask = excluded_intervals(text, include_quoted)
    cuts = _cut_points(text, mask, chunk_chars)
    pending = [(cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1)]
    newlines = [-1] + [m.start() for m in re.finditer('\n', text)]
    findings, chunks, incomplete = [], [], []
    rules = None
    while pending:
        lo, hi = pending.pop(0)
        part = scan_text(text[lo:hi], pack=pack, include_quoted=include_quoted, max_hits=MAX_HITS)
        rules = part['rule_count']
        if part['truncated'] and hi - lo > MIN_CHUNK_CHARS:
            sub = _cut_points(text[lo:hi], excluded_intervals(text[lo:hi], include_quoted), (hi - lo) // 2)
            pending[0:0] = [(lo + sub[i], lo + sub[i + 1]) for i in range(len(sub) - 1)]
            continue
        if part['truncated']:
            incomplete.append({'start': lo, 'end': hi})
        chunks.append({'start': lo, 'end': hi, 'finding_count': part['finding_count'],
                       'truncated': part['truncated']})
        for f in part['findings']:
            f = dict(f, start=f['start'] + lo, end=f['end'] + lo)
            line = max(bisect.bisect_left(newlines, f['start']), 1)
            f['line'], f['column'] = line, f['start'] - newlines[line - 1]
            findings.append(f)
    findings.sort(key=lambda x: (x['start'], x['end'], x['id']))
    chunks.sort(key=lambda c: c['start'])
    cats = Counter(f['category'] for f in findings)
    repeated = Counter(f['id'] for f in findings)
    words = re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE)
    return {'schema': 'wi9.hotphrases.report/1', 'owner': 'Antonio T. Smith Jr.',
            'document_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest(),
            'rules_sha256': hashlib.sha256(Path(pack).read_bytes()).hexdigest(),
            'word_count': len(words), 'rule_count': rules if rules is not None else len(read_rules(pack)),
            'finding_count': len(findings),
            'density_per_1000_words': round(1000 * len(findings) / max(1, len(words)), 2),
            'by_category': dict(sorted(cats.items())),
            'repeated_rule_hits': {k: n for k, n in repeated.items() if n >= 2},
            'findings': findings, 'chunks': chunks, 'complete': not incomplete,
            'incomplete_ranges': incomplete, 'truncated': bool(incomplete),
            'release_authorized': False,
            'interpretation': 'Editorial review candidates. Phrase matches do not prove machine authorship and do not demand rewriting. No detector optimization.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    scan = sub.add_parser('scan')
    scan.add_argument('--input', required=True, help='Existing UTF-8 text file')
    scan.add_argument('--rules', default=str(DEFAULT_PACK), help='Trusted local rule pack')
    scan.add_argument('--include-quotes', action='store_true')
    scan.add_argument('--max-hits', type=int, default=MAX_HITS)
    scan.add_argument('--format', choices=('json', 'text'), default='json')
    args = parser.parse_args(argv)
    try:
        path = Path(args.input)
        if path.stat().st_size > MAX_DOCUMENT_CHARS * 4:
            raise ValueError('INPUT_FILE_OVERSIZE')
        text = path.read_text(encoding='utf-8')
        result = None
        if len(text) <= MAX_CHARS:
            result = scan_text(text, pack=args.rules, include_quoted=args.include_quotes, max_hits=args.max_hits)
        # A long manuscript, or a scan that reached the cap without the reader
        # asking for one, is scanned in chunks rather than cut off.
        if result is None or (result['truncated'] and args.max_hits == MAX_HITS):
            result = scan_document(text, pack=args.rules, include_quoted=args.include_quotes)
    except (OSError, ValueError, UnicodeError, TypeError) as exc:
        print(json.dumps({'status':'HOLD','error':str(exc),'release_authorized':False}))
        return 3
    if args.format == 'text':
        print('%d rules | %d findings | %.2f / 1000 words (editorial only)%s' % (
            result['rule_count'], result['finding_count'], result['density_per_1000_words'],
            ' | %d chunks' % len(result['chunks']) if 'chunks' in result else ''))
        if result.get('truncated'):
            print('INCOMPLETE: the scan reached its cap; findings after the cap were not listed')
        for f in result['findings']:
            print('%d:%d %s %s [%s]' % (f['line'], f['column'], f['severity'], f['excerpt'], f['id']))
            print('  %s' % f['question'])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
