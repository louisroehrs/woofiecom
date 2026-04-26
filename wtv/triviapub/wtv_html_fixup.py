#!/usr/bin/env python3
"""
Apply wtv-html-fixup transformations to all .html files in the current directory.

Usage:
    cd path/to/game-directory
    python /path/to/wtv_html_fixup.py

Steps applied:
  1. Add stylesheet link (if missing)
  2. Add footer block (if missing)
  3. Replace absheight -> height
  4. Replace abswidth -> width
  5. Comment out EMBED sound tags
  6. Add align=center valign=top to the WebTV jewel cell td
  7. Replace file:// with /
  8. Restructure SCORE&NEXT ROW into nested table
  9. Re-indent with 2-space indentation
"""

import glob
import os
import re

STYLESHEET_LINK = '<link rel="stylesheet" href="../../wtvstyles.css">'

FOOTER_BLOCK = (
    '      <footerborder></footerborder>\n'
    '      <footer>\n'
    '        <div class=footerstatus>WebTV Crossword</div>'
    '<div class=audiostatus><div class="audiogreen"></div>\n'
    '        </div>\n'
    '      </footer>'
)


# ---------------------------------------------------------------------------
# Step functions
# ---------------------------------------------------------------------------

def step_stylesheet(content):
    if "../../wtvstyles.css" in content:
        return content
    if STYLESHEET_LINK in content:
        return content
    return re.sub(r'(<html>)', r'\1\n<head>    ' + STYLESHEET_LINK + r'\n</head>', content, flags=re.IGNORECASE)

def step_scaler(content):
    if "scaler.js" in content:
        return content
    return re.sub(r'<link rel="stylesheet" href="../../../wtvstyles.css">',r'    <link rel="stylesheet" href="../../../wtvstyles.css">\n    <script src="../../../scaler.js"></script>\n    <META NAME="Author" CONTENT="(C) 1997 Louis F. Roehrs">',content, flags=re.IGNORECASE)

def step_isolate_check_question(content):
    if "CheckOnRightQuestion" in content:
        return content
    return re.sub(r'CheckQuestionOn', '</script>\nCheckOnRightQuestion',content)

def step_trivia_js(content):
    if "trivia.js" in content:
        return content
    return re.sub(r'<script language="JavaScript">[\s\S]*?(<\/SCRIPT>)','<script src="../../script/trivia.js"></script>',content)


def step_sound_files(content) :
    if "<audio" in content:
        return content
    return re.sub(r'</footer>',r'</footer>\n<audio id="newbell3.mid"><source src="../../../audio/newbell3.mp3" type="audio/mpeg"/></audio>\n<audio id="buzz.mid"><source src="../../../audio/buzz.mp3" type="audio/mpeg"  /></audio>\n<audio id="applause.mp2"><source src="../../../audio/applause.mp2" type="audio/mpeg"  /></audio>',content,flags=re.IGNORECASE)

    
def step_footer(content):
    if re.search(r'<footer>', content, re.IGNORECASE):
        return content
    return re.sub(
        r'(\s*</body>)',
        '\n' + FOOTER_BLOCK + r'\n\n  \1',
        content,
        flags=re.IGNORECASE,
    )

def step_dumb_quotes(content):
    return content.replace('�',"'")

def step_absheight(content):
    return re.sub(r'absheight', 'height', content, flags=re.IGNORECASE)

def step_home_logo_link(content):
    if "arcade/aracade.html" in content:
        return content
    return content.replace('<IMG width=104 height=87 src=/ROMCache/WebTVLogoJewel.gif>','<a href="../../../arcade/arcade.html"><IMG width=104 height=87 src=/ROMCache/WebTVLogoJewel.gif></a>')

def step_abswidth(content):
    return re.sub(r'abswidth', 'width', content, flags=re.IGNORECASE)


