"""D02: fail-closed boundaries and migration-drift checks for 333.

Stdlib-only, read-only and offline:
python3 -m unittest discover -s tests -p 'test_identity_boundaries.py' -v

Tests describe PRESENT SOURCE; they do not simulate live OHMIC, authorize
a member, provision STOS, or prove that the external service is deployed.
Known mixed-authority routes are documented as explicit migration findings
rather than silently classifying them as sovereign-authenticated.
"""
import ast
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source(path):
    return (ROOT / path).read_text(encoding="utf-8")


def dependency_names(path):
    """Inspect FastAPI Depends expressions without importing the application."""
    tree = ast.parse(source(path))
    return {
        ast.unparse(n.args[0])
        for n in ast.walk(tree)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == "Depends"
        and n.args
    }


class SovereignIdentityBoundaryTests(unittest.TestCase):
    def test_browser_handoff_not_admitted_as_member_authority(self):
        auth = source("app/dependencies/sovereign_authentication.py")
        self.assertNotIn("localStorage", auth)
        self.assertNotIn("333_identity_handoff_v1", auth)
        self.assertIn("decode_access_token(token)", auth)
        self.assertIn('UUID(str(payload["sub"]))', auth)
        self.assertIn('confirmed_id != member_id', auth)
        self.assertIn('not result.get("ok") or not result.get("active")', auth)

    def test_missing_member_token_must_reject(self):
        src = source("app/dependencies/sovereign_authentication.py")
        tree = ast.parse(src)
        fn = next(node for node in tree.body if isinstance(node, ast.AsyncFunctionDef)
                  and node.name == "get_current_sovereign_member")
        checks = [node for node in ast.walk(fn) if isinstance(node, ast.If)
                  and isinstance(node.test, ast.UnaryOp)
                  and isinstance(node.test.op, ast.Not)
                  and isinstance(node.test.operand, ast.Name)
                  and node.test.operand.id == "token"]
        self.assertTrue(any(any(isinstance(x, ast.Raise) for x in node.body) for node in checks))

    def test_missing_ohmic_authority_fails_closed(self):
        auth = source("app/dependencies/sovereign_authentication.py")
        self.assertIn("if not _authority_ready():", auth)
        self.assertIn("MemberAuthorityUnavailableError", auth)
        self.assertIn("httpx.RequestError", auth)

    def test_member_scoped_profile_operations(self):
        profile = source("app/routers/profiles.py")
        self.assertIn("Depends(get_current_sovereign_member)", profile)
        self.assertIn("get_profile(member_id=member.id)", profile)
        self.assertIn("update_profile(member_id=member.id", profile)
        self.assertNotIn("333_identity_handoff_v1", profile)

    def test_ohmic_routers_rely_on_verified_member_dependency(self):
        for name in ("hollo", "bazaar", "fleapit", "bunya"):
            with self.subTest(router=name):
                deps = dependency_names(f"app/routers/{name}.py")
                self.assertIn("get_current_sovereign_member", deps)

    def test_admin_review_has_a_role_guard_not_a_public_route(self):
        admin = source("app/routers/admin.py")
        perms = source("app/dependencies/permissions.py")
        self.assertIn("require_roles(Role.MAIL_ADMIN, Role.ADMINISTRATOR)", admin)
        self.assertIn("role_is_allowed(user.role, allowed)", perms)
        self.assertIn("Depends(get_current_user)", perms)

    def test_legacy_authority_paths_are_explicitly_tracked(self):
        # This is a migration WATCH: do not claim these are already OHMIC-backed.
        legacy = source("app/dependencies/authentication.py")
        mail = source("app/routers/even_mail.py")
        admin = source("app/routers/admin.py")
        self.assertIn("session.get(User, user_id)", legacy)
        self.assertIn("Depends(get_current_user)", mail)
        self.assertIn("require_roles(Role.MAIL_ADMIN, Role.ADMINISTRATOR)", admin)
        self.assertNotIn("get_current_sovereign_member", mail)

    def test_fleapit_csrf_adapter_fails_closed_if_authority_missing(self):
        csrf = source("app/dependencies/fleapit_csrf.py")
        fleapit = source("app/routers/fleapit.py")
        self.assertIn('import_module("app.dependencies.sovereign_csrf")', csrf)
        self.assertIn("if verifier is None:", csrf)
        self.assertIn("HTTP_503_SERVICE_UNAVAILABLE", csrf)
        self.assertIn("Depends(require_fleapit_csrf)", fleapit)
        # Missing verifier is a recorded readiness blocker, not an implicit bypass.
        if not (ROOT / "app/dependencies/sovereign_csrf.py").exists():
            self.assertIn("FleaPit writes are disabled", csrf)

    def test_no_public_333_route_or_stos_commissioning_changes(self):
        gateway = source("index.html")
        contract = source("architecture/333-topology-contract.v1.json")
        for number in ("3331117777", "3332227777", "3333337777", "3334447777"):
            self.assertIn(number, gateway)
        self.assertIn('"state": "planned-uncommissioned"', contract)
        self.assertIn('"runtimeBinding": false', contract)
        self.assertIn('"controlSurfaces": false', contract)


if __name__ == "__main__":
    unittest.main()
