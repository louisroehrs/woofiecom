#!/usr/bin/env python3
"""
Scans the wtv/ directory tree for .swf, .spl, and .fla files and generates
embed_browser.html in the same directory, allowing the user to select any
found file and preview it in an <embed> tag.

Run from anywhere — paths in the HTML are always relative to wtv/.
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE   = os.path.join(SCRIPT_DIR, 'embed_browser.html')
EXTENSIONS = {'.swf', '.spl', '.fla'}


def find_files():
    """Return sorted list of (rel_path, ext) tuples relative to SCRIPT_DIR."""
    found = []
    for dirpath, _dirs, filenames in os.walk(SCRIPT_DIR):
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in EXTENSIONS:
                abs_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(abs_path, SCRIPT_DIR)
                # Normalise to forward slashes for HTML
                rel_path = rel_path.replace(os.sep, '/')
                found.append((rel_path, ext.lstrip('.')))
    return sorted(found, key=lambda x: (x[1], x[0]))


def build_options(files):
    """Build <optgroup> blocks grouped by extension."""
    groups = {}
    for rel_path, ext in files:
        groups.setdefault(ext, []).append(rel_path)

    html = []
    for ext in ('swf', 'spl', 'fla'):
        if ext not in groups:
            continue
        html.append(f'      <optgroup label=".{ext.upper()} files">')
        for rel_path in groups[ext]:
            label = rel_path
            html.append(f'        <option value="{rel_path}">{label}</option>')
        html.append('      </optgroup>')
    return '\n'.join(html)


def generate_html(files):
    options = build_options(files)
    count   = len(files)

    return f"""\
<!DOCTYPE html>
<html>
<head>
  <title>Embed Browser &mdash; wtv/</title>
  <style>
    body {{
      font-family: Arial, Helvetica, sans-serif;
      background: #1a1a2e;
      color: #e0e0e0;
      margin: 0;
      padding: 20px;
    }}
    h1 {{
      font-size: 20px;
      color: #ffcc00;
      margin-bottom: 4px;
    }}
    .subtitle {{
      font-size: 12px;
      color: #888;
      margin-bottom: 18px;
    }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }}
    select {{
      flex: 1;
      min-width: 300px;
      padding: 6px 8px;
      font-size: 13px;
      background: #0d0d1a;
      color: #e0e0e0;
      border: 1px solid #444;
      border-radius: 4px;
    }}
    button {{
      padding: 6px 16px;
      background: #ffcc00;
      color: #000;
      border: none;
      border-radius: 4px;
      font-weight: bold;
      cursor: pointer;
      font-size: 13px;
    }}
    button:hover {{ background: #ffe066; }}
    #path-display {{
      font-size: 12px;
      color: #aaa;
      font-family: monospace;
      margin-bottom: 12px;
      min-height: 16px;
    }}
    #embed-code {{
      font-family: monospace;
      font-size: 12px;
      background: #0d0d1a;
      border: 1px solid #333;
      border-radius: 4px;
      padding: 10px;
      margin-bottom: 16px;
      color: #7ec8e3;
      white-space: pre;
      overflow-x: auto;
    }}
    #preview-box {{
      background: #000;
      border: 2px solid #333;
      border-radius: 6px;
      padding: 10px;
      display: inline-block;
      min-width: 320px;
      min-height: 240px;
    }}
    #preview-label {{
      font-size: 11px;
      color: #555;
      margin-bottom: 20px;
    }}
  </style>
</head>
<body>

<h1>Embed Browser &mdash; wtv/</h1>
<div class="subtitle">{count} files found (.swf, .spl, .fla)</div>

<div class="controls">
  <select id="file-select" onchange="updatePreview()">
    <option value="">-- select a file --</option>
{options}
  </select>
  <button onclick="updatePreview()">Load</button>
</div>

<div id="path-display"></div>
<div id="embed-code"></div>

<div id="preview-label">Preview:</div>
<div id="preview-box">
  <div id="embed-container"></div>
</div>

<script>
  function updatePreview() {{
    var sel  = document.getElementById('file-select');
    var src  = sel.value;
    var pathDisplay = document.getElementById('path-display');
    var codeBox     = document.getElementById('embed-code');
    var container   = document.getElementById('embed-container');

    if (!src) {{
      pathDisplay.textContent = '';
      codeBox.textContent = '';
      container.innerHTML = '';
      return;
    }}

    pathDisplay.textContent = src;

    var embedTag = '<EMBED SRC="' + src + '" WIDTH="320" HEIGHT="240" AUTOSTART="TRUE" LOOP="FALSE">';
    codeBox.textContent = embedTag;

    container.innerHTML =
      '<embed src="' + src + '" width="320" height="240" autostart="true" loop="false">';
  }}
</script>

</body>
</html>
"""


def main():
    files = find_files()
    if not files:
        print('No .swf, .spl, or .fla files found.')
        return

    html = generate_html(files)
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'Found {len(files)} file(s).')
    print(f'Written: {OUT_FILE}')


if __name__ == '__main__':
    main()