def step_comment_embeds(content):
    """Wrap consecutive EMBED sound tags in an HTML comment."""
    # Already commented if <!-- immediately precedes an EMBED
    if re.search(r'<!--\s*\n\s*<EMBED', content, re.IGNORECASE):
        return content

    # Match two consecutive multiline EMBED tags (separated by optional whitespace)
    pattern = re.compile(
        r'(\s+<EMBED\b[^>]*>\s+<EMBED\b[^>]*>)',
        re.DOTALL | re.IGNORECASE,
    )

    def wrap_comment(m):
        inner = m.group(1).strip()
        return '\n<!--\n    ' + re.sub(r'\n\s*', '\n    ', inner) + '\n-->'

    return pattern.sub(wrap_comment, content)


def step_logo_cell(content):
    """Add align=center valign=top to the td containing WebTVLogoJewel.gif."""
    pattern = re.compile(
        r'(<td\b[^>]*>)(\s*<IMG[^>]*WebTVLogoJewel\.gif[^>]*>)',
        re.IGNORECASE | re.DOTALL,
    )

    def fix_td(m):
        td, img = m.group(1), m.group(2)
        if not re.search(r'\balign=center\b', td, re.IGNORECASE):
            td = td[:-1] + ' align=center>'
        if not re.search(r'\bvalign=top\b', td, re.IGNORECASE):
            td = td[:-1] + ' valign=top>'
        return td + img

    return pattern.sub(fix_td, content)


def step_file_protocol(content):
    return content.replace('file://', '/')


def step_spacerace_trivial_task(content):
    return content.replace("WebTV SpaceRace","WebTV Trivial Task")

def step_button_click(content):
    return content.replace('href="javascript:CheckAndRedirect(','onclick="CheckAndRedirect(')

def step_rom_cache(content):
    return content.replace('src=/ROMCache/Spacer.gif','src=/wtv/ROMCache/spacer.gif')

def step_main_table_measurements(content):
    content = re.sub(r'<table cellpadding=0 cellspacing=0>[^<]*<tr height=200>','<table cellpadding=0 cellspacing=0 width=100%>\n<tr height=90>',content)
    content = content.replace('<td colspan=2 width=195 height=120>','<td colspan=3 width=195 height=90>')
    content = content.replace('<!-- Question -->','<td rowspan=3 width=10 align=left>\n<IMG src=/ROMCache/Spacer.gif name=message width=10 height=108>\n</td>\n<!-- Question Text -->')
    return content

def step_textarea_disable(content):
    return re.sub(r'<textarea noselect','<textarea disabled noselect',content, re.IGNORECASE);

def step_score_row(content):
    """Replace the three-cell score/next row with a nested-table version."""
    # Already restructured: new format has <!-- //SCORE CELL --> followed by <table
    if re.search(r'<!-- //SCORE CELL -->\s*\n\s*<table', content, re.IGNORECASE | re.DOTALL):
        return content

    # Extract question number from the next-arrow href (may be split across lines)
    q_match = re.search(
        r"RedirectToNextQuestion\('general',\s*\n?\s*(\d+)\)",
        content,
    )
    if not q_match:
        return content
    q_num = q_match.group(1)

    new_row = f"""\
        <!-- //SCORE&NEXT ROW -->

        <tr>
          <td colspan=3>
            <!-- //SCORE CELL -->
            <table width=100%>
              <tr>
                <td valign=absmiddle align=center><font size=+2>Score:</font></td>

                <td valign=absmiddle>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=scorem>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score0>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score1>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score2>
                  <img width=33 height=53 src=/ROMCache/spacer.gif name=score3>
                </td>

                <!-- // NEXT ARROW -->

                <td valign=absmiddle align=center>
                  <a href="javascript:RedirectToNextQuestion('general', {q_num})">
                    <img width=84 height=51 src="../../images/arrow.gif">
                  </a>
                </td>
              </tr>
            </table>
          </td>
          <!-- // SCORE&NEXT -->
        </tr>"""

    old_pattern = re.compile(
        r'[ \t]*<!-- //SCORE&NEXT ROW -->.*?<!-- // SCORE&NEXT -->\s*\n\s*</tr>',
        re.DOTALL | re.IGNORECASE,
    )
    return old_pattern.sub(new_row, content)


