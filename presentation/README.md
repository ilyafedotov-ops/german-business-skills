# Launch materials

[English](README.md) · [Русский](README.ru.md)

LinkedIn and YouTube materials for German Business Kit in the "Beleg" (receipt)
design, with their sources. People in the examples are fictional; the three
answers on slides 5–7 are real replies, summarized. Nothing here is a business
record or tax advice. Rendered videos (MP4) are not stored in Git; rebuild them
with the commands below.

## Ready to use

| File | Use |
| --- | --- |
| `carousel-en/german-business-kit-carousel-en.pdf` | English LinkedIn document post: 12 slides, 1080×1350, three real questions answered in English (slides 5–7) |
| `carousel-de/german-business-kit-carousel-de.pdf` | German edition: the same questions asked and answered in German |
| `carousel-*/slides/*.png` | The slides as 1080×1350 images for image posts or comments |
| `post/linkedin-post.md` | English and German launch posts, first comment, video post, "real questions" post |
| `post/youtube.md` | YouTube title, description with chapters, tags |
| `post/scripts.md` | Narration for both videos; the renderer reads captions from this file |
| `post/real-examples.md`, `post/real-examples.de.md` | The three real questions with full, unedited answers |
| `video/*.srt`, `video/*.chapters.json` | Caption tracks and chapter times from the last render |
| `video/youtube-thumbnail.png` | YouTube thumbnail, 1280×720 |

The LinkedIn video (4:5, about 99 s) and the YouTube walkthrough (16:9, about
5:38) are rendered to `video/` locally and ignored by Git.

## What the videos show

- Receipt scenes built from the same content as the carousels.
- **Real apps:** unedited screenshots of Claude and Codex with the kit installed,
  from `installer/images/`: a first-step answer in Claude, the seven skills in
  Codex and a German conversation in Codex. The conversations are fictional
  examples; nothing is submitted. These replace the earlier recording of the
  removed fictional browser prototype.
- Three real questions (Berlin, Hamburg, Munich), each asked in a fresh Claude
  Code session (Opus 5.5, high effort) on 25 November 2026 with the released
  `v0.13.0-preview.2` bundle. Their footers keep that version: the answers were
  not re-run for 0.14.

## Design

- `PRODUCT.md`: product facts used for the design.
- `DIRECTION.md`: the chosen direction (receipt / Beleg).
- `DESIGN.md`: tokens, type, components and rules of the receipt world.

## Rebuild

Use the repository's development dependencies (`npm ci` at the repository root
and `npx playwright install chromium`), plus `ffmpeg` for the videos. From
`presentation/build/`:

```sh
python3 make_receipts.py                 # writes receipt-en.html, receipt-de.html, scenes-receipt-yt.html
node render-receipts.cjs en              # carousel-en: PNGs + PDF
node render-receipts.cjs de              # carousel-de: PNGs + PDF
node render-video.cjs linkedin           # video/german-business-kit-linkedin.mp4 + .srt + .chapters.json
node render-video.cjs youtube            # video/german-business-kit-youtube.mp4 + .srt + .chapters.json
node render-thumbnail.cjs thumbnail-receipt.html
```

`render-video.cjs` reads narration text from `post/scripts.md` and audio from
`audio/*.mp3`. Add `--stills 3,20,45` to preview single frames, or set
`CAPS=only` to print the timeline and caption breaks without rendering. Martian
Mono and the QR/barcode libraries load from Google Fonts and cdnjs at render time.
`swift check-qr.swift <png>` decodes the QR codes. After a re-render, update the
chapter times in `post/youtube.md` from `video/german-business-kit-youtube.chapters.json`.

## Narration and music

Narration (Runway voice "Niki") and the instrumental bed were generated with
Runway; `audio/tasks.json` lists the task ID of each current clip. Changing a
line in `post/scripts.md` means generating that clip again with the same voice.

## Asking new real questions

1. Export a released bundle into an empty folder:
   `git archive v<VERSION> .claude-plugin plugin.json skills | tar -x -C <kit-dir>`.
2. Run `build/qa/run.sh <kit-dir> <empty-work-root> <name> "<question>"` for each
   question. It starts an isolated Claude Code session without user settings,
   plugins or MCP servers; tools are limited to web search/fetch, reading and
   Python for arithmetic. Keep the session logs outside Git.
3. Inspect a run with `build/qa/summarize.py <name>/turn1.jsonl`, export readable
   answers with `build/qa/export.py <work-root> <out.md> [de]`, then edit the
   slide content in `build/make_receipts.py`. Every OK line must name a page the
   session actually fetched; show unreachable sources in red.
