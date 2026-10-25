# Локальное распространение плагина — v0.3.0 preview

[English](distribution.md) | [Русский](distribution.ru.md)

Общие инструкции поддерживаются только в `skills/de-business-kit`. Корневой `plugin.json` задаёт переносимые метаданные Agent Plugins; `.claude-plugin/plugin.json` — небольшой адаптер Claude. Офлайн-сборщик копирует один и тот же skill в два независимых локальных marketplace-пакета. Включены лицензия, манифесты, подготовленные EN/RU README из `packaging/` и все ресурсы skill; тесты проекта, история Git, личные файлы в корне и настройки компьютера исключены. Перед сборкой проверьте общий skill: сборщик не ищет секреты в содержимом файлов.

В этой версии нет MCP-сервера, lifecycle hooks, учётных данных, автоматической установки или обновления. Установка плагина не предоставляет Python, доступ к файлам, браузерные инструменты, подписки или доступ к банку, Lexware либо ELSTER. Возможности определяются инструментами хоста, разрешениями и политикой аккаунта.

## Сборка и проверка без установки

Из проверенного исходного проекта, с Python 3.9+ без дополнительных пакетов:

```bash
python3 -B -m unittest discover -s tests -v
python3 -B tools/check_package.py
python3 -B tools/build_package.py --output /absolute/path/to/new-review-bundle
```

В Windows замените `python3` на `py -3` или установленную команду Python 3 и укажите абсолютный Windows-путь. Родительский каталог результата должен существовать. Сборщик отклоняет существующий результат, переходы через `..`, символические ссылки и результат внутри исходного проекта. Для каждой сборки выбирайте новый каталог; установленная версия не перезаписывается.

Результат содержит:

```text
new-review-bundle/
  codex/.agents/plugins/marketplace.json
  codex/plugins/de-business-kit/plugin.json
  codex/plugins/de-business-kit/skills/de-business-kit/...
  claude/.claude-plugin/marketplace.json
  claude/plugins/de-business-kit/.claude-plugin/plugin.json
  claude/plugins/de-business-kit/skills/de-business-kit/...
  codex.zip
  claude.zip
  SHA256SUMS
```

Оба воспроизводимых ZIP — **архивы для переноса marketplace**, а не файлы для прямой загрузки плагина. Перед добавлением локального marketplace распакуйте архив в новый каталог. Например:

```bash
python3 -m zipfile -l /absolute/path/to/new-review-bundle/codex.zip
python3 -m zipfile -e /absolute/path/to/new-review-bundle/codex.zip /absolute/path/to/new-extraction
```

Корнем marketplace станет `/absolute/path/to/new-extraction/codex`. Уже созданные каталоги `codex` и `claude` также предназначены для использования как корни marketplace. `SHA256SUMS` выявляет изменение байтов архива, но не подтверждает личность издателя. Храните пакеты отдельно от личных рабочих данных бизнеса.

## Необязательная установка после проверки

Следующие команды меняют настройки хоста; сборщик их не запускает.

Для Codex зарегистрируйте проверенный локальный marketplace:

```bash
codex plugin marketplace add /absolute/path/to/new-review-bundle/codex
```

Перезапустите ChatGPT desktop, откройте каталог Plugins, выберите **German Business Kit Preview** и установите **German Business Kit**. В новом чате попросите `de-business-kit` провести настройку. Доступность локального marketplace зависит от приложения и политики. Основание: [официальная документация OpenAI по упаковке и локальным marketplace](https://developers.openai.com/plugins/build/plugins), проверена 25.10.2026.

Для Claude Code сначала проверьте marketplace и плагин:

```bash
claude plugin validate /absolute/path/to/new-review-bundle/claude
claude plugin validate /absolute/path/to/new-review-bundle/claude/plugins/de-business-kit
claude plugin marketplace add /absolute/path/to/new-review-bundle/claude
claude plugin install de-business-kit@de-business-kit-preview
```

Начните новую сессию Claude Code и вызовите `/de-business-kit:de-business-kit`. Регистрация и установка используют область действия по умолчанию; сначала проверьте настройки хоста и нужную область. См. [инструкцию Claude по marketplace](https://code.claude.com/docs/en/plugin-marketplaces) и [справочник манифеста](https://code.claude.com/docs/en/plugins-reference), проверены 25.10.2026. Эти команды описывают локальный путь Claude Code; импорт в Claude Desktop/Cowork остаётся отдельной невыполненной проверкой.

Не включайте одновременно отдельно скопированный skill и его плагин в одной сессии. Сохраняйте предыдущий проверенный пакет до успешной синтетической проверки замены. Обновление skill не требует удаления или повторного создания личного рабочего пространства.

## Доказательства и оставшиеся проверки

Тесты распаковывают каждый архив, находят каталог и манифест, сравнивают каждый файл skill с общим исходником и запускают извлечённый `workspace.py` для английского и русского синтетических пространств после удаления исходного тестового пакета. Проверяются воспроизводимость, отсутствие ресурсов, расхождение метаданных, небезопасные пути и отказ от перезаписи. Это офлайн-проверки утилит и ресурсов.

25.10.2026 проверка без установки `plugin validate` в Claude Code **2.1.310** прошла для созданного локального marketplace и его плагина. Теперь оба пакета содержат EN/RU README со взаимными ссылками и первым запросом для настройки. Отдельная проверка публичного каталога по-прежнему указывает на отсутствие иконки; публикация и приёмка каталога отложены. Codex CLI **0.164.0** предоставляет команду регистрации marketplace, но регистрация и установка не запускались.

CI выполняет нативные задания `windows-latest` (Python 3.9/3.14) и `macos-latest` (Python 3.10/3.14). [Все четыре задания прошли 25.10.2026](https://github.com/ilyafedotov-ops/german-business-skills/actions/runs/40229530057) после исправления ошибки установщика при работе с корнем диска, выявленной первым запуском Windows. Python 3.9 проверяется в Windows, поскольку [набор сборок GitHub для macOS ARM64 его не предоставляет](https://github.com/actions/python-versions/blob/main/versions-manifest.json). Эти проверки запускают офлайн-утилиты Python, а не desktop-приложения.

В рамках упаковки не проверялись установка и обнаружение в desktop-приложениях, запросы разрешений, синхронизация аккаунта или полный живой процесс. Прежде чем заявлять поддержку desktop, зафиксируйте продукт и версию, ОС, язык, обнаружение, настройку, продолжение работы и результаты с синтетическими файлами. Используйте [статус проверок](validation.ru.md) и [сценарии](../evals/scenarios.json).
