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
OUT_DIR    = os.path.join(SCRIPT_DIR, '..', '..', 'wordfindpub', 'general')

HEAD_BLOCK = """\
    <link rel="stylesheet" href="../../wtvstyles.css">
    <script src="../../scaler.js"></script>
    <META NAME="Author" CONTENT="(C) 1997 Louis F. Roehrs">
"""

FOOTER_BLOCK = (
    '      <footerborder></footerborder>\n'
    '      <footer>\n'
    '        <div class=footerstatus>WebTV Wordfinder</div>'
    '<div class=audiostatus><div class="audiogreen"></div>\n'
    '        </div>\n'
    '      </footer>'
)

# Markers for the protected region (content kept byte-for-byte)
PROTECT_START = '//  ************** Changable settings from HERE'
PROTECT_END   = '//  ************** Changable settings to HERE'


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


def insert_script_ref(content):
    """Insert <script src="../../wordfind/script/wordfind.js"></script>
    immediately before the closing </head> tag."""
    tag = '<script src="../../wordfind/script/wordfind.js"></script>\n'
    return re.sub(r'(</head>)', tag + r'\1', content, count=1, flags=re.IGNORECASE)


def strip_common_javascript(content):
    """
    Within the <script> block that follows <title>Loading Game...</title>,
    remove all JS outside the protected settings region:
      - Remove everything between <script language="JavaScript"> and
        '//  ************** Changable settings from HERE'
      - Keep everything from PROTECT_START through PROTECT_END (inclusive)
      - Remove everything from after PROTECT_END through the closing </script>
    The </script> and </head> tags themselves are preserved.
    """
    SCRIPT_OPEN  = '<script language="JavaScript">'
    SCRIPT_CLOSE = '</script>'
    TITLE_MARKER = '<title>Loading Game...</title>'

    title_pos = content.lower().find(TITLE_MARKER.lower())
    if title_pos == -1:
        return content

    script_open_pos = content.lower().find(SCRIPT_OPEN.lower(), title_pos)
    if script_open_pos == -1:
        return content

    script_content_start = script_open_pos + len(SCRIPT_OPEN)

    # Find </head> to bound our search for the closing </script>
    head_close_pos = content.lower().find('</head>', script_content_start)
    if head_close_pos == -1:
        return content

    # The closing </script> is the last one before </head>
    script_close_pos = content.lower().rfind(SCRIPT_CLOSE.lower(), script_content_start, head_close_pos)
    if script_close_pos == -1:
        return content

    script_body = content[script_content_start:script_close_pos]

    protect_start_idx = script_body.find(PROTECT_START)
    protect_end_idx   = script_body.find(PROTECT_END)
    if protect_start_idx == -1 or protect_end_idx == -1:
        return content

    protect_end_pos = protect_end_idx + len(PROTECT_END)
    protected = script_body[protect_start_idx:protect_end_pos]

    closing_tag = content[script_close_pos:script_close_pos + len(SCRIPT_CLOSE)]
    new_script = SCRIPT_OPEN + '\n\n' + protected + '\n\n' + closing_tag

    return content[:script_open_pos] + new_script + content[script_close_pos + len(SCRIPT_CLOSE):]

def insert_footer(content):
    if re.search(r'<footer>', content, re.IGNORECASE):
        return content
    return re.sub(
        r'(\s*</body>)',
        '\n' + FOOTER_BLOCK + r'\n\n  \1',
        content,
        flags=re.IGNORECASE,
    )

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
            f'               <img src="/wtv/ROMCache/spacer.gif" border=1'
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
        content = re.sub(r'(?<!\.\./wordfind/)(?<!\.\.)images/', '../wordfind/images/', content)
        content = content.replace(placeholder, body_tag)
    else:
        content = re.sub(r'(?<!\.\./wordfind/)(?<!\.\.)images/', '../wordfind/images/', content)
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
            'background="../../wordfind/images/back200.jpg"',
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


def fix_abs_dimensions(content):
    """Replace WebTV-specific abswidth/absheight attributes with standard width/height."""
    content = re.sub(r'\babswidth\b', 'width', content, flags=re.IGNORECASE)
    content = re.sub(r'\babsheight\b', 'height', content, flags=re.IGNORECASE)
    return content


def remove_bgcolor_53001b(content):
    """Remove all occurrences of bgcolor=53001b (any case, with or without quotes)."""
    return re.sub(r'\s*bgcolor=["\']?53001b["\']?', '', content, flags=re.IGNORECASE)

def remove_bgcolor_464664(content):
    """Remove all occurrences of bgcolor=464664 (any case, with or without quotes)."""
    return re.sub(r'\s*bgcolor=["\']?464664["\']?', '', content, flags=re.IGNORECASE)

def change_table_widths(content):
    """Change table width from 166 to 220"""
    return re.sub(r'\<td width=166','<td width=220', content, flags=re.IGNORECASE)

def remove_spacer(content):
    return content.replace('<IMG width=8 height=7 src=/ROMCache/Spacer.gif><BR>','')

def fix_romcache_paths(content):
    """Replace /ROMCache/Spacer.gif (any case) with /wtv/ROMCache/spacer.gif."""
    return re.sub(
        r'/ROMCache/Spacer\.gif',
        '/wtv/ROMCache/spacer.gif',
        content,
        flags=re.IGNORECASE
    )


def comment_out_embeds(content):
    """Wrap all <EMBED ...> tags in HTML comments."""
    return re.sub(
        r'(<EMBED\b[^>]*>)',
        r'<!-- \1 -->',
        content,
        flags=re.IGNORECASE | re.DOTALL
    )

def add_ad(content):

    return content.replace('<INSERT AD sponsor=GAMES width=394 height=71 template=insetad.tmpl>','<a href="credits.html"><IMG SRC="http://www.woofie.com/images/bws.gif" WIDTH=394 HEIGHT=71 BORDER=0 usemap=woofie></a>')


def replace_home_link(content):
    return content.replace('href="wtv-home:/home"','href="../arcade/arcade.html?wtv-home:/home"')

def convert(src_path, dst_path):
    with open(src_path, 'r', encoding='latin-1') as f:
        content = f.read()

    content = strip_common_javascript(content)
    content = insert_head_block(content)
    content = insert_script_ref(content)
    content = fix_double_braces_outside_protected(content)
    content = replace_insert_ad(content)
    content = fix_image_paths(content)
    content = fix_background(content)
    content = fix_abs_dimensions(content)
#    content = remove_bgcolor_53001b(content)
#    content = remove_bgcolor_464664(content)
#    content = remove_spacer(content)
 #   content = change_table_widths(content)
    content = fix_romcache_paths(content)
    content = comment_out_embeds(content)
    content = insert_footer(content)
    content = replace_home_link(content)
    content = add_ad(content)
    
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'w', encoding='latin-1') as f:
        f.write(content)

    print(f'  OK  {os.path.basename(src_path):25s} -> {os.path.basename(dst_path)}')


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

#    pattern = re.compile(r'^(wf|wordfind)[^/]*\.tmpl$', re.IGNORECASE)
    pattern = re.compile(r'^[^/]*\.tmpl$', re.IGNORECASE)
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
