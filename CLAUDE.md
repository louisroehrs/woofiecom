# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A static HTML website — Big Woofie Studios / woofie.com — built by Louis Roehrs. No build system, no package manager, no test suite. Files are served directly as-is. Open any `.html` file in a browser to test it.

## Architecture

### Design System (`woofie.css`, `ttx.css`)

Two swappable CSS themes controlled by `theme.js` via `setTheme("woofie")` / `setTheme("ttx")`. The active theme is stored in a cookie and applied by swapping `document.styleSheets[0].href`. The shared design language:

- **Title bar**: `#000066` navy background, `#ff0000` red text, Courier New bold 28px
- **Panel headers** (`.panelheader`): `#ddddff` lavender background, Arial bold
- **Panel data** (`.paneldata`): white background, `#0000ff` blue text, Verdana 12px
- **Column dividers** (`.column`): `#000066` navy, 7px height
- **Page background**: `#808080` gray
- `ttx.css` variant uses `#666666` gray for `.column` instead of navy

### Flash Polyfill (`ruffle/`)

All `.swf` files in `flash/` are polyfilled by Ruffle. Pages that embed Flash include `<script src="ruffle/ruffle.js">` in the `<head>` and wrap `<EMBED>` tags in `<div class="ruffle-player">`. The `.wasm` file in `ruffle/` must be served with `application/wasm` MIME type.

### index.html

The main page. Notable features:
- Two-column table layout: left column (content/links) + right column (Flash player, Amazon search widget)
- **Weird Al modal**: A hidden button (`#weirdalBtnWrap`) that fades in after 5 seconds via `setTimeout` adding class `revealed`. Opens a modal overlay (`#weirdalOverlay`) telling the woofie.com / "White & Nerdy" origin story with embedded YouTube player.

### Key Subdirectories

- **`ui/graphing/`** — JavaScript charting demos. `piechart.html` uses IE-only VML; `piechartsvg.html` is the modern SVG replacement with the same four-input interface.
- **`dhtml/dialog/`** — Reusable popup/dialog HTML components
- **`wtv/kar/`** — KaraokeTV player: retro TV UI rendering `.kar`/`.emk` MIDI files with lyrics via SpessaSynth. Self-contained; open `index.html` directly.
- **`dt/DemandTec/`** — Enterprise UI prototypes with their own `DemandTec.css`
- **`music/`** — Celtic music artist pages (Loreena McKennitt, Altan, etc.) with Amazon affiliate links
- **`portfolio/`** — WebTV games portfolio
- **`velocity3studios/`** — 3D animation showcase
- **`mac/`** — iWeb-exported photo galleries
- **`ERPD/`** — ExtJS-based enterprise resource planning demo

### Theme Switching

`theme.js` exposes `setTheme(name)` which sets a cookie and swaps the first stylesheet href. The index page footer has links: `setTheme("ttx")` and `setTheme("woofie")`. The URL prefix in `theme.js` is hardcoded to `http://www.woofie.com/` — when editing locally, this will fail; the stylesheet swap won't work unless the URL is updated or the files are served from that domain.

### Amazon Affiliate Links

Affiliate tag `bigwoofieenterta` is used throughout. Old Amazon cover image URL pattern (`amazon.com/covers/...`) is dead — modern images use `m.media-amazon.com/images/I/{hash}` which requires looking up per-product.
