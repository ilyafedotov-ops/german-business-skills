---
name: German Business Kit · Beleg
description: Launch visuals where every answer prints as a receipt and ends "sent by you".
colors:
  carbon: "#252a7c"
  carbon-deep: "#191c5c"
  carbon-light: "#343a9a"
  carbon-ink: "#c9ccf5"
  ink: "#141414"
  ink-mid: "#3d3d3a"
  ink-faded: "#5f5f5a"
  rule: "#8d8d86"
  red: "#c8251a"
  paper-white: "#f6f6f1"
  paper-yellow: "#f3df7a"
  paper-blue: "#cadcef"
  paper-pink: "#f2c3d0"
  yellow-faded: "#574d17"
  blue-faded: "#3d4f66"
  pink-faded: "#6b3646"
typography:
  print:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "30px"
    fontWeight: 450
    lineHeight: 1.46
    letterSpacing: "normal"
  double-height:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "62px"
    fontWeight: 760
    lineHeight: 1.08
    letterSpacing: "-0.012em"
  double-width:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "50px"
    fontWeight: 800
    lineHeight: 1.12
    letterSpacing: "-0.01em"
  field-label:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "24px"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.05em"
  fine-print:
    fontFamily: "Martian Mono, ui-monospace, monospace"
    fontSize: "21px"
    fontWeight: 450
    lineHeight: 1.45
rounded:
  none: "0px"
  stamp: "12px"
  browser: "14px"
spacing:
  receipt-x: "54px"
  receipt-top: "56px"
  receipt-bottom: "64px"
  rule: "22px"
  rule-double: "26px"
components:
  receipt:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "56px 54px 64px"
    width: "880px"
  caption-strip:
    backgroundColor: "{colors.paper-white}"
    textColor: "{colors.ink}"
    typography: "{typography.print}"
    padding: "14px 26px"
  stamp:
    textColor: "{colors.red}"
    rounded: "{rounded.stamp}"
    padding: "8px 18px 10px"
---

# Design System: German Business Kit · Beleg

## Overview

Launch visuals for German Business Kit (LinkedIn carousels in English and German, a 4:5 LinkedIn video, a 16:9 YouTube walkthrough). The world is the Kassenbon and the duplicate receipt book: each slide is a receipt on carbon-paper blue, itemizing what an answer checked and closing with the kit's rule, SENT BY … YOU. Seed key 291c5f8f; direction contract in DIRECTION.md. Built in `build/make_receipts.py` and `build/receipt.css`.

## Colors

Strategy: committed. Carbon blue owns the ground at full bleed; paper carries the content; red is a second thermal ink, never decoration.

### Primary
- **Carbon** `#252a7c` with a soft top light `#343a9a` and a deep floor `#191c5c`. Text on carbon is white or `#c9ccf5`.

### Secondary
- **Paper**: original white `#f6f6f1`; copy tints canary `#f3df7a`, blue `#cadcef`, pink `#f2c3d0`. In the carousel, Berlin prints on white, Hamburg on blue, Munich on yellow, the close on pink.

### Tertiary
- **Red second ink** `#c8251a`: limits, deadlines, unreachable sources, and every YOU / SIE.

### Neutral
- Thermal ink `#141414` for decisive lines, `#3d3d3a` for running text, `#5f5f5a` for faded lines on white.

### Named Rules
- **Tinted fading.** On a coloured copy, faded and mid ink take that paper's hue (`#574d17` on yellow, `#3d4f66` on blue, `#6b3646` on pink); grey never sits on a tint.
- **Red means "you or a limit".** Nothing else is red.

## Typography

One face, Martian Mono (Google Fonts), used the way a receipt printer uses its font: the width axis creates double-height (`wdth` 75) and double-width (`wdth` 112.5) print; everything else is one body size per slide.

### Hierarchy
- Double-height: the slide's question or claim. 62px at `--k` 1.
- Double-width: results and totals (FREIBERUFLER, SENT BY … YOU). 50px.
- Print: every line item and sentence. 30px.
- Field label: uppercase receipt headers such as "CHECKED: OFFICIAL PAGES IT OPENED". 24px, 0.05em tracking.
- Fine print: provenance lines ("Real reply · … · not tax advice"). 21px, the only size below body.

### Named Rules
- **One size per slide body.** A slide scales its whole receipt with `--k` (0.95–1.2) to fill the frame; ranks never come from shrinking secondary text.
- **Body text never under 24px on a 1080-wide slide**, except fine print.

## Layout

Portrait slides are 1080×1350: a running strip at top (brand left, BELEG nn/12 right), the receipt centred in the remaining area at 880px wide. Landscape scenes are 1920×1080: the receipt fitted into an 880×812 box on the left by `window.__fit`, the headline and notes centred in the right column, captions in a band from y 930. Dot leaders carry every key/value row; values stay on one line, keys may wrap.

## Elevation & Depth

Paper lifts off carbon with one shadow: `drop-shadow(0 28px 32px rgba(8,10,50,.5))`. Copies sit behind the original, rotated a few degrees, no separate shadow.

## Shapes

Receipts have no radius and serrated top and bottom edges (CSS conic-gradient mask, 26px teeth). Stamps are 12px-rounded boxes with a 5–6px red border, rotated −3° to −8°. The only rounded rectangle is the window frame around real app screenshots (14px).

## Components

### Receipt
Lines in print order: optional merchant header, double-height question, faded context line, dashed rule, checked sources with OK, double rule, double-width result, key/value rows, honest notes in red, double rule, SENT BY … YOU, fine-print provenance.

### Stamp
GEPRÜFT 25.11. beside a result word (inline), or ENTWURF · NICHT VERSANDT on the border of a quoted letter.

### Caption strip
A paper strip in the print style on the carbon stage; one or two lines of narration.

### Printing (video)
Lines appear top-down in 0.16 s opacity steps, cued to narration words; a line never prints before the line above it. A spotlighted list turns the current row red.

## Do's and Don'ts

### Do:
- Itemize sources a session actually fetched, with OK, and mark unreachable ones in red.
- End every answer receipt with who sends.
- Label real replies, fictional people, summaries and "not tax advice" in fine print.

### Don't:
- Don't use grey on a coloured paper; tint it.
- Don't add a second typeface or an italic; Martian Mono has none and receipts print none.
- Don't print values in a smaller size to fit; shorten the words.
- Don't put a marketing label above a heading; the receipt's merchant header is the only line above the cover headline.

Not canonized: the detector's remaining warnings (uppercase field labels, frame clipping, navy depth shadow) are world-native or intentional; the cover's merchant header above the headline is a judgment call, recorded here rather than generalized.