# ---------------------------------------------------------------------------
# Re-indentation
# ---------------------------------------------------------------------------

BLOCK_TAGS = {
    'html', 'head', 'body', 'table', 'tr', 'td', 'th', 'thead', 'tbody',
    'tfoot', 'form', 'div', 'footer', 'center', 'script',
}


def reindent(content):
    """Re-indent HTML with 2-space indentation."""
    lines = content.split('\n')
    result = []
    depth = 0
    in_script = False
    script_depth = 0
    in_comment = False

    for raw in lines:
        s = raw.strip()

        if not s:
            result.append('')
            continue

        # Multi-line HTML comment passthrough
        if in_comment:
            result.append('  ' * depth + s)
            if '-->' in s:
                in_comment = False
            continue

        if s.startswith('<!--') and '-->' not in s:
            in_comment = True
            result.append('  ' * depth + s)
            continue

        # Inside <script> block: preserve relative structure
        if in_script:
            if re.match(r'</script\s*>', s, re.IGNORECASE):
                in_script = False
                depth = script_depth
                result.append('  ' * depth + s)
            else:
                result.append('  ' * (script_depth + 1) + s)
            continue

        # Closing block tag: reduce depth before printing
        close = re.match(r'</([\w]+)', s, re.IGNORECASE)
        if close and close.group(1).lower() in BLOCK_TAGS:
            depth = max(0, depth - 1)

        result.append('  ' * depth + s)

        # Opening block tag: increase depth after printing
        open_tag = re.match(r'<([\w]+)', s, re.IGNORECASE)
        if open_tag:
            tag = open_tag.group(1).lower()
            if tag == 'script':
                script_depth = depth
                in_script = True
                depth += 1
            elif tag in BLOCK_TAGS:
                # Don't increase if the closing tag is also on this line
                if not re.search(r'</' + tag + r'\s*>', s, re.IGNORECASE):
                    depth += 1

    return '\n'.join(result)


# ---------------------------------------------------------------------------
# Process a single file
# ---------------------------------------------------------------------------

TRANSFORMSALL = [
    ('stylesheet',    step_stylesheet),
    ('footer',        step_footer),
    ('absheight',     step_absheight),
    ('abswidth',      step_abswidth),
    ('comment EMBED', step_comment_embeds),
    ('logo cell',     step_logo_cell),
    ('file://',       step_file_protocol),
    ('score row',     step_score_row),
    ('main_table_measurements', step_main_table_measurements),
    ('spacerace_trivial_task',step_spacerace_trivial_task),
    ('button_click',step_button_click),
    ('rom_cache',step_rom_cache),
    ('textarea_disable',step_textarea_disable),
    ('sound_files', step_sound_files),
    ('scaler',step_scaler),
    ('isolate_check_question',step_isolate_check_question),
    ('trivia_js', step_trivia_js),
    ('dumb_quotes', step_dumb_quotes),
    ('home_logo_link', step_home_logo_link),
]

TRANSFORMS = [
    ('scaler',step_scaler),
]

def process_file(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        original = f.read()

    content = original
    applied = []

    for name, fn in TRANSFORMS:
        new = fn(content)
        if new != content:
            applied.append(name)
            content = new

    reindented = reindent(content)
    if reindented != content:
        applied.append('reindent')
        content = reindented

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return applied
    return []


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    html_files = sorted(glob.glob('*.html'))
    if not html_files:
        print('No .html files found in current directory.')
        return

    changed = 0
    for path in html_files:
        result = process_file(path)
        if result:
            print(f'  {path}: {", ".join(result)}')
            changed += 1
        else:
            print(f'  {path}: no changes')

    print(f'\n{changed}/{len(html_files)} files changed.')


if __name__ == '__main__':
    main()
