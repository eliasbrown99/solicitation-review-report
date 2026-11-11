"""Inspect saved historical outputs without importing the app or invoking a model.

Requires a local Capstone clone with the specified Git object. Exports aggregates
only: no filenames, source text, headings, summaries, or document identifiers.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import tempfile

SNAPSHOT = 'aa91149b093b438564d85b017198a2a2686ad2fe'
BULLET = re.compile(r'^(\s*)(?:[-*•]|\d+[.)])\s+')

def bullet_counts(text):
    matches = [BULLET.match(line) for line in text.splitlines()]
    matches = [m for m in matches if m]
    if not matches:
        return 0, 0
    indents = [len(m.group(1).expandtabs(4)) for m in matches]
    return sum(i == min(indents) for i in indents), len(indents)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-repo', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    # Independent checks distinguish nested details from top-level bullets.
    assert bullet_counts('- first\n- second\n  - detail') == (2, 3)
    assert bullet_counts('• one\n• two\n• three\n• four\n• five\n• six') == (6, 6)
    payload = subprocess.check_output(['git', '-C', str(args.source_repo), 'show', f'{SNAPSHOT}:summaries.db'])
    with tempfile.TemporaryDirectory(prefix='capstone-snapshot-') as tmp:
        snapshot = Path(tmp) / 'summaries.db'
        snapshot.write_bytes(payload)
        db = sqlite3.connect(f'file:{snapshot}?mode=ro', uri=True)
        rows = db.execute('SELECT filename, upload_time, summary FROM summaries').fetchall()
        db.close()
    top_counts = collections.Counter()
    all_counts = collections.Counter()
    section_counts = []
    nested, empty = 0, 0
    for filename, uploaded, summary in rows:
        sections = json.loads(summary)
        section_counts.append(len(sections))
        for section in sections:
            text = section['summary']
            top, all_items = bullet_counts(text)
            top_counts[top] += 1
            all_counts[all_items] += 1
            nested += top != all_items
            empty += not text.strip()
    assert sum(top_counts.values()) == sum(section_counts)
    assert sum(all_counts.values()) == sum(section_counts)
    result = {
        'source_commit': SNAPSHOT,
        'snapshot_sha256': hashlib.sha256(payload).hexdigest(),
        'scope': 'Historical saved-output snapshot; not a labeled evaluation set or complete project corpus.',
        'document_rows': len(rows),
        'distinct_filenames': len({r[0] for r in rows}),
        'section_summaries': sum(section_counts),
        'upload_date_range': [min(r[1] for r in rows)[:10], max(r[1] for r in rows)[:10]],
        'top_level_bullets': dict(sorted(top_counts.items())),
        'all_bullet_lines': dict(sorted(all_counts.items())),
        'summaries_with_nested_bullets': nested,
        'empty_summaries': empty,
        'definition': 'A bullet line starts with -, *, •, or a number plus . or ). Top-level lines have the smallest indentation within that summary. One observation is one stored section summary; output length is not accuracy.',
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'saved-output-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
