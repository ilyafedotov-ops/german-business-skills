# Try the guided workspace

[English](prototype.md) | [Русский](prototype.ru.md) | [Documentation](index.md)

Open [the interactive demo](../prototype/index.html) in a current desktop browser. From a downloaded repository ZIP, extract the ZIP first, open the `prototype` folder, then double-click `index.html`. Keep `index.html`, `style.css`, `state.js` and `app.js` together. Windows and macOS users need no Python, Node, terminal commands, installation or sign-in to try it.

This is a **synthetic interaction prototype**, separate from the installed skill and its private business workspace. It uses fictional records. Do not enter real business information. The interface is currently English; this guide is available in English and Russian.

## Four things to try

1. Choose **Organize existing records** on Home. Preview the sample folder, choose files, review the selection and add them. One unsupported example is explicitly excluded. No real folder is opened or uploaded.
2. Open **Documents → Review invoice**. Compare the proposed total with the original example, correct `119.00` to `119.80` (or `119,80`), and leave the category unresolved if unsure. **Save draft** preserves work; **Mark document reviewed** checks the sample source fields. Neither records an accounting entry.
3. Open **This month → Investigate payment**. Inspect the €12 statement row and possible receipt. Add a note, leave it open or link the example receipt. No payment is initiated and no accounting entry is posted.
4. Close the tab, reopen the same file in the same browser and choose **Continue where I stopped**. The demo restores your document correction or investigation. An interrupted folder preview also retains its step and selection.

The five screens are Home, Documents, This month, Taxes and letters, and Accounts and services. Settings and demo diagnostics sit outside the main navigation. On narrow screens, navigation wraps and the original document appears above the review form.

## Help and saving

Hints appear beside fields. Expand an explanation when you need more context. **Help me with this** opens a task-specific request you can copy into your existing assistant. Nothing is sent automatically. Connection guidance first identifies the exact product and available capabilities; this demo does not connect Gmail, Lexware, sevdesk, WISO, a bank or an insurer.

Changes are stored only in this browser when its local storage accepts them. “Saved on this browser” is shown after a successful write. Failed storage or a conflicting change from another tab leaves current edits visible and reports that they were not saved. Copy them before leaving. Clearing browser data, using a different browser, private browsing or moving the demo can prevent recovery. This is not encrypted storage, synchronization or a backup.

**Settings → Reset fictional demo data** asks before replacing this demo's saved data. It never modifies your actual files or skill workspace. Browser-specific file storage behavior still needs real-device acceptance testing.

## What remains to build

The preview is a synthetic HTML document, not a PDF reader or OCR engine. Imports are sample selections, not filesystem or bank-export parsing. Taxes and letters shows workflow boundaries, not a working return editor or ELSTER transport. Service comparisons prepare an assistant request, not a current provider ranking or purchase flow. No production desktop shell or runtime was selected.

The next gate is a moderated study with nontechnical Windows/macOS users, followed by a production interface connected to validated workspace commands. Automated browser tests do not replace that study. See [design research](research/gui-ux-recommendation.md) and [verification evidence](prototype-validation.md).

## Developer checks only

End users do not need these commands. Maintainers use Node 22 and the locked Playwright development dependency:

```text
npm ci --ignore-scripts
npx playwright install chromium webkit
npm test
npm run test:browser
npm run test:browser -- --browser=webkit
```

The tests open the actual HTML file directly. Screenshots go to ignored `output/prototype/`. The prototype adds no production dependency and performs no network requests. The portable skill packages remain separate.
