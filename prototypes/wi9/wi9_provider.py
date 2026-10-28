#!/usr/bin/env python3
"""Bring-your-own-model connector for v9 composition: gates first, the model last.

Project owner: Antonio T. Smith Jr. / Density6 LLC

v9 ships no model and holds no key. A writer who wants a draft candidate
names their own program: any local executable that reads one JSON request on
stdin and writes one JSON candidate (wi9.candidate/1) on stdout. That program
may call a hosted model with the writer's own key, or run a local one.

The order is fixed and is the point of this file:

  1. venue policy  (wi9_composition.prepare_request): human-only and unknown
     policies never reach the model; a disclosure venue needs a disclosure plan
  2. evidence      consented source cards with unique ids, or nothing is sent
  3. the writer's explicit --consent-to-send: source cards leave this process
  4. the model     run with no shell, a deadline, an output cap and an
                   environment holding only the one key variable the writer names
  5. inspection    (wi9_composition.inspect_candidate): every paragraph cites a
                   card, quotations are exact, first-person claims are anchored

The best result this can return is DRAFT_REVIEW_REQUIRED. release_authorized
is always false, whatever the model's output says. The candidate is
ai_generated and carries no authorship claim. Keys never appear in arguments,
reports, logs or source control: --key-env takes the NAME of an environment
variable, and its value is passed to the program and nowhere else.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wi9_composition import inspect_candidate, prepare_request  # noqa: E402

SCHEMA = "wi9.provider-run/1"
ENV_NAME = re.compile(r"^[A-Z_][A-Z0-9_]{0,63}$")
PASSTHROUGH_ENV = ("PATH", "LANG", "LC_ALL", "TMPDIR", "SYSTEMROOT")
DEFAULT_TIMEOUT = 120.0
MAX_TIMEOUT = 900.0
MAX_REQUEST_CHARS = 400_000
MAX_OUTPUT_BYTES = 2_000_000
MAX_DOSSIER_BYTES = 2_000_000


class ProviderRefusal(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _hold(code, detail, **extra):
    out = {"schema": SCHEMA, "status": "HOLD", "issues": [{"code": code, "detail": detail}],
           "provider_called": False, "release_authorized": False}
    out.update(extra)
    return out


def _executable(path):
    p = Path(path)
    if not p.is_absolute():
        raise ProviderRefusal("PROVIDER_PATH_RELATIVE", "name the provider program by its absolute path")
    if not p.is_file() or not os.access(str(p), os.X_OK):
        raise ProviderRefusal("PROVIDER_NOT_EXECUTABLE", "the provider is not an executable file")
    return p


def run_provider(dossier, provider_cmd, provider_args=(), key_env=None, consent_to_send=False,
                 timeout=DEFAULT_TIMEOUT, environ=None):
    environ = os.environ if environ is None else environ
    prepared = prepare_request(dossier)
    if prepared.get("status") != "REQUEST_READY":
        # Steps 1-2. The model is never reached.
        return _hold(prepared.get("reason", "REQUEST_REFUSED"),
                     "the venue policy or the evidence refused a prose request; no model was called",
                     alternative=prepared.get("alternative"))
    if consent_to_send is not True:
        return _hold("SEND_CONSENT_REQUIRED",
                     "pass --consent-to-send: the source cards leave this process to your own program")
    if key_env is not None and not ENV_NAME.match(key_env):
        return _hold("KEY_ENV_INVALID", "--key-env takes the NAME of an environment variable, never a key")
    if not isinstance(timeout, (int, float)) or not 0 < timeout <= MAX_TIMEOUT:
        return _hold("TIMEOUT_INVALID", "the deadline is between 0 and %d seconds" % MAX_TIMEOUT)
    try:
        program = _executable(provider_cmd)
    except ProviderRefusal as exc:
        return _hold(exc.code, str(exc))
    payload = json.dumps(prepared["request"], sort_keys=True, ensure_ascii=False)
    if len(payload) > MAX_REQUEST_CHARS:
        return _hold("REQUEST_TOO_LARGE", "the request exceeds %d characters" % MAX_REQUEST_CHARS)
    env = {k: environ[k] for k in PASSTHROUGH_ENV if k in environ}
    if key_env is not None:
        if key_env not in environ:
            return _hold("KEY_ENV_UNSET", "the environment variable %s is not set" % key_env)
        env[key_env] = environ[key_env]
    trace = {"request_sha256": _sha(payload.encode("utf-8")), "provider_sha256": _sha(program.read_bytes()),
             "provider": program.name, "key_env": key_env, "source_cards": len(prepared["request"]["source_cards"])}
    started = time.monotonic()
    try:
        proc = subprocess.run([str(program)] + [str(a) for a in provider_args], input=payload.encode("utf-8"),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=timeout,
                              shell=False, check=False)
    except subprocess.TimeoutExpired:
        return _hold("PROVIDER_TIMEOUT", "the provider did not answer within %s seconds" % timeout,
                     provider_called=True, trace=trace)
    except OSError as exc:
        return _hold("PROVIDER_FAILED", "the provider could not start: %s" % exc.strerror, trace=trace)
    trace["seconds"] = round(time.monotonic() - started, 3)
    if proc.returncode != 0:
        return _hold("PROVIDER_FAILED", "the provider exited %d" % proc.returncode, provider_called=True,
                     trace=trace)
    if len(proc.stdout) > MAX_OUTPUT_BYTES:
        return _hold("PROVIDER_OUTPUT_TOO_LARGE", "the provider returned more than %d bytes" % MAX_OUTPUT_BYTES,
                     provider_called=True, trace=trace)
    try:
        candidate = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return _hold("PROVIDER_OUTPUT_INVALID", "the provider did not return JSON", provider_called=True,
                     trace=trace)
    issues = []
    if isinstance(candidate, dict):
        claimed = {k for k in ("release_authorized", "approved", "verified", "human_authored", "origin")
                   if k in candidate}
        if claimed:
            # Model output is data. It cannot authorize, approve or declare authorship.
            issues.append({"code": "PROVIDER_CLAIMED_AUTHORITY",
                           "detail": "ignored provider fields: %s" % ", ".join(sorted(claimed))})
            candidate = {k: v for k, v in candidate.items() if k not in claimed}
    inspected = inspect_candidate(candidate, prepared)
    issues.extend({"code": e, "detail": "candidate inspection"} for e in inspected.get("errors", []))
    trace["candidate_sha256"] = inspected.get("candidate_sha256")
    return {"schema": SCHEMA, "status": inspected["status"], "provider_called": True,
            "candidate_text": inspected.get("candidate_text"), "candidate_origin": "ai_generated",
            "issues": issues, "trace": trace, "release_authorized": False,
            "claim_scope": inspected.get("claim_scope"),
            "next": "Read the draft against your sources, run `wi authorship meaning diff` against your own text, "
                    "and decide every change yourself. This draft cannot be submitted to a human-only venue."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True, help="a composition dossier (venue, document, evidence)")
    parser.add_argument("--provider-cmd", required=True, help="absolute path of your own model program")
    parser.add_argument("--provider-arg", action="append", default=[], help="an argument for that program")
    parser.add_argument("--key-env", help="NAME of the environment variable holding your key, never the key")
    parser.add_argument("--consent-to-send", action="store_true",
                        help="you agree the source cards leave this process to your program")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args(argv)
    try:
        path = Path(args.input)
        if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_DOSSIER_BYTES:
            raise ValueError("INPUT_NOT_A_BOUNDED_FILE")
        dossier = json.loads(path.read_text(encoding="utf-8"))
        result = run_provider(dossier, args.provider_cmd, args.provider_arg, args.key_env, args.consent_to_send,
                              args.timeout)
    except (OSError, ValueError, UnicodeError, TypeError) as exc:
        result = _hold("PROVIDER_INPUT_INVALID", "%s: %s" % (type(exc).__name__, exc))
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if result["status"] == "DRAFT_REVIEW_REQUIRED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
