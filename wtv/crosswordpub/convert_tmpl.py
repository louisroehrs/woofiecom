#!/usr/bin/env python3
"""
Convert wf*.tmpl and wordfind*.tmpl files in wtv/wordfind/ to .html files
in wtv/wordfindpub/general/, matching the structure of 19970922planets.html.

Rules:
- Leave the original .html files untouched
"""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR    = SCRIPT_DIR
OUT_DIR    = os.path.join(SCRIPT_DIR, '..', 'new',)


def remove_bgsound(content):
    return content.replace('<bgsound src="../sounds/jollygooba1.mid" LOOP=TRUE>','');

def add_audio(content):
    return content.replace('</footer>','</footer>\n<audio id="applause.mp2"><source src="../../audio/applause.mp2" type="audio/mpeg"  /></audio>\n<audio id="jollygooba1.mp3"><source src="../../audio/jollygooba1.mp3" type="audio/mpeg"  /></audio>');


def convert(src_path, dst_path):
    with open(src_path, 'r', encoding='latin-1') as f:
        content = f.read()


    content= remove_bgsound(content)
    content= add_audio(content):

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='latin-1') as f:
        f.write(content)

    print(f'  OK  {os.path.basename(src_path):25s} -> {os.path.basename(dst_path)}')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    pattern = re.compile(r'^[^/]*\.html$', re.IGNORECASE)
    candidates = sorted(f for f in os.listdir(SRC_DIR) if pattern.match(f))

    if not candidates:
        print('No matching .html files found.')
        sys.exit(1)

    print(f'Converting {len(candidates)} file(s) to {os.path.realpath(OUT_DIR)}\n')
    for fname in candidates:
        src = os.path.join(SRC_DIR, fname)
        dst = os.path.join(OUT_DIR, os.path.splitext(fname)[0] + '.html')
        convert(src, dst)

    print(f'\nDone. {len(candidates)} file(s) written.')


if __name__ == '__main__':
    main()
