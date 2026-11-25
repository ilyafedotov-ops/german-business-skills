# Hilfe in ELSTER und Ihrer Buchhaltungssoftware

[English](assisted-services.en.md) · [Русский](assisted-services.ru.md) · **Deutsch**

Sie können den Assistenten bitten, einen Dienst zu bedienen, nicht nur ihn zu
erklären. Zum Beispiel: **„Hilf mir, diesen Entwurf auszufüllen; ich prüfe und
übermittle ihn selbst.“** Mit passenden, erlaubten Browser- oder Computer-Werkzeugen
kann er unterstützte Felder ausfüllen, das Ergebnis prüfen und Sie durch die
restlichen Schritte führen. Die Verfügbarkeit wird für Ihre tatsächliche App, Ihr
Konto und den angefragten Vorgang geprüft.

Beginnen Sie mit der [Anleitung zum Aufruf eines Skills](user-guide.de.md#einen-skill-aufrufen). Für eine Aufgabe rund um den Zugang zu einem Dienst wählen Sie `de-business-services`; für die Geschäftsaufgabe unten nennen Sie `de-business-operations`.

## Wann Browser- oder Computer-Werkzeuge einschalten

German Business Kit liefert die fachlichen Anweisungen. Ihr Assistent liefert die
eigentlichen Werkzeuge, Hilfs-Skills und Berechtigungen. Ein eingeschalteter Skill
allein verbindet keine Bank, öffnet keine Browsersitzung und erlaubt keine Änderungen.

| Ihre Aufgabe | Nützliche Funktion |
| --- | --- |
| Aktuelle Regeln recherchieren oder öffentliche Hilfeseiten lesen | Websuche/Seiten lesen; interaktiver Browser- oder Desktopzugriff ist meist unnötig. |
| Daten über eine vorhandene unterstützte Verbindung lesen oder aktualisieren | Der passende Connector mit seinen begrenzten Berechtigungen; keine zusätzliche Browser-Einrichtung für Vorgänge, die er bereits unterstützt. |
| Eine unterstützte Website bedienen, einen Entwurf prüfen, vereinbarte Felder ausfüllen oder einen ausgewählten Export holen | Interaktive Browser-Werkzeuge; prüfen Sie die Unterstützung für die tatsächliche Website, das Konto, den Speicher-/Download-/Upload-Vorgang und die Daten. |
| In einer installierten Anwendung ohne passenden Connector oder Browserweg arbeiten | Native Computer-Steuerung, nur wenn der Host diese App, das Betriebssystem, den Vorgang und die Daten unterstützt. |
| Eine Frage erklären oder mit einer bereits gelieferten Datei arbeiten | Chat und Datei-/Dokumentwerkzeuge; Browser- oder Computerzugriff ist optional. |

**Prüfen Sie die Eignung vor sensiblen Konten.** Anthropic rät derzeit ausdrücklich
davon ab, den eingebauten Browser oder die Chrome-Integration für Finanzkonten,
Gesundheitsdaten oder personenbezogene Daten anderer zu nutzen, und davon, Banking-,
Gesundheits- oder Behörden-Apps nativ steuern zu lassen. Manche Websites sind
gesperrt. Umgehen Sie eine Browser-Einschränkung nicht mit Desktop-Steuerung. Prüfen
Sie für echte Arbeit in ELSTER, bei der Bank oder mit Kundendaten zuerst die aktuellen
Einschränkungen und Verarbeitungsbedingungen des gewählten Hosts; nutzen Sie eine
passende unterstützte Verbindung, eine angemessen reduzierte Datei oder einen
geführten manuellen Weg, wenn die Steuerung der Oberfläche ungeeignet ist. Werte
vorbereiten und Nachweise prüfen können Sie auch, ohne dem Assistenten die Kontrolle
über ein Portal zu geben. [Hinweise zur Datenverarbeitung](user-guide.de.md#ki-grenzen-und-ihre-daten).

### Die Funktion in Ihrer App einschalten

Diese von den Anbietern dokumentierten Wege wurden am **26. Oktober 2026** geprüft.
Namen, Verfügbarkeit und Richtlinien von Organisationen können abweichen; der
Assistent soll prüfen, was tatsächlich verfügbar ist, statt zu behaupten, dass es
für jeden Nutzer einen bestimmten Schalter gibt.

| App/Weg | Einrichtung, sofern angeboten |
| --- | --- |
| Codex / ChatGPT desktop, eingebauter Browser | Bitten Sie darum, **@Browser** zu nutzen. Er verwendet ein eigenes Browserprofil; Zugriffe verwalten Sie unter **Settings → Browser → Agent permissions**. Uploads von Dateien kann er derzeit nicht automatisieren; erledigen Sie diese manuell oder nutzen Sie einen anderen unterstützten Weg. [Browser-Anleitung](https://learn.chatgpt.com/docs/browser). |
| Codex mit Ihrer vorhandenen Browsersitzung | **Settings → Computer Use → Browser wählen → Install** für die offizielle Erweiterung; kehren Sie zurück, um **Manage** zu bestätigen, und wählen Sie dann im Gespräch **@Chrome**, **@Edge** oder den unterstützten Browser. [Anleitung zur Erweiterung](https://learn.chatgpt.com/docs/chrome-extension). |
| Codex mit nativen Anwendungen | **Plugins → Computer Use → Install plugin/Enable**, Server- und Skill-Steuerung einschalten, dann **Try now**. Prüfen Sie App-Berechtigungen unter **Settings → Computer use** und die abgefragten Berechtigungen des Betriebssystems. [Anleitung Computer Use](https://learn.chatgpt.com/docs/computer-use). |
| Claude Cowork, Browser | Wo verfügbar, braucht der eingebaute Browser keine Erweiterung. Wählen Sie ihn unter **Settings → Cowork → Preferred browser**. Für vorhandene Chrome-Tabs nutzen Sie **Customize → Connectors → Claude in Chrome → Configure** und schalten ihn dann für das Gespräch ein. [Eingebauter Browser](https://support.claude.com/en/articles/16607400-use-the-built-in-browser-in-claude-cowork), [Chrome-Einrichtung](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome). |
| Claude mit nativen Anwendungen | Aktuelle Beta: Pro/Max auf unterstütztem macOS/Windows-Desktop. Nutzen Sie **Settings → Capabilities** oder, falls angezeigt, **System → This computer → Enable computer use**; prüfen Sie den App-Zugriff. Die aktuelle Dokumentation schließt Team/Enterprise von dieser nativen Funktion aus. [Einrichtung und Grenzen der Computer-Steuerung](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer-in-cowork). |

Beginnen Sie mit dem kleinsten nötigen Zugriff. Lassen Sie Anmeldung, MFA und
Zertifikate im offiziellen, von Ihnen gesteuerten Ablauf; teilen Sie nie Geheimnisse
im Chat. Browserinhalte, Bildschirmfotos und Werkzeugergebnisse können den
KI-Anbieter erreichen. Prüfen Sie den angefragten Umfang und blenden Sie
unbeteiligte sensible Inhalte vor dem Bildschirmzugriff aus. Eingeschaltete
Steuerung erlaubt weder Versand noch Kauf, Zahlung oder Übermittlung; der Umfang
Ihrer Aufgabe und jeder abschließende Schritt, den Sie sich vorbehalten, gelten
weiter. Sie können den Zugriff im Host wieder abschalten. Schalten Sie keine
Sicherheitsfunktionen ab und installieren Sie keine beliebigen Werkzeuge.

Probieren Sie zuerst eine öffentliche oder erfundene Aufgabe:

> Nutze de-business-services. Prüfe, ob du diese öffentliche Hilfeseite mit den verfügbaren Browser-Werkzeugen öffnen und lesen kannst. Melde dich nicht an, fülle keine Formulare aus und ändere nichts. Sag mir, was du tatsächlich beobachtet hast und ob dieses Werkzeug die Interaktion unterstützt, die ich später brauche.

Der Assistent soll gegebenenfalls die Anweisungen des installierten Hilfs-Skills
lesen und nach der Einrichtung einen kleinen erlaubten Vorgang prüfen.
**Eingerichtet** ist nicht dasselbe wie **für diesen Vorgang getestet**. Fehlt das
Werkzeug oder möchten Sie es nicht einschalten, arbeiten Sie mit einem
Feld-Arbeitsblatt, einem ausgewählten Export oder manuellen Schritten weiter. Das Kit
braucht dafür weder Python noch Playwright oder eine Entwicklungsumgebung.

## 1. Sagen Sie, was Sie fertigstellen möchten

Nennen Sie den Dienst und das Ergebnis, etwa ein Anmeldeformular vorbereiten, einen
Rechnungsentwurf bearbeiten oder die Dokumente für Oktober herunterladen. Gibt es
schon einen Entwurf, verweisen Sie darauf. Über APIs, Connectoren oder Dateischemata
müssen Sie nichts wissen.

> Nutze de-business-operations. Ich nutze Lexware Office im Browser. Hilf mir, einen vorhandenen Rechnungsentwurf zu korrigieren.
> Fülle die bestätigten Angaben aus und zeig mir die Vorschau. Fertigstellen und
> Versenden erledige ich selbst. Sag mir, worauf du zugreifen kannst, bevor du etwas änderst.

Der Assistent prüft die verfügbaren Werkzeuge und die aktuellen Produktanleitungen.
Eine vorhandene passende Verbindung kann für unterstützte Vorgänge genutzt werden;
ein Browser kann Teile abdecken, die der Connector nicht kann. Fehlender API-Zugang
bedeutet nicht automatisch, einen höheren Tarif zu kaufen oder die
Buchhaltungssoftware zu wechseln.

## 2. Das richtige Konto öffnen

Der Assistent erklärt den Weg und jeden tatsächlich fehlenden Zugang. Ist eine
Anmeldung nötig, melden Sie sich selbst auf der offiziellen Seite an, einschließlich
MFA, Zertifikaten oder CAPTCHA. Sagen Sie dann, dass Sie bereit sind. Fügen Sie keine
Passwörter, TANs, API-Schlüssel oder ELSTER-Zertifikatsdateien in das Gespräch ein.

Klären Sie vor echten persönlichen Dokumenten oder Bildschirmfotos, welche Inhalte
der KI-Dienst erhalten kann. Ein lokaler Browser bedeutet keine lokale
KI-Verarbeitung. Der Assistent soll nach Ihrer Rückkehr das vorgesehene Konto bzw.
die Firma und den Entwurf bestätigen. Wird eine neue Browser-Integration gebraucht,
soll er die unterstützte Einrichtung und die Berechtigungen erklären, bevor er Sie
bittet, sie einzuschalten; er darf keine stillschweigend installieren.

## 3. Den Entwurf vorbereiten und ausfüllen

Der Assistent sammelt nur die für diese Aufgabe nötigen Angaben und bereitet
vorgeschlagene Werte mit ihren Quellen vor. Unbekanntes bleibt offen. Er kann
freigegebene Felder anhand der tatsächlich sichtbaren Bezeichnungen ausfüllen, die
eingegebenen Werte prüfen und, wo unterstützt, einen Entwurf speichern. Eingaben
können im Dienst automatisch gespeichert werden; der vereinbarte Umfang schließt
diese Wirkung ein, bevor die Eingabe beginnt. Sie müssen nicht jedes Feld erneut
freigeben, wenn Sie diese Arbeit bereits freigegeben haben.

Bei fehlenden Angaben soll der Assistent unabhängige Felder weiter bearbeiten und
eine klare Frage stellen. Er darf keine Steuernummer, Umsatzschätzung, steuerliche
Wahl oder Formel erfinden, um ein Pflichtfeld zu überwinden. Berechnungen nutzen
geprüfte Quellen und ein passendes amtliches Werkzeug oder die gewählte Software;
nicht verfügbare Berechnungen bleiben als Lücken benannt.

**Beispiel ELSTER:**

> Hilf mir, den Fragebogen zur steuerlichen Erfassung für meine Tätigkeit in Deutschland vorzubereiten.
> Prüfe das richtige Formular und mein vorhandenes Konto. Trage die bekannten Angaben
> in einen Entwurf ein, soweit deine Werkzeuge das erlauben; frag nach fehlenden
> Wahlentscheidungen. Ich melde mich an und übermittle nach der Prüfung selbst. Erkläre
> auch, ob meine Tätigkeit eine eigene Gewerbeanmeldung braucht und ob meine Gemeinde
> einen kombinierten Weg anbietet.

Der Fragebogen zur steuerlichen Erfassung in ELSTER und die Gewerbeanmeldung bei der
Gemeinde sind getrennte Verfahren. Der Weg hängt von der tatsächlichen Tätigkeit und
dem Ort ab; ein ausgefüllter steuerlicher Fragebogen allein beweist keine
Gewerbeanmeldung.

## 4. Gemeinsam prüfen, dann selbst bestätigen

Der Assistent zeigt, was eingegeben wurde, Formular/Dokument/Jahr und Empfänger,
verbleibende Warnungen, vorgeschlagene steuerliche Wahlentscheidungen und Anlagen. Er
unterscheidet **Entwurf speichern**, **Vorschau**, **Fertigstellen**, **Versenden**
und **Übermitteln**.

Haben Sie gesagt, dass Sie selbst abschließen, überlässt der Assistent Ihnen diesen
Schritt. Er soll Ihnen sagen, wo der gespeicherte Entwurf liegt und welche beobachtete
Schaltfläche Sie nutzen, wenn Sie bereit sind. Ist ein Pflichtwert oder eine Warnung
offen, erklärt er vor der Übermittlung, was fehlt. Ein anderes Konto oder eine
wesentliche Änderung erfordert eine neue Prüfung der betroffenen Angaben.

Kehren Sie nach Ihrem Schritt in das Gespräch zurück. Der Assistent kann, wo
verfügbar, den Status oder einen nicht geheimen Beleg prüfen. Ihre Nachricht
„erledigt“ wird als Ihre Aussage festgehalten, bis ein Nachweis sie bestätigt. Ist
das Ergebnis unsicher, prüft er den Verlauf, bevor er einen weiteren Versuch vorschlägt.

## Daten exportieren oder importieren

> Lade die ausgewählten Dokumente für Oktober aus meiner Buchhaltungssoftware herunter. Prüfe den
> Datumsfilter und die Originalformate. Sperre keine Buchungen, stelle keine Entwürfe
> fertig und übertrage nichts an eine Beratung. Wenn der Export diese Wirkungen nicht
> vermeiden kann, erkläre die Alternative, bevor du weitermachst.

Manche Exporte ändern Datensätze oder senden Daten an andere Stellen. Der Assistent
prüft den gewählten Weg, bestätigt Auswahl und Nebenwirkungen, prüft dann die
tatsächlich heruntergeladenen Dateien und meldet eine nur teilweise Abdeckung. Eine
PDF-Vorschau ist nicht unbedingt das ursprüngliche Rechnungs-XML. Ein Import ist ein
eigener Schreibvorgang: Prüfen Sie Ziel, Zuordnung und Umgang mit Dubletten, bevor er
läuft. Export oder Import ändern Ihre maßgeblichen Bücher nicht stillschweigend.

Bei **Lexware Office** kann ein vorhandener Rechnungsentwurf eine Bearbeitung im
Browser erfordern; die derzeit dokumentierte API bietet weder eine Funktion zum
Aktualisieren von Rechnungen noch eine herunterladbare Rechnungsdatei für einen
Entwurf. Der Assistent darf die Rechnung nicht fertigstellen, nur um ein PDF zu
erhalten. Diese Anbieterdetails müssen bei der Nutzung erneut geprüft werden; siehe
den [datierten Nachweis amtlicher Quellen](../references/assisted-services-sources.md).

## Wenn der Assistent die Seite nicht bedienen kann

Er soll sagen, welche Funktion fehlt, und die mögliche Vorbereitung abschließen. Zum
Beispiel: „Ich kann diese Werte vorbereiten, aber in diesem Browser die Anlage nicht
hochladen. Bitte nutzen Sie die Upload-Schaltfläche auf Ihrem Bildschirm, wählen Sie
diese Datei und kehren Sie dann zurück, damit ich das Ergebnis prüfen kann.“ Er kann
ein kurzes Arbeitsblatt Feld für Feld liefern oder einen ausgewählten lokalen Export
prüfen. Für diesen Ausweichweg müssen Sie weder Python installieren noch
Schutzfunktionen abschalten.

Bewahren Sie den gespeicherten Entwurf bzw. die Referenz und den nächsten Schritt
auf, damit die nächste Sitzung fortsetzen kann. Dieses Kit liefert Abläufe, keinen
eingebauten ELSTER- oder Lexware-Connector und keine Garantie, dass jeder Bildschirm
unterstützt wird. Getestet wurden nur lokale Lexware-Beispiele; eine echte Abnahme
steht aus. [Eine Aufgabe wählen](user-guide.de.md#erste-aufgabe) · [Hilfe im Alltag](user-guide.de.md).
