"""Static guided installer: complete EN/RU/DE wording, official links, offline page."""
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlparse

from tools.check_doc_links import anchors
from tools.skill_catalog import skill_names


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "installer"
LANGUAGES = ("en", "ru", "de")
REPOSITORY = "ilyafedotov-ops/german-business-skills"
# Provider hosts checked on the date recorded in links.js, plus this project on GitHub.
OFFICIAL_HOSTS = {
    "claude.ai", "claude.com", "support.claude.com", "privacy.claude.com",
    "chatgpt.com", "learn.chatgpt.com", "help.openai.com",
    "persistent.oaistatic.com", "get.microsoft.com", "github.com",
    "digital-strategy.ec.europa.eu",
}
# Answers to the "would you share this?" check; the wording lives in text.js.
QUIZ = {"demo": "ok", "question": "ok", "customer": "check", "letter": "check",
        "elster": "never", "banking": "never"}


def data(name, variable):
    """The page loads plain scripts; their single assignment must stay strict JSON."""
    text = (INSTALLER / name).read_text(encoding="utf-8")
    match = re.fullmatch(r"/\*[^*]*\*/\n" + re.escape(f"window.{variable} = ") + r"(\{.*\});\n", text, re.S)
    if not match:
        raise AssertionError(f"{name} must contain one JSON assignment to window.{variable}")
    return json.loads(match[1])


def shape(value, path="$"):
    if isinstance(value, dict):
        return {key: shape(item, f"{path}.{key}") for key, item in value.items()}
    if isinstance(value, list):
        return [shape(item, f"{path}[{index}]") for index, item in enumerate(value)]
    if not isinstance(value, str) or not value.strip():
        raise AssertionError(f"Empty or non-text locale value at {path}")
    return ("text", tuple(sorted(set(re.findall(r"\{([a-zA-Z]+)\}", value)))), value.count("**") % 2)


def strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    else:
        yield value


class InstallerContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = data("text.js", "INSTALLER_TEXT")
        cls.links = data("links.js", "INSTALLER_LINKS")
        cls.skills = list(skill_names((ROOT / "skills/de-business-kit/assets/skill-set.json").read_bytes()))

    def test_every_language_has_the_same_complete_structure(self):
        self.assertEqual(tuple(self.text), LANGUAGES)
        english = shape(self.text["en"])
        for language in LANGUAGES:
            with self.subTest(language=language):
                translated = shape(self.text[language])
                self.assertEqual(translated, english)
                self.assertFalse([s for s in strings(self.text[language]) if s.count("**") % 2],
                                 "Unbalanced **emphasis**")
                if language != "en":
                    same = [s for s in strings(self.text[language]) if s in set(strings(self.text["en"]))
                            and re.search(r"[a-z]{4} [a-z]{4}", s)]
                    self.assertEqual(same, [], "English sentences left untranslated")

    def test_skill_names_and_demo_requests_stay_machine_readable(self):
        for language in LANGUAGES:
            with self.subTest(language=language):
                locale = self.text[language]
                self.assertEqual(list(locale["skills"]["list"]), self.skills)
                for name, demo in locale["demos"]["items"].items():
                    invoked = re.findall(r"de-business-[a-z]+", demo["prompt"])
                    self.assertTrue(invoked, f"{name} request must call a skill")
                    self.assertTrue(set(invoked) <= set(self.skills), invoked)
                self.assertIn("[", locale["skills"]["openai"]["manualPrompt"])
                self.assertEqual(re.findall(r"de-business-[a-z]+", locale["safety"]["ask"]), ["de-business-kit"])

    def test_kit_install_starts_with_one_request_to_the_assistant(self):
        # Beginners paste one request; the click-by-click routes stay as a fallback.
        readme = {"en": ROOT / "README.md", "ru": ROOT / "README.ru.md"}
        for language in LANGUAGES:
            for provider in ("claude", "openai"):
                with self.subTest(language=language, provider=provider):
                    info = self.text[language]["skills"][provider]
                    self.assertIn(f"https://github.com/{REPOSITORY}", info["prompt"])
                    self.assertNotIn("[", info["prompt"], "The request must work without editing")
                    self.assertTrue(info["promptLabel"].strip())
                    self.assertLessEqual(len(info["steps"]), 4)
                    self.assertGreaterEqual(len(info["manualSteps"]), 4)
                    self.assertTrue(info["manualTitle"].strip())
                    if language in readme:
                        quoted = re.findall(r"^> (.*German Business Kit.*github\.com.*)$",
                                            readme[language].read_text(encoding="utf-8"), re.M)
                        self.assertIn(info["prompt"], quoted, "Keep the request identical to the README")

    def test_pages_stay_short_and_recommend_only_paid_plans(self):
        # Each page shows a few short steps; the detailed steps stay for "More…".
        for language in LANGUAGES:
            with self.subTest(language=language):
                locale = self.text[language]
                for provider in ("claude", "openai"):
                    for step in ("account", "app", "skills"):
                        short = locale[step][provider]["short"]
                        self.assertLessEqual(len(short), 4, f"{step}.{provider}.short")
                        self.assertLessEqual(max(len(item.split()) for item in short), 30, f"{step}.{provider}.short")
                    self.assertTrue(locale["assistant"][provider]["summary"].strip())
                openai = locale["assistant"]["openai"]
                for text in (locale["assistant"]["unsure"], openai["summary"], *openai["points"],
                             *locale["account"]["openai"]["steps"], *locale["account"]["openai"]["short"]):
                    self.assertNotRegex(text, r"\*\*Free\*\*|бесплатно|kostenlos|without paying", "Recommend paid plans only")
                safety = locale["safety"]
                self.assertEqual(len(safety["warnings"]), 3)
                self.assertIn("MIT", safety["license"])
                self.assertIn(safety["understand"], safety["question"], "The question names the option to choose")

    def test_data_and_risk_step_covers_both_providers_and_the_share_check(self):
        app = (INSTALLER / "app.js").read_text(encoding="utf-8")
        table = re.search(r"const QUIZ = \{([^}]*)\};", app)
        if table is None:
            self.fail("app.js must define the QUIZ answer table")
        self.assertEqual(dict(re.findall(r"(\w+): '(\w+)'", table[1])), QUIZ)
        for language in LANGUAGES:
            with self.subTest(language=language):
                safety = self.text[language]["safety"]
                self.assertEqual(list(safety["quiz"]), list(QUIZ))
                self.assertEqual(set(safety["quizChoices"]), set(QUIZ.values()))
                for provider in ("claude", "openai"):
                    self.assertGreaterEqual(len(safety[provider]["steps"]), 2)
        privacy = self.links["privacy"]
        self.assertEqual(set(privacy), {"claude", "openai", "aiAct"})

    def test_links_are_official_https_and_match_the_published_release(self):
        self.assertRegex(self.links["checked"], r"^20[0-9]{2}-[01][0-9]-[0-3][0-9]$")
        for url in strings(self.links):
            if not url.startswith(("http:", "https:", "//")):
                continue
            with self.subTest(url=url):
                parsed = urlparse(url)
                self.assertEqual(parsed.scheme, "https")
                self.assertIn(parsed.hostname, OFFICIAL_HOSTS)
        catalog = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        [plugin] = catalog["plugins"]
        tag = plugin["source"]["ref"]
        version = tag.removeprefix("v")
        release = self.links["release"]
        self.assertEqual(self.links["marketplace"], plugin["source"]["repo"])
        self.assertEqual(release["page"], f"https://github.com/{REPOSITORY}/releases/tag/{tag}")
        prefix = f"https://github.com/{REPOSITORY}/releases/download/{tag}/"
        self.assertEqual(release["codexZip"], prefix + f"de-business-kit-{version}-codex.zip")
        self.assertEqual(release["checksums"], prefix + "SHA256SUMS")

    def test_documentation_links_resolve_to_existing_headings(self):
        prefix = f"https://github.com/{REPOSITORY}/blob/main/"
        self.assertEqual(set(self.links["docs"]), set(LANGUAGES))
        for language, docs in self.links["docs"].items():
            for key, url in docs.items():
                with self.subTest(language=language, key=key):
                    self.assertTrue(url.startswith(prefix), url)
                    path, _, fragment = url.removeprefix(prefix).partition("#")
                    target = ROOT / unquote(path)
                    self.assertTrue(target.is_file(), path)
                    if fragment:
                        self.assertIn(unquote(fragment), anchors(target.read_text(encoding="utf-8")))

    def test_page_is_static_and_offline(self):
        page = (INSTALLER / "index.html").read_text(encoding="utf-8")
        policy = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', page)
        if policy is None:
            self.fail("The page must declare its Content-Security-Policy")
        for directive in ("default-src 'self'", "script-src 'self'", "connect-src 'none'",
                          "form-action 'none'", "object-src 'none'"):
            self.assertIn(directive, policy[1])
        references = re.findall(r'(?:src|href)="([^"#:]+)"', page)
        self.assertTrue(references)
        for reference in references:
            self.assertTrue((INSTALLER / reference).is_file(), reference)
        self.assertTrue((INSTALLER / self.links["local"]["screenshot"]).resolve().is_file())
        # Real-app screenshots for every step, assistant and language.
        results = self.links["local"]["results"]
        self.assertEqual(set(results), {"skills", "first"})
        for step, providers in results.items():
            self.assertEqual(set(providers), {"claude", "openai"})
            for provider, files in providers.items():
                self.assertEqual(set(files), set(LANGUAGES))
                for language, file in files.items():
                    with self.subTest(step=step, provider=provider, language=language):
                        self.assertTrue((INSTALLER / file).is_file(), file)
                        self.assertLess((INSTALLER / file).stat().st_size, 400_000, "Keep screenshots small")


if __name__ == "__main__":
    unittest.main()
