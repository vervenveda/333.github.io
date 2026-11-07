"""D04 read-only offline and backup source-boundary tests.

python3 -m unittest discover -s tests -p 'test_offline_backup_boundaries.py' -v

Tests do not simulate a browser Cache API, touch member data, or commission STOS.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class OfflineBackupBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worker = read("service-worker.js")
        cls.offline = read("offline.html")
        cls.contract = json.loads(read("architecture/333-topology-contract.v1.json"))

    def test_precache_covers_all_apps_and_two_fleapit_pages(self):
        for app in self.contract["subsidiaries"]:
            with self.subTest(app=app["id"]):
                self.assertIn(app["appPath"].split("/")[-1], self.worker)
                self.assertTrue((ROOT / app["appPath"]).exists())
        self.assertIn("FleaPit™_media_gate_Index.html", self.worker)
        self.assertIn("FleaPit™ _media_hub_index.html", self.worker)

    def test_offline_fallback_includes_all_seven_destinations(self):
        links = re.findall(r'<a class="app-link"[^>]*href="([^"]+)"', self.offline)
        self.assertEqual(len(links), 7)
        self.assertEqual(len(links), len(set(links)))
        for app in self.contract["subsidiaries"]:
            expected = app.get("entryPath") if app["id"] == "fleapit" else app["appPath"]
            with self.subTest(app=app["id"]):
                self.assertIn("./" + expected, links)

    def test_runtime_cache_whitelist_and_privacy_guards(self):
        for marker in (
            "function approvedPublicCacheRequest(request)",
            "function approvedPublicCacheResponse(response)",
            'request.headers.has("Authorization")',
            "STATIC_PATHS.has(url.pathname)",
            "ASSET_EXTENSIONS.has(extension)",
            'request.mode === "navigate"',
            "url.search",
            'response.headers.get("Cache-Control")',
            'response.headers.has("Set-Cookie")',
            'type.includes("application/json")',
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.worker)
        self.assertIn("approvedPublicCacheRequest(request) && approvedPublicCacheResponse(response)", self.worker)
        self.assertIn("approvedPublicCacheRequest(request) ? await caches.match(request) : null", self.worker)

    def test_cache_version_advanced_after_policy_change(self):
        self.assertIn("CACHE_PREFIX}v8", self.worker)
        self.assertIn("key.startsWith(CACHE_PREFIX)", self.worker)

    def test_hollo_and_even_mail_backups_validate_schema_and_size(self):
        cases = [
            ("app/HOLLO_333_direct_connect_index.html", "5*1024*1024", "hollo-backup"),
            ("app/EVen_mail_index.html", "MAX_IMPORT_BYTES", "even-mail-workspace"),
        ]
        for path, limit, schema in cases:
            s = read(path)
            with self.subTest(path=path):
                self.assertIn(limit, s)
                self.assertIn(schema, s)
                self.assertIn("confirm(", s)

    def test_bazaar_and_fleapit_import_limits_are_present(self):
        self.assertIn("150*1024*1024", read("app/Bazaar_Art_Live_index.html"))
        self.assertIn("if(f.size>MAX_IMPORT)", read("app/FleaPit™ _media_hub_index.html"))

    def test_bunya_import_size_limit_is_unresolved_not_silently_claimed(self):
        s = read("app/Bunya_digital_infrastructure_index.html")
        self.assertIn("async function importWorkspace(file)", s)
        self.assertIn("JSON.parse(await file.text())", s)
        self.assertIn("normalizeWorkspace(imported)", s)

    def test_stos_stays_uncommissioned(self):
        policy = self.contract["governance"]["futureSTOSPolicy"]
        self.assertEqual(policy["state"], "planned-uncommissioned")
        self.assertIs(policy["runtimeBinding"], False)
        self.assertIs(policy["controlSurfaces"], False)

if __name__ == "__main__":
    unittest.main()
