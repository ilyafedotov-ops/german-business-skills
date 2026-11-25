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
| `carousel-ru/german-business-kit-carousel-ru.pdf` | Russian edition: the same three situations asked in Russian with the released 0.14 kit |
| `carousel-*/slides/*.png` | The slides as 1080×1350 images for image posts or comments |
| `post/linkedin-post.md` | English and German launch posts, first comment (EN · DE · RU), video post, "real questions" post |
| `post/youtube.md`, `post/youtube.de.md`, `post/youtube.ru.md` | YouTube title, description with chapters and tags for each language |
| `post/scripts.md`, `post/scripts.de.md`, `post/scripts.ru.md` | Narration for both videos per language; the renderer reads captions from these files |
| `post/real-examples.md`, `post/real-examples.de.md`, `post/real-examples.ru.md` | The three real questions with full, unedited answers |
| `video/*.srt`, `video/*.chapters.json` | Caption tracks and chapter times from the last render |
| `video/youtube-thumbnail.png` | YouTube thumbnail, 1280×720 |
| `video/youtube-avatar.png`, `video/youtube-banner.png` | YouTube channel picture (800×800) and banner (2560×1440, text inside the 1546×423 safe area) |

The LinkedIn videos (4:5; English about 99 s, German 1:50, Russian 1:47) and the
YouTube walkthroughs (16:9; 5:38, 6:17, 6:12) are rendered to `video/` locally and
ignored by Git. German and Russian files end in `-de` and `-ru`.

## Published

- YouTube channel [German Business Kit (@GermanBusinessKit)](https://www.youtube.com/@GermanBusinessKit)
  with the walkthrough [https://youtu.be/TUkzD0C6qio](https://youtu.be/TUkzD0C6qio)
  (public since 25 November 2026, English captions from `video/german-business-kit-youtube.srt`).
- German walkthrough [https://youtu.be/rY_VdGS7mPs](https://youtu.be/rY_VdGS7mPs) and Russian walkthrough
  [https://youtu.be/sVlPgHtQ6zg](https://youtu.be/sVlPgHtQ6zg) (public since 25 November 2026, captions from
  `video/german-business-kit-youtube-de.srt` and `-ru.srt`). The three descriptions link each other.
- The LinkedIn posts in `post/linkedin-post.md` link the walkthrough in their language, the slides as PDF and the repository.

## What the videos show

- Receipt scenes built from the same content as the carousels.
- **Real apps:** unedited screenshots of Claude and Codex with the kit installed,
  from `installer/images/`: a first-step answer in Claude, the seven skills in
  Codex and a conversation in Codex, in the video's language (the English video
  shows the German Codex conversation). The conversations are fictional
  examples; nothing is submitted. These replace the earlier recording of the
  removed fictional browser prototype.
- Three real questions (Berlin, Hamburg, Munich), each asked in a fresh Claude
  Code session (Opus 5.5, high effort) on 25 November 2026. The English and German
  answers come from the released `v0.13.0-preview.2` bundle and their footers keep
  that version; the Russian questions were asked in Russian with the released
  `v0.14.0-preview.1` bundle and are labelled 0.14.

## Design

- `PRODUCT.md`: product facts used for the design.
- `DIRECTION.md`: the chosen direction (receipt / Beleg).
- `DESIGN.md`: tokens, type, components and rules of the receipt world.

## Rebuild

Use the repository's development dependencies (`npm ci` at the repository root
and `npx playwright install chromium`), plus `ffmpeg` for the videos. From
`presentation/build/`:

```sh
python3 make_receipts.py                 # writes receipt-{en,de,ru}.html and scenes-receipt-yt-{en,de,ru}.html
node render-receipts.cjs en              # carousel-en: PNGs + PDF (also de, ru)
node render-video.cjs linkedin           # video/german-business-kit-linkedin.mp4 + .srt + .chapters.json
node render-video.cjs youtube            # video/german-business-kit-youtube.mp4 + .srt + .chapters.json
node render-video.cjs youtube --lang de  # video/german-business-kit-youtube-de.mp4 (also linkedin, and --lang ru)
node render-thumbnail.cjs thumbnail-receipt.html
node render-channel-art.cjs              # video/youtube-avatar.png + youtube-banner.png
```

`render-video.cjs` reads narration text from `post/scripts.md` (or
`post/scripts.de.md`, `post/scripts.ru.md` with `--lang`) and audio from
`audio/*.mp3` (or `audio/de/`, `audio/ru/`). Demo framing is computed from the
screenshot heights, so re-captured screenshots need no new offsets. Add `--stills 3,20,45` to preview single frames, or set
`CAPS=only` to print the timeline and caption breaks without rendering. Martian
Mono and the QR/barcode libraries load from Google Fonts and cdnjs at render time.
`swift check-qr.swift <png>` decodes the QR codes. After a re-render, update the
chapter times in `post/youtube*.md` from the matching `video/*.chapters.json`.

## Narration and music

Narration and the instrumental bed were generated with Runway (Eleven v4): English
voice "Niki", German "Carla Blum", Russian "Angelina". `audio/tasks.json`,
`audio/de/tasks.json` and `audio/ru/tasks.json` list the task ID of each current
clip. Changing a line in a scripts file means generating that clip again with the
same voice.

## Asking new real questions

1. Export a released bundle into an empty folder:
   `git archive v<VERSION> .claude-plugin plugin.json skills | tar -x -C <kit-dir>`.
2. Run `build/qa/run.sh <kit-dir> <empty-work-root> <name> "<question>"` for each
   question. It starts an isolated Claude Code session without user settings,
   plugins or MCP servers; tools are limited to web search/fetch, reading and
   Python for arithmetic. Keep the session logs outside Git.
3. Inspect a run with `build/qa/summarize.py <name>/turn1.jsonl`, export readable
   answers with `build/qa/export.py <work-root> <out.md> [de|ru]`, then edit the
   slide content in `build/make_receipts.py`. Every OK line must name a page the
   session actually fetched; show unreachable sources in red.
