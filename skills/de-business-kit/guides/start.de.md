# Hier starten

**Deutsch** · [Русский](user-guide.ru.md#первая-задача) · [English](user-guide.en.md#first-task)

German Business Kit ist ein System von Skills für Selbstständige in Deutschland: Gründungsvorbereitung, Formulare, Fragen, Dienstleistungen, laufende Arbeit und Berichte. Anleitungen zur Vorbereitung decken auch Änderungen, die erste Einstellung, eine Pause und die Beendigung einer Tätigkeit ab; die tatsächliche Ausführung wird separat geprüft. Beschreiben Sie das gewünschte Ergebnis in normalen Worten. Eine einfache Frage erfordert weder die lokale Anwendung noch einen neuen Arbeitsordner. Eine vollständige Buchhaltungssoftware und ELSTER-Übermittlung sind nicht enthalten.

Für anspruchsvolle Aufgaben empfehlen wir **Claude Opus 5.5 / High** oder
**GPT-6 Astra / High**, sofern Ihr Konto diese Auswahl bietet. Wählen Sie Modell
und Denkaufwand in der App; die Skills ändern diese Einstellung nicht.
Ein einfaches erstes Beispiel braucht kein Upgrade. Höherer Denkaufwand kann
mehr Zeit und Nutzungskontingent benötigen; Quellen- und Rechenprüfungen bleiben
nötig. [Modellwahl und Alternativen auf Englisch](install.en.md#choose-a-model).

**KI-Unterstützung, keine professionelle Steuerberatung:** Das Kit ist ein
Selbsthilfe-Werkzeug und kein Steuerberater. KI kann sich bei Regeln, Beträgen
und Fristen irren. Inhalte gelesener Dateien können von OpenAI oder Anthropic
verarbeitet werden; ein lokaler Ordner bedeutet keine rein lokale KI.
Prüfen Sie Konto, Datenkontrollen und benötigte Inhalte vor echten Dokumenten.
[Hinweise zu Risiken und Daten auf Englisch](user-guide.en.md#ai-limits-and-your-data).

## Ihr erster Schritt

Installation in der Claude-App (kostenpflichtiger Tarif): **Cowork → Customize → Plugins → Add → Add marketplace**, `ilyafedotov-ops/german-business-skills` eingeben und **German Business Kit** installieren. Die ausführliche [Installationsanleitung](install.en.md) gibt es auf Englisch und Russisch, auch für Codex. Starten Sie danach eine neue Aufgabe in Cowork oder öffnen Sie Ihr Codex-Projekt mit den installierten Skills. Ist im Codex-Projekt nur der Ordner vorhanden, bitten Sie den Assistenten, die lokale Installation zu prüfen und die vorgesehenen Dateien und Ziele zu erklären. Ein heruntergeladenes ZIP installiert noch nichts. Python und geänderte Sicherheitseinstellungen sind keine Voraussetzung für den Einstieg.

Rufen Sie den Skill zuerst auf: In **Claude** geben Sie **/** ein oder öffnen
**+** und wählen **de-business-kit** aus **German Business Kit**. In **Codex**
schreiben Sie **„Nutze de-business-kit“** oder **`$de-business-kit`** vor Ihre
Anfrage. In Claude Code mit installiertem Plugin lautet der Aufruf
**`/de-business-kit:de-business-kit`**. Fehlt der Skill, prüfen Sie die Installation.

Wählen Sie eine Anfrage:

- **Vorhandene Unterlagen:** „Nutze de-business-accounting. Meine Unterlagen liegen in einem Ordner, in E-Mails oder in einer Buchhaltungssoftware. Zeige zuerst, was zugänglich ist. Hilf mir dann bei der Auswahl. Ändere noch nichts in der Quelle und versende nichts.“
- **Neue Tätigkeit:** „Nutze de-business-start. Hilf mir beim nächsten Schritt für meine geplante Tätigkeit … Berücksichtige meine bereits bestehenden Tätigkeiten.“
- **Fortsetzen:** „Nutze de-business-kit. Setze die Arbeit im vorhandenen Unternehmensordner fort. Was ist fertig, was ist offen und was kommt als Nächstes?“
- **Ausprobieren:** „Nutze de-business-kit. Zeige ein kleines Beispiel mit erfundenen Daten in einem getrennten Übungsordner.“

## Ordner und erster Erfolg

Wählen Sie für laufende Arbeit einen privaten Ordner außerhalb des Projekts, der Skill-Installation und aller Git-Repositories. Neue deutsche Arbeitsbereiche haben **Eingang, Dokumente, Buchhaltung, Steuern, Unternehmen** sowie `HIER-STARTEN.md`. Bestehende Bereiche bleiben unverändert. Ein Wechsel der Gesprächssprache benennt keine Ordner um. Bewahren Sie auch versteckte interne Dateien und `.workspace-layout.json` in einer vollständigen Sicherung auf; ein ausgewähltes Dokumentenarchiv ist keine vollständige Sicherung. Benennen Sie verwaltete Ordner und gespeicherte Originale nicht manuell um.

Beginnen Sie mit einer kleinen Aufgabe. Klären Sie vor echten personenbezogenen Daten den tatsächlichen Verarbeitungsweg; lokale Dateien bedeuten kein lokales KI-Modell. Zugangsdaten und Bestätigungscodes gehören nur in die offizielle Anmeldung. Ihre vorhandene Buchhaltungssoftware bleibt maßgeblich, wenn Sie sie weiterverwenden. Die Wahl kann beim Ordnen der Unterlagen zunächst offenbleiben.

> Zeige mir das lesbare Ergebnis, offene Fragen und den nächsten Schritt. Speichere eine kurze Fortsetzungsnotiz und verlinke die Datei.

Ein Entwurf ist nicht versandt; ein Übermittlungsbeleg ist keine inhaltliche Zustimmung des Finanzamts. Löschen Sie bei Problemen weder Originale noch den bestehenden Arbeitsordner. Bitten Sie um eine verständliche Diagnose.

Deutsche Ordner, diese Startanleitung und eine Briefvorlage sind vorhanden. Vollständige Berichtsvorlagen und das ausführliche Nutzerhandbuch gibt es derzeit auf [Russisch](user-guide.ru.md) und [Englisch](user-guide.en.md); eine vollständige deutsche Übersetzung ist noch nicht umgesetzt.
