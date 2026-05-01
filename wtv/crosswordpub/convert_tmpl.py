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
SRC_DIR    = os.path.join(SCRIPT_DIR, 'general')
OUT_DIR    = os.path.join(SCRIPT_DIR, 'new')


def remove_bgsound(content):
    return re.sub(r'[ \t]*<bgsound[^>]*>\n?', '', content, flags=re.IGNORECASE)

def add_audio(content):
    audio_tags = (
        '  <audio id="applause.mp2"><source src="../../audio/applause.mp2" type="audio/mpeg"  /></audio>\n'
        '  <audio id="jollygooba1.mp3"><source src="../../audio/jollygooba1.mp3" type="audio/mpeg"  /></audio>\n'
    )
    return re.sub(r'(</body>)', audio_tags + r'\1', content, count=1, flags=re.IGNORECASE)


def fix_body_style(content):
    """Add height/width to the body style attribute, creating it if absent."""
    def replacer(m):
        tag = m.group(0)
        extra = 'height: 420px; width: 560px; '
        if re.search(r'\bstyle\s*=', tag, re.IGNORECASE):
            tag = re.sub(
                r'(style\s*=\s*["\'])',
                r'\g<1>' + extra,
                tag,
                flags=re.IGNORECASE
            )
        else:
            tag = re.sub(r'(<body\b)', r'\1 style="' + extra + '"', tag, flags=re.IGNORECASE)
        return tag
    return re.sub(r'<body\b[^>]*>', replacer, content, flags=re.IGNORECASE | re.DOTALL)


def insert_script_ref(content):
    return content.replace(
        '<script src="../../scaler.js"></script>',
        '<script src="../../scaler.js"></script>\n    <script src="../../crossword/script/crossword.js"></script>'
    )


def remove_first_td_width(content):
    """Remove the width attribute from the first <td> in the first non-JS table."""
    # Find the first non-JS table
    table_match = re.search(r'(?<!write\(")(<table\b[^>]*>)', content, re.IGNORECASE)
    if not table_match:
        return content
    table_pos = table_match.end()
    # Find the first <td> after that
    td_match = re.search(r'<td\b[^>]*>', content[table_pos:], re.IGNORECASE)
    if not td_match:
        return content
    td_start = table_pos + td_match.start()
    td_end   = table_pos + td_match.end()
    new_td = re.sub(r'\s*\bwidth=["\']?[^"\'>\s]+["\']?', '', content[td_start:td_end], count=1, flags=re.IGNORECASE)
    return content[:td_start] + new_td + content[td_end:]


def fix_first_table_width(content):
    """Change width on the first non-JS <table> tag to 560."""
    def replacer(m):
        tag = re.sub(r'\bwidth=["\']?[^"\'>\s]+["\']?', 'width=560', m.group(0), count=1, flags=re.IGNORECASE)
        return tag
    # Match the first <table ...> that isn't inside a document.write()
    return re.sub(r'(?<!write\(")(<table\b[^>]*>)', replacer, content, count=1, flags=re.IGNORECASE)


def fix_script_language_typo(content):
    """Fix the misspelling 'langauge' -> 'language' in script tags."""
    return re.sub(r'\blangauge\b', 'language', content, flags=re.IGNORECASE)


def fix_control_buttons_table_width(content):
    """Change width=100 to width=100% on the control buttons table."""
    return re.sub(
        r'(<!--\s*Control Buttons\s*-->.*?<table\b[^>]*)\bwidth=100\b',
        r'\g<1>width=100%',
        content,
        count=1,
        flags=re.IGNORECASE | re.DOTALL
    )


def remove_nbsp_before_correct(content):
    return re.sub(r'&nbsp;(\s*<A\b[^>]*CorrectPuzzle)', r'\1', content, flags=re.IGNORECASE)


def strip_common_javascript(content):
    """
    Remove the common JS engine code that follows 'kOtherFormElements = 0;'
    up to (but not including) the closing </script> tag.
    """
    CUT_AFTER  = 'kOtherFormElements = 0;'
    SCRIPT_CLOSE = '</script>'

    cut_pos = content.find(CUT_AFTER)
    if cut_pos == -1:
        return content

    # Start cutting from the end of the marker line
    cut_start = cut_pos + len(CUT_AFTER)

    # Find the next </script> after the cut point
    close_pos = content.lower().find(SCRIPT_CLOSE.lower(), cut_start)
    if close_pos == -1:
        return content

    # Replace everything between the marker and </script> with a single newline
    return content[:cut_start] + '\n\n    ' + content[close_pos:]


def convert(src_path, dst_path):
    with open(src_path, 'r', encoding='latin-1') as f:
        content = f.read()


    content= remove_bgsound(content)
    content= fix_first_table_width(content)
    content= remove_first_td_width(content)
    content= fix_body_style(content)
    content= insert_script_ref(content)
    content= fix_script_language_typo(content)
    content= fix_control_buttons_table_width(content)
    content= remove_nbsp_before_correct(content)
    content= strip_common_javascript(content)
    content= add_audio(content)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='latin-1') as f:
        f.write(content)

    print(f'  OK  {os.path.basename(src_path):25s} -> {os.path.basename(dst_path)}')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    pattern = re.compile(r'^.+\.html$', re.IGNORECASE)
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
