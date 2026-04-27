#!/usr/bin/env python3
"""
Convert wf*.tmpl and wordfind*.tmpl files in wtv/wordfind/ to .html files
in wtv/wordfindpub/general/, matching the structure of 19970922planets.html.

Rules:
- Add a proper <head> block (stylesheet at ../../wtvstyles.css, scaler.js, meta author)
- Replace {{ with { in JS functions — but NOT inside the protected region:
    from '//  ************** Changable settings from HERE'
    down to 'LoadImages();'
- Replace bare <INSERT AD ...> tags with a commented-out version + spacer img
- Rewrite 'images/' references to '../../wordfind/images/'
- Leave the original .tmpl files untouched
"""

import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR    = SCRIPT_DIR
OUT_DIR    = os.path.join(SCRIPT_DIR, '..', 'wordfindpub', 'general')

HEAD_BLOCK = """\
  <head>
    <link rel="stylesheet" href="../../wtvstyles.css">
    <script src="../../scaler.js"></script>
    <META NAME="Author" CONTENT="(C) 1997 Louis F. Roehrs">
  </head>
"""

# Markers for the protected region (content kept byte-for-byte)
PROTECT_START = '//  ************** Changable settings from HERE'
PROTECT_END   = 'LoadImages();'


def insert_head_block(content):
    """Insert <head>...</head> immediately after the opening <html> tag."""
    # Match <html> with optional attributes, case-insensitive
    match = re.search(r'(<html[^>]*>)', content, re.IGNORECASE)
    if not match:
        return content
    pos = match.end()
    return content[:pos] + '\n' + HEAD_BLOCK + content[pos:]


def fix_double_braces_outside_protected(content):
    """
    Replace {{ with { throughout the file, except inside the protected region.
    The protected region runs from PROTECT_START through the first occurrence
    of PROTECT_END after it.
    """
    start_idx = content.find(PROTECT_START)
    if start_idx == -1:
        # No protected region found — safe to replace everywhere
        return content.replace('{{', '{')

    # Find PROTECT_END starting from PROTECT_START
    end_search_start = start_idx + len(PROTECT_START)
    end_idx = content.find(PROTECT_END, end_search_start)
    if end_idx == -1:
        # No end marker — protect everything from start to end of file
        before = content[:start_idx].replace('{{', '{')
        return before + content[start_idx:]

    # end_idx points to the start of PROTECT_END string; include it fully
    protect_end_pos = end_idx + len(PROTECT_END)

    before    = content[:start_idx].replace('{{', '{')
    protected = content[start_idx:protect_end_pos]          # untouched
    after     = content[protect_end_pos:].replace('{{', '{')

    return before + protected + after


def replace_insert_ad(content):
    """
    Replace bare <INSERT AD width=W height=H> tags with:
        <!-- <INSERT AD width=W height=H> -->
        <center>
          <img src="/ROMCache/spacer.gif" border=1 width=W height=H>
        </center>

    Already-commented-out <INSERT AD> tags are left alone.
    """
    def replacer(m):
        full_tag = m.group(0)
        width  = m.group(1)
        height = m.group(2)
        return (
            f'<!-- {full_tag} -->\n'
            f'             <center>\n'
            f'               <img src="/ROMCache/spacer.gif" border=1'
            f' width={width} height={height}>\n'
            f'             </center>'
        )

    # Only replace if NOT already inside an HTML comment
    # Strategy: split on comment blocks, replace only outside them
    parts = re.split(r'(<!--.*?-->)', content, flags=re.DOTALL)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            # Inside an existing comment — leave unchanged
            result.append(part)
        else:
            # Outside comments — safe to replace
            replaced = re.sub(
                r'<INSERT\s+AD\s+width=(\d+)\s+height=(\d+)>',
                replacer,
                part,
                flags=re.IGNORECASE
            )
            result.append(replaced)
    return ''.join(result)


def fix_image_paths(content):
    """
    Rewrite bare 'images/' references to '../../wordfind/images/' so that
    output files in wtv/wordfindpub/general/ resolve assets correctly.
    Skips occurrences that are already prefixed (idempotent).
    The <body background> attribute is handled separately by fix_background().
    """
    # Temporarily mask the body background attribute so it isn't rewritten here
    body_match = re.search(r'(<body\b[^>]*>)', content, re.IGNORECASE | re.DOTALL)
    if body_match:
        body_tag = body_match.group(1)
        placeholder = '\x00BODYTAG\x00'
        content = content[:body_match.start()] + placeholder + content[body_match.end():]
        content = re.sub(r'(?<!\.\./wordfind/)(?<!\.\.)images/', '../../wordfind/images/', content)
        content = content.replace(placeholder, body_tag)
    else:
        content = re.sub(r'(?<!\.\./wordfind/)(?<!\.\.)images/', '../../wordfind/images/', content)
    return content


def fix_background(content):
    """
    Set the <body background=...> attribute to 'images/BACK.JPG', matching
    19970922planets.html which lives in the same output directory.
    Also adds style="background-repeat: repeat;" to the body tag.
    """
    def replacer(m):
        tag = re.sub(
            r'background=["\']?[^\s"\'>]+["\']?',
            'background="../../wordfind/images/BACK.JPG"',
            m.group(0),
            flags=re.IGNORECASE
        )
        # Add or update style attribute with background-repeat
        if re.search(r'\bstyle\s*=', tag, re.IGNORECASE):
            tag = re.sub(
                r'(style\s*=\s*["\'])(["\'])',
                r'\1background-repeat: repeat;\2',
                tag,
                flags=re.IGNORECASE
            )
        else:
            tag = re.sub(r'(<body\b)', r'\1 style="background-repeat: repeat;"', tag, flags=re.IGNORECASE)
        return tag

    return re.sub(r'<body\b[^>]*>', replacer, content, flags=re.IGNORECASE | re.DOTALL)


def convert(src_path, dst_path):
    with open(src_path, 'r', encoding='latin-1') as f:
        content = f.read()

    content = insert_head_block(content)
    content = fix_double_braces_outside_protected(content)
    content = replace_insert_ad(content)
    content = fix_image_paths(content)
    content = fix_background(content)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='latin-1') as f:
        f.write(content)

    print(f'  OK  {os.path.basename(src_path):25s} -> {os.path.basename(dst_path)}')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    pattern = re.compile(r'^(wf|wordfind)[^/]*\.tmpl$', re.IGNORECASE)
    candidates = sorted(f for f in os.listdir(SRC_DIR) if pattern.match(f))

    if not candidates:
        print('No matching .tmpl files found.')
        sys.exit(1)

    print(f'Converting {len(candidates)} file(s) to {os.path.realpath(OUT_DIR)}\n')
    for fname in candidates:
        src = os.path.join(SRC_DIR, fname)
        dst = os.path.join(OUT_DIR, os.path.splitext(fname)[0] + '.html')
        convert(src, dst)

    print(f'\nDone. {len(candidates)} file(s) written.')


if __name__ == '__main__':
    main()
