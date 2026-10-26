# Arbeitsordner und Sprache

[English](folder-structure.md) | [Русский](folder-structure.ru.md) | [Deutsch](folder-structure.de.md)

Neue Arbeitsbereiche erhalten mit `start` oder dem CLI-Befehl `init` echte deutsche, russische oder englische Ordnernamen. Die Sprache wird bei der Erstellung gewählt. Bestehende Arbeitsbereiche behalten ihre Pfade. Selbst geführte Buchhaltung bleibt der Hauptablauf; Exporte sind optional.

## Fünf Bereiche für den Alltag

| Ordner | Zweck |
| --- | --- |
| `01 Eingang` | Gemischte Unterlagen vor der Übernahme |
| `02 Dokumente` | Erhaltene Originale und aufbereitete Dateien |
| `03 Buchhaltung` | Kontoauszüge, Buchungen und Berichte |
| `04 Steuern` | Vorbereitung von Erklärungen und Übermittlungsnachweise |
| `05 Unternehmen` | Anmeldung und geschäftlicher Schriftverkehr |

Im Hauptordner liegt `HIER-STARTEN.md`. Gemischte Dateien können zunächst in den Eingang; eine steuerliche Einordnung ist vorher nicht erforderlich. Das Ablegen allein ist noch kein Import und keine Prüfung.

Monate entstehen bei Bedarf, beispielsweise `02 Dokumente/2026/10/Originale/`. Der Import erhält die Quelldaten unverändert und erfasst den ursprünglichen Dateinamen; Archivkopien behalten die bisherige Benennung nach Hash. Der Ablagemonat bestimmt keinen steuerlichen Zeitraum. Mehrere Aufgaben können dasselbe Original verwenden.

Profil, Indizes und Historie liegen in `.business-kit`. Die versionierte `.workspace-layout.json` legt die Ordnersprache fest. Beide gehören in jede Sicherung. Versteckte Dateien sind keine Zugriffssicherung. Dateien und Ordner nicht manuell ändern oder umbenennen.

## Sprache und Kompatibilität

Ein Wechsel der Gesprächs- oder Berichtssprache benennt keine Ordner um. Stabile interne Verweise werden in die tatsächlichen Pfade übersetzt. Vor gewöhnlichen Dateioperationen liest der Assistent die Zuordnung mit `workspace.py folders --root <Privatordner>` oder `windows.ps1 -Action folders -Root <Privatordner>`. Englische Pfade in technischen Referenzen sind interne Kennungen.

Neue CLI-Arbeitsbereiche verwenden die übersetzte Struktur. `--layout legacy` beziehungsweise `-Layout legacy` wählt ausdrücklich die frühere Struktur. Die Python-Funktion `init_workspace` behält aus Kompatibilitätsgründen den bisherigen Standard; `start_workspace` verwendet übersetzte Ordner. Bestehende Bereiche werden unverändert fortgesetzt. Eine automatische Migration ist nicht enthalten; sie würde Vorschau, geprüfte Sicherung, Kollisionsprüfung, Verweiszuordnung und Hashprüfung benötigen.

Native Windows-Befehle für Einrichtung, Quellvorschau, Import und Integritätsprüfung nutzen dieselbe Zuordnung wie die optionalen Python-Abläufe, Berichte und Archive. Erweiterte Python-Funktionen werden dadurch nicht zu nativen Windows-Funktionen. Deutsche Ordner und die Startanleitung sind umgesetzt; Prototyp und Berichtsvorlagen sind noch nicht vollständig übersetzt. PowerShell-Prüfungen unter Linux ersetzen keine Abnahme unter Windows PowerShell 5.1. Siehe [Validierung](validation.md) und [dreisprachige Zuordnung](folder-structure.md).
