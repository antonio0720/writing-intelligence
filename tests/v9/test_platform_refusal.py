"""Where POSIX file safety is absent, v9 refuses by name rather than walking paths unsafely.

The authorship checker, the firsthand vault and the review ledger open every
file through O_NOFOLLOW and dir_fd. Windows has neither, so on Windows each
must HOLD with PLATFORM_UNSUPPORTED. This file runs on every platform: on
Windows it exercises the real refusal; on POSIX it removes the two flags and
proves the same refusal fires, so the code path is tested in both places.
"""
import contextlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[2]
KERNEL = REPO / "prototypes" / "wi9"
sys.path.insert(0, str(KERNEL))
import wi9_fs  # noqa: E402
import wi9_ledger  # noqa: E402
import wi9_vault  # noqa: E402


def authorship():
    spec = importlib.util.spec_from_file_location("wa_platform", str(REPO / "scripts" / "wi-authorship.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextlib.contextmanager
def without_posix_safety():
    if os.name == "nt":
        yield
        return
    with mock.patch.object(os, "O_NOFOLLOW", None, create=True):
        del os.O_NOFOLLOW
        yield


def capture(fn, argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = fn(argv)
    return code, json.loads(out.getvalue())


class PlatformRefusal(unittest.TestCase):
    def test_authorship_audit_refuses(self):
        wa = authorship()
        with without_posix_safety():
            code, out = capture(wa.main, ["audit", "--input",
                                          str(REPO / "examples" / "v9" / "claim-coverage" / "dossier-cut.json")])
        self.assertEqual(3, code)
        self.assertIn("PLATFORM_UNSUPPORTED", json.dumps(out))

    def test_vault_refuses(self):
        with tempfile.TemporaryDirectory() as d, without_posix_safety():
            code, out = capture(wi9_vault.main, ["init", "--root", str(Path(d) / "vault"), "--project", "p"])
        self.assertEqual(3, code)
        self.assertEqual("PLATFORM_UNSUPPORTED", out["issues"][0]["code"])

    def test_ledger_refuses(self):
        with tempfile.TemporaryDirectory() as d, without_posix_safety():
            code, out = capture(wi9_ledger.main, ["verify", "--ledger", str(Path(d) / "ledger"),
                                                  "--authority-store", str(Path(d) / "store")])
        self.assertEqual(3, code)
        self.assertEqual("PLATFORM_UNSUPPORTED", out["issues"][0]["code"])

    def test_refusal_is_not_raised_where_posix_safety_exists(self):
        if os.name == "nt":
            self.skipTest("Windows has no O_NOFOLLOW; the refusal above is the behaviour")
        wi9_fs.require_posix()


if __name__ == "__main__":
    unittest.main()
