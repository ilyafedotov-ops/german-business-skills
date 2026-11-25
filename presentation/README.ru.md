# Материалы для запуска

[English](README.md) · [Русский](README.ru.md)

Материалы German Business Kit для LinkedIn и YouTube в дизайне «Beleg» (чек)
вместе с исходниками. Люди в примерах вымышлены; три ответа на слайдах 5–7 —
настоящие ответы в сокращении. Здесь нет деловых записей и налоговых
консультаций. Готовые видео (MP4) в Git не хранятся; соберите их командами ниже.

## Готово к использованию

| Файл | Назначение |
| --- | --- |
| `carousel-en/german-business-kit-carousel-en.pdf` | Английский документ для LinkedIn: 12 слайдов 1080×1350, три настоящих вопроса с ответами на английском (слайды 5–7) |
| `carousel-de/german-business-kit-carousel-de.pdf` | Немецкая версия: те же вопросы, заданные и отвеченные по-немецки |
| `carousel-*/slides/*.png` | Слайды как изображения 1080×1350 для постов или комментариев |
| `post/linkedin-post.md` | Английский и немецкий посты, первый комментарий, пост с видео и пост «настоящие вопросы» |
| `post/youtube.md` | Название, описание с главами и теги для YouTube |
| `post/scripts.md` | Текст озвучки обоих видео; из него же строятся субтитры |
| `post/real-examples.md`, `post/real-examples.de.md` | Три настоящих вопроса с полными неотредактированными ответами |
| `video/*.srt`, `video/*.chapters.json` | Субтитры и время глав из последней сборки |
| `video/youtube-thumbnail.png` | Обложка YouTube, 1280×720 |
| `video/youtube-avatar.png`, `video/youtube-banner.png` | Аватар канала YouTube (800×800) и баннер (2560×1440, текст в безопасной зоне 1546×423) |

Видео для LinkedIn (4:5, около 99 с) и обзор для YouTube (16:9, около 5:38)
собираются локально в `video/` и игнорируются Git.

## Опубликовано

- Канал YouTube [German Business Kit (@GermanBusinessKit)](https://www.youtube.com/@GermanBusinessKit)
  с обзором [https://youtu.be/TUkzD0C6qio](https://youtu.be/TUkzD0C6qio)
  (публичный с 25 ноября 2026 года, английские субтитры из `video/german-business-kit-youtube.srt`).
- Посты LinkedIn в `post/linkedin-post.md` ссылаются на это видео, слайды в PDF и репозиторий.

## Что показывают видео

- Сцены-чеки с тем же содержанием, что и карусели.
- **Настоящие приложения:** неотредактированные скриншоты Claude и Codex с
  установленным набором из `installer/images/`: ответ с первым шагом в Claude,
  семь скиллов в Codex и разговор на немецком в Codex. Разговоры — вымышленные
  примеры, ничего не отправляется. Они заменили прежнюю запись удалённого
  вымышленного браузерного прототипа.
- Три настоящих вопроса (Берлин, Гамбург, Мюнхен), каждый в новом сеансе Claude
  Code (Opus 5.5, высокое усилие) 25 ноября 2026 года с выпущенным пакетом
  `v0.13.0-preview.2`. В подписях осталась эта версия: для 0.14 ответы не
  перезапускались.

## Дизайн

- `PRODUCT.md`: факты о продукте, использованные в дизайне.
- `DIRECTION.md`: выбранное направление (чек / Beleg).
- `DESIGN.md`: токены, шрифты, компоненты и правила «чекового» стиля.

## Пересборка

Нужны зависимости разработки репозитория (`npm ci` в корне и
`npx playwright install chromium`), а для видео — `ffmpeg`. Из
`presentation/build/`:

```sh
python3 make_receipts.py                 # пишет receipt-en.html, receipt-de.html, scenes-receipt-yt.html
node render-receipts.cjs en              # carousel-en: PNG + PDF
node render-receipts.cjs de              # carousel-de: PNG + PDF
node render-video.cjs linkedin           # video/german-business-kit-linkedin.mp4 + .srt + .chapters.json
node render-video.cjs youtube            # video/german-business-kit-youtube.mp4 + .srt + .chapters.json
node render-thumbnail.cjs thumbnail-receipt.html
node render-channel-art.cjs              # video/youtube-avatar.png + youtube-banner.png
```

`render-video.cjs` берёт текст озвучки из `post/scripts.md`, а звук — из
`audio/*.mp3`. Флаг `--stills 3,20,45` сохраняет отдельные кадры для проверки,
`CAPS=only` печатает таймлайн и разбивку субтитров без сборки. Шрифт Martian Mono
и библиотеки QR/штрихкода загружаются из Google Fonts и cdnjs во время сборки.
`swift check-qr.swift <png>` декодирует QR-коды. После пересборки обновите время
глав в `post/youtube.md` по `video/german-business-kit-youtube.chapters.json`.

## Озвучка и музыка

Озвучка (голос Runway «Niki») и инструментальная подложка созданы в Runway;
`audio/tasks.json` содержит ID задачи каждого текущего фрагмента. Если меняется
строка в `post/scripts.md`, этот фрагмент нужно сгенерировать заново тем же голосом.

## Новые настоящие вопросы

1. Экспортируйте выпущенный пакет в пустую папку:
   `git archive v<VERSION> .claude-plugin plugin.json skills | tar -x -C <kit-dir>`.
2. Для каждого вопроса запустите `build/qa/run.sh <kit-dir> <empty-work-root> <name> "<question>"`.
   Скрипт открывает изолированный сеанс Claude Code без пользовательских
   настроек, плагинов и MCP-серверов; инструменты ограничены веб-поиском,
   чтением и Python для арифметики. Журналы сеансов храните вне Git.
3. Проверьте запуск через `build/qa/summarize.py <name>/turn1.jsonl`, выгрузите
   ответы через `build/qa/export.py <work-root> <out.md> [de]` и обновите
   содержимое слайдов в `build/make_receipts.py`. Каждая строка OK должна
   называть страницу, которую сеанс действительно открыл; недоступные источники
   показывайте красным.
