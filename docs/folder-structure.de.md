# Arbeitsordner und Sprache

[English](folder-structure.md) | [Русский](folder-structure.ru.md) | [Deutsch](folder-structure.de.md)

Stand: 25.10.2026. Die technischen Ordner tragen bisher englische Namen. Eine russische Gesprächssprache ändert diese Namen nicht. Deutsch wird in einigen Einstellungen akzeptiert; mehrere Befehle und Ausgaben unterstützen jedoch nur Englisch/Russisch oder verwenden Englisch als Ersatz. Vollständige deutsche Unterstützung ist noch nicht umgesetzt.

Die Trennung zwischen `04_accounting` und `06_bookkeeping` ist für Nutzer unklar: Beide wirken wie ein Ablageort für Rechnungen. Der Eingang unter `00_admin/inbox` ist schwer zu finden. Profil, Indizes und Änderungshistorie sollten keine alltäglichen Ablageentscheidungen erfordern.

Bereits verbessert: Neue Arbeitsbereiche erzeugen nicht mehr alle zwölf Monate mit jeweils drei Unterordnern. Der benötigte Monat und sein Originalordner entstehen beim Import. Dadurch entfallen 49 leere Verzeichnisse beim Start. Bestehende Ordner und Dateien bleiben erhalten.

## Empfohlene Bereiche

| Ordner | Zweck |
| --- | --- |
| `01 Eingang` | Gemischte Unterlagen, die noch eingeordnet werden müssen |
| `02 Dokumente` | Erhaltene Originale und zugehörige aufbereitete Dateien |
| `03 Buchhaltung` | Kontoauszüge, Buchungsdaten und Berichte |
| `04 Steuern` | Erklärungen, steuerlicher Schriftverkehr und Übermittlungsnachweise |
| `05 Unternehmen` | Anmeldung, Verträge und sonstiger geschäftlicher Schriftverkehr |

Diese Namen sind **ein Vorschlag**; die aktuellen Schreibwerkzeuge verwenden diese Pfade noch nicht. Zu entscheiden ist, ob neue Arbeitsbereiche tatsächlich übersetzte Ordner im Explorer/Finder bekommen oder die Bezeichnungen nur in Oberfläche und Anleitung erscheinen. Physische Ordnernamen benötigen eine gemeinsame, geprüfte Pfadzuordnung für alle Werkzeuge.

Unterordner sollen erst bei Bedarf entstehen. Dokumente lassen sich nach `JJJJ/MM` gliedern, darunter beispielsweise `Originale` und `Aufbereitet`. Die Oberfläche zeigt Monatsnamen. Ein Ablagemonat legt keinen steuerlichen Zeitraum fest. Originalnamen und Dateiinhalte bleiben erhalten; verständliche Titel gehören in den Katalog. Mehrere Aufgaben können auf ein Original verweisen, ohne es mehrfach abzulegen.

Profil, Indizes, Historie und technische Konfiguration gehören in einen gekennzeichneten internen Bereich. Dieser ist keine Zugriffssicherung und muss mitgesichert werden. Nutzer müssen die steuerliche Einordnung nicht vor dem Eingang gemischter Unterlagen festlegen; offene Fragen bleiben sichtbar.

Selbst geführte Buchhaltung ist der Hauptablauf. Optionale Exporte gehören zu Berichten; die Übergabe an einen Steuerberater bestimmt nicht die Ordnerstruktur. Dokumentprüfung, Buchung, vorbereitete Erklärung, Übermittlung und Antwort des Finanzamts bleiben getrennte Zustände.

## Bestehende Arbeitsbereiche

Bestehende technische Ordner nicht manuell umbenennen: gespeicherte Verweise können dadurch ungültig werden. Eine spätere Migration benötigt Vorschau, geprüfte Sicherung, Kollisionsprüfung, vollständige Zuordnung aller Verweise, Hashprüfung der Originale und einen nachvollziehbaren Abschluss.

Ordnersprache und Gesprächssprache sollen getrennt gespeichert werden. Ein Wechsel der Assistentensprache darf ein bestehendes Archiv nicht umbenennen. Amtliche Formularbezeichnungen bleiben unverändert und werden in der gewählten Sprache erklärt.

Abnahmekriterium: Nutzer können auf Russisch oder Deutsch beginnen, gemischte Unterlagen hinzufügen und später fortfahren, ohne englische Anweisungen verstehen zu müssen. Windows und macOS müssen dieselben Regeln verwenden; Sprachwechsel und bestehende Archive dürfen Originale nicht verändern.

Diese Änderung setzt nur die bedarfsgerechte Anlage der Monate um. Übersetzte physische Ordner, Migration und eine übersetzte Prototyp-Oberfläche stehen noch aus. Der [technische Überblick](folder-structure.md) enthält die dreisprachige Zuordnung.
