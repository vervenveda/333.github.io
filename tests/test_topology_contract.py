"""Read-only topology invariants for 333 Network.

Run: python3 -m unittest discover -s tests -p 'test_topology_contract.py' -v
No external packages, network requests, writes or STOS side effects.
"""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "architecture" / "333-topology-contract.v1.json"


class Network333TopologyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.gateway = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
        cls.backend = (ROOT / "app/main.py").read_text(encoding="utf-8")

    def test_seven_application_inventory_and_existing_source(self):
        apps = self.data["subsidiaries"]
        self.assertEqual(len(apps), 7)
        self.assertEqual(len({app["id"] for app in apps}), 7)
        for app in apps:
            with self.subTest(app=app["id"]):
                self.assertTrue((ROOT / app["appPath"]).is_file())
                self.assertTrue((ROOT / app["backendRouter"]).is_file())
                self.assertTrue(app["storageKeys"])
                self.assertTrue(app["apiPrefix"].startswith("/"))

    def test_four_previously_assigned_routes_only(self):
        assigned = self.data["routes"]["assigned"]
        self.assertEqual(len(assigned), 4)
        self.assertEqual(
            {entry["number"] for entry in assigned},
            {"333-111-7777", "333-222-7777", "333-333-7777", "333-444-7777"},
        )
        for entry in assigned:
            with self.subTest(route=entry["number"]):
                number = entry["number"].replace("-", "")
                self.assertIn(number, self.gateway)
                target = entry["url"].lstrip("./")
                self.assertTrue((ROOT / target).is_file())
        app_numbers = {
            app["routeNumber"] for app in self.data["subsidiaries"]
            if app["routeNumber"] is not None
        }
        self.assertEqual(app_numbers, {
            "333-222-7777", "333-333-7777", "333-444-7777"
        })

    def test_no_pretense_of_live_or_commissioned_stos(self):
        policy = self.data["governance"]["futureSTOSPolicy"]
        self.assertEqual(policy["state"], "planned-uncommissioned")
        self.assertIs(policy["runtimeBinding"], False)
        self.assertIs(policy["secrets"], False)
        self.assertIs(policy["controlSurfaces"], False)
        self.assertEqual(policy["slotAssignments"], "not assigned")
        self.assertTrue(self.data["sharedLocalIdentity"]["notForAuthorization"])
        self.assertTrue(all(
            "terminalId" not in app and "commissioned" not in app for app in self.data["subsidiaries"]
        ))

    def test_precache_includes_all_owned_application_pages(self):
        for app in self.data["subsidiaries"]:
            with self.subTest(app=app["id"]):
                self.assertTrue(app["pwaPrecached"])
                self.assertIn(app["appPath"].split("/")[-1], self.worker)
        fleapit = next(app for app in self.data["subsidiaries"] if app["id"] == "fleapit")
        self.assertTrue((ROOT / fleapit["entryPath"]).is_file())
        self.assertIn(fleapit["entryPath"].split("/")[-1], self.worker)

    def test_backend_router_registration_is_source_declared(self):
        for app in self.data["subsidiaries"]:
            with self.subTest(app=app["id"]):
                module = app["backendRouter"].replace("/", ".").removesuffix(".py")
                self.assertIn(f'"{module}"', self.backend)

    def test_fleapit_alias_is_preserved_without_auto_migration(self):
        fleapit = next(app for app in self.data["subsidiaries"] if app["id"] == "fleapit")
        alt = fleapit["alternateImplementation"]
        self.assertEqual(alt["canonicalStatus"], "unresolved")
        self.assertIn(alt["current333DirectoryLink"], self.gateway)
        parsed = urlsplit(alt["current333DirectoryLink"])
        self.assertEqual(parsed.scheme, "https")
        self.assertEqual(parsed.netloc, "vervenveda.github.io")
        self.assertEqual(fleapit["routeNumber"], None)


if __name__ == "__main__":
    unittest.main()
