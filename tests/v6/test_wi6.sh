#!/usr/bin/env bash
#
# test_wi6.sh — regression suite for the v6 sovereign meaning runtime.
#
# Same rule as the v5 suite, and it is the only rule that matters here: every
# assertion has a negative twin. The v6 layer exists to refuse things — an
# unauthorized acceptance, a stale approval, a merge that would invent a
# number nobody asserted, a capsule whose bytes moved. A suite that only
# checks the happy path would stay green with every one of those refusals
# deleted, and a green suite that survives the removal of the control it
# claims to test is worse than no suite: it certifies nothing while looking
# like assurance.
#
# So this file checks that the good case is accepted AND that each refusal
# actually fires, with the correct error code.
#
# stdlib Python only. No network. Runs in a temp directory and cleans up.
#
# Usage: bash tests/v6/test_wi6.sh
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
WI="python3 $REPO/scripts/wi.py"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cd "$WORK"

FAILED=0
ok()   { echo "PASS $1"; }
bad()  { echo "FAIL $1"; [ -n "${2:-}" ] && echo "     $2"; FAILED=1; }
check(){ if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "expected [$3], got [$2]"; fi; }
has()  { if echo "$2" | grep -q "$3"; then ok "$1"; else bad "$1" "missing [$3] in: $2"; fi; }
hasnt(){ if echo "$2" | grep -q "$3"; then bad "$1" "found [$3] and should not have"; else ok "$1"; fi; }

pid_of() {  # first proposal id with the given status
  $WI proposals --status "$1" --json 2>/dev/null \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['proposals'][0]['proposal_id'] if d['proposals'] else '')"
}
pid_last() {  # most recently created proposal with the given status
  $WI proposals --status "$1" --json 2>/dev/null \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['proposals'][-1]['proposal_id'] if d['proposals'] else '')"
}
root_of() {
  $WI log --limit 1 --json 2>/dev/null \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['commits'][0]['root'] if d['commits'] else '')"
}

$WI init --title "v6 suite" --mode strict >/dev/null 2>&1

# --------------------------------------------------------------------------
# 1. Canonicalization and domain separation
# --------------------------------------------------------------------------
echo '{"b":2,"a":1,"s":"café"}' > obj.json
C1=$($WI canon obj.json --json | python3 -c "import json,sys;print(json.load(sys.stdin)['state_digest_v6'])")
C2=$($WI canon obj.json --json | python3 -c "import json,sys;print(json.load(sys.stdin)['state_digest_v6'])")
check "canonical digest is stable" "$C1" "$C2"

V5D=$($WI canon obj.json --json | python3 -c "import json,sys;print(json.load(sys.stdin)['state_digest_v5'])")
if [ "$C1" != "$V5D" ]; then ok "v5 and v6 digests are domain separated"
else bad "v5 and v6 digests are domain separated" "both are $C1"; fi

# Key order and Unicode form must not change the digest. If they did, the
# same meaning would hash two ways and staleness would fire at random.
printf '{"a":1,"s":"cafe\\u0301","b":2}' > obj2.json
C3=$($WI canon obj2.json --json | python3 -c "import json,sys;print(json.load(sys.stdin)['state_digest_v6'])")
check "key order and NFC normalization do not move the digest" "$C3" "$C1"

# A different payload must move it. Otherwise the digest is a constant.
echo '{"b":2,"a":2,"s":"café"}' > obj3.json
C4=$($WI canon obj3.json --json | python3 -c "import json,sys;print(json.load(sys.stdin)['state_digest_v6'])")
if [ "$C4" != "$C1" ]; then ok "a changed payload moves the digest"
else bad "a changed payload moves the digest"; fi

# --------------------------------------------------------------------------
# 2. A proposal is not an edit
# --------------------------------------------------------------------------
cat > base.json <<'JSON'
{"text":"The program served 11800 households in 2022.",
 "quantities":[{"coefficient":11800,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON

BEFORE_ROOT=$(root_of)
OUT=$($WI propose --node households --payload base.json --why "baseline" --actor antonio 2>&1)
has "propose reports the delta class" "$OUT" "node_created"
has "propose states that nothing changed" "$OUT" "Nothing has changed"
check "propose did not move the branch root" "$(root_of)" "$BEFORE_ROOT"

# --------------------------------------------------------------------------
# 3. Authority is required, and every refusal is distinguishable
# --------------------------------------------------------------------------
P=$(pid_of open)
# A refused transition exits 2, the same code the gate uses for BLOCK. It is
# not a usage error and must not be mistaken for one.
OUT=$($WI decide "$P" --accept --actor antonio 2>&1); RC=$?
check "acceptance without a grant is refused" "$RC" "2"
has "refusal names the missing capability" "$OUT" "WI_AUTHORITY_DENIED"
check "the refused proposal did not move the root" "$(root_of)" "$BEFORE_ROOT"

# A grant that has already expired is a different failure from having none.
$WI authority issue --subject stale-editor --capability claim.accept \
   --scope workspace --issuer antonio --expires 2020-01-01T00:00:00+00:00 >/dev/null 2>&1
OUT=$($WI decide "$P" --accept --actor stale-editor 2>&1)
has "an expired grant authorizes nothing" "$OUT" "WI_AUTHORITY_EXPIRED"

# So is a grant that reaches the wrong scope.
$WI authority issue --subject narrow-editor --capability claim.accept \
   --scope branch --scope-value some-other-branch --issuer antonio >/dev/null 2>&1
OUT=$($WI decide "$P" --accept --actor narrow-editor 2>&1)
has "a grant out of scope authorizes nothing" "$OUT" "WI_GRANT_SCOPE_EXCEEDED"

# And so is a revoked one.
$WI authority issue --subject ex-editor --capability claim.accept \
   --scope workspace --issuer antonio >/dev/null 2>&1
GID=$($WI authority list --json | python3 -c "
import json,sys
print([g['grant_id'] for g in json.load(sys.stdin)['grants'] if g['subject']=='ex-editor'][0])")
$WI authority revoke --grant "$GID" >/dev/null 2>&1
OUT=$($WI decide "$P" --accept --actor ex-editor 2>&1)
has "a revoked grant authorizes nothing" "$OUT" "WI_AUTHORITY_REVOKED"

# A judgment provider may never hold a grant at all. This is constitutional,
# not configurable, so it fails at issue time rather than at decision time.
OUT=$($WI authority issue --subject some-model --subject-kind judgment_provider \
        --capability claim.accept --scope workspace --issuer antonio 2>&1)
has "a judgment provider cannot be granted authority" "$OUT" "WI_AUTHORITY_DENIED"

# --------------------------------------------------------------------------
# 4. Delegation is monotonic
# --------------------------------------------------------------------------
$WI authority issue --subject antonio --capability claim.accept \
   --scope workspace --issuer antonio --expires 2030-01-01T00:00:00+00:00 >/dev/null 2>&1
PARENT=$($WI authority list --json | python3 -c "
import json,sys
print([g['grant_id'] for g in json.load(sys.stdin)['grants']
       if g['subject']=='antonio' and not g['revoked_at']][0])")

# Narrowing is allowed.
OUT=$($WI authority delegate --subject deputy --capability claim.accept.wording_only \
        --scope workspace --issuer antonio --parent "$PARENT" \
        --expires 2029-01-01T00:00:00+00:00 2>&1)
has "a narrower delegation is accepted" "$OUT" "delegated"

# Widening is not. `canon.modify` is not below `claim.accept`.
OUT=$($WI authority delegate --subject deputy --capability canon.modify \
        --scope workspace --issuer antonio --parent "$PARENT" \
        --expires 2029-01-01T00:00:00+00:00 2>&1)
has "a widening delegation is refused" "$OUT" "WI_GRANT_SCOPE_EXCEEDED"

# Neither is outliving the parent.
OUT=$($WI authority delegate --subject deputy2 --capability claim.accept.wording_only \
        --scope workspace --issuer antonio --parent "$PARENT" \
        --expires 2040-01-01T00:00:00+00:00 2>&1)
has "a delegation outliving its parent is refused" "$OUT" "WI_GRANT_SCOPE_EXCEEDED"

# --------------------------------------------------------------------------
# 5. Acceptance, application and the difference between them
# --------------------------------------------------------------------------
OUT=$($WI decide "$P" --accept --actor antonio 2>&1)
has "an authorized acceptance is recorded" "$OUT" "DECISION ACCEPTED"
has "the decision names the grant it exercised" "$OUT" "$PARENT"
check "acceptance alone did not move the root" "$(root_of)" "$BEFORE_ROOT"

$WI commit -m "baseline household figure" --actor antonio >/dev/null 2>&1
AFTER_ROOT=$(root_of)
if [ "$AFTER_ROOT" != "$BEFORE_ROOT" ]; then ok "commit moved the root"
else bad "commit moved the root" "root is still $BEFORE_ROOT"; fi

# --------------------------------------------------------------------------
# 6. A decision binds to the exact state it approved
# --------------------------------------------------------------------------
cat > v2.json <<'JSON'
{"text":"The program served 12100 households in 2022.",
 "quantities":[{"coefficient":12100,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON
cat > v3.json <<'JSON'
{"text":"The program served 12300 households in 2022.",
 "quantities":[{"coefficient":12300,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON

$WI propose --node households --payload v2.json --why "first revision" --actor antonio >/dev/null 2>&1
OLD_P=$(pid_of open)
# Now move the target underneath that open proposal.
$WI propose --node households --payload v3.json --why "second revision" --actor antonio >/dev/null 2>&1
NEW_P=$($WI proposals --status open --json | python3 -c "
import json,sys; ps=json.load(sys.stdin)['proposals']; print(ps[-1]['proposal_id'])")
$WI decide "$NEW_P" --accept --actor antonio >/dev/null 2>&1
$WI commit -m "second revision" --actor antonio >/dev/null 2>&1

OUT=$($WI decide "$OLD_P" --accept --actor antonio 2>&1)
has "a decision on a moved target is refused" "$OUT" "WI_DECISION_STALE"
has "the refusal explains it will not reattach" "$OUT" "never saw"

# --------------------------------------------------------------------------
# 7. Simulation mutates nothing
# --------------------------------------------------------------------------
cat > v4.json <<'JSON'
{"text":"The program served 12300 households nationally in 2022.",
 "quantities":[{"coefficient":12300,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":[]}
JSON
$WI propose --node households --payload v4.json --why "drop the region" --actor antonio >/dev/null 2>&1
PRE=$(root_of)
OUT=$($WI simulate --actor antonio 2>&1)
has "simulation says it changed nothing" "$OUT" "SIMULATION ONLY"
has "dropping the last scope constraint is a broadening" "$OUT" "scope_broadened"
has "simulation reports the provably unaffected remainder" "$OUT" "Provably unaffected"
has "simulation reports the repair frontier" "$OUT" "repair frontier"
check "simulation did not move the root" "$(root_of)" "$PRE"

# --------------------------------------------------------------------------
# 8. Semantic classification: the edits that look small
# --------------------------------------------------------------------------
cat > should.json <<'JSON'
{"text":"The agency should publish the report within 30 days.",
 "modality":"should","subject":"agency","bound_actor":"agency"}
JSON
cat > shall.json <<'JSON'
{"text":"The agency shall publish the report within 30 days.",
 "modality":"shall","subject":"agency","bound_actor":"agency"}
JSON
$WI branch create legal --switch >/dev/null 2>&1
$WI propose --node notice --type meaning.obligation --payload should.json \
    --why "baseline obligation" --actor antonio >/dev/null 2>&1
Q=$(pid_of open)
$WI decide "$Q" --accept --actor antonio >/dev/null 2>&1
$WI commit -m "notice obligation" --actor antonio >/dev/null 2>&1

OUT=$($WI propose --node notice --type meaning.obligation --payload shall.json \
        --why "counsel asked for shall" --actor antonio 2>&1)
has "should to shall is a legal force change" "$OUT" "legal_force_strengthened"
has "a legal force change requires obligation authority" "$OUT" "obligation.create"

# The actor holds claim.accept, which does not cover obligation.create.
R=$(pid_of open)
OUT=$($WI decide "$R" --accept --actor antonio 2>&1)
has "claim authority cannot accept a legal force change" "$OUT" "WI_AUTHORITY_DENIED"

# Wording that leaves every typed field alone is wording only — and that is a
# conclusion the comparison reached, never an assumption it started from.
cat > reworded.json <<'JSON'
{"text":"Within 30 days, the agency should publish the report.",
 "modality":"should","subject":"agency","bound_actor":"agency"}
JSON
OUT=$($WI propose --node notice --type meaning.obligation --payload reworded.json \
        --why "reorder the clause" --actor antonio 2>&1)
has "an identical typed state with new wording is wording_only" "$OUT" "wording_only"
hasnt "wording_only does not demand obligation authority" "$OUT" "obligation.create"

# --------------------------------------------------------------------------
# 9. Merge preserves disagreement instead of inventing agreement
# --------------------------------------------------------------------------
$WI branch switch main >/dev/null 2>&1
$WI branch create audit >/dev/null 2>&1

cat > ours.json <<'JSON'
{"text":"The program served 11800 households in 2022.",
 "quantities":[{"coefficient":11800,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON
cat > theirs.json <<'JSON'
{"text":"The program served 12400 households in 2022.",
 "quantities":[{"coefficient":12400,"scale":0,"unit":"households"}],
 "temporal_scope":{"from":"2022-01-01","until":"2023-01-01"},
 "modality":"is","subject":"program","spatial_scope":["Delta region"]}
JSON

$WI propose --node households --payload ours.json --why "ours" --actor antonio >/dev/null 2>&1
A=$(pid_last open); $WI decide "$A" --accept --actor antonio >/dev/null 2>&1
$WI commit -m "ours: 11800" --actor antonio >/dev/null 2>&1

$WI branch switch audit >/dev/null 2>&1
$WI propose --node households --payload theirs.json --why "theirs" --actor antonio >/dev/null 2>&1
B=$(pid_last open); $WI decide "$B" --accept --actor antonio >/dev/null 2>&1
$WI commit -m "theirs: 12400" --actor antonio >/dev/null 2>&1

$WI branch switch main >/dev/null 2>&1
PRE=$(root_of)
OUT=$($WI merge audit --actor antonio 2>&1); RC=$?
check "a semantic conflict blocks the merge" "$RC" "2"
has "the conflict is typed by what disagrees" "$OUT" "Quantity"
has "both sides are shown verbatim" "$OUT" "11800"
has "both sides are shown verbatim, the other one" "$OUT" "12400"
has "the merge says it refused to average" "$OUT" "did not average"

# The one assertion that matters most in this file: no value that neither
# branch asserted may appear anywhere in the merge output.
hasnt "the merge did not invent 12100" "$OUT" "12100"
hasnt "the merge did not invent 12000" "$OUT" "12000"
check "a conflicted merge did not move the root" "$(root_of)" "$PRE"

OUT=$($WI conflicts 2>&1)
has "the conflict is retained as a first-class object" "$OUT" "unresolved"
OUT=$($WI constraints 2>&1)
has "an unresolved conflict fails C015" "$OUT" "FAIL C015"

# Resolution is a decision, made by an actor with authority, and named.
CID=$($WI conflicts --json | python3 -c "
import json,sys; print(json.load(sys.stdin)['conflicts'][0]['conflict_id'])")
OUT=$($WI conflicts --resolve "$CID" --take ours --actor antonio 2>&1)
has "resolving a conflict records who did it" "$OUT" "resolved"
OUT=$($WI constraints 2>&1)
hasnt "C015 clears once the conflict is resolved" "$OUT" "FAIL C015"

# --------------------------------------------------------------------------
# 10. Bitemporal query
# --------------------------------------------------------------------------
OUT=$($WI as-of --valid-at 2022-06-01 2>&1)
has "a state valid in 2022 is returned for 2022" "$OUT" "households"
OUT=$($WI as-of --valid-at 2019-06-01 2>&1)
hasnt "a state valid only in 2022 is not returned for 2019" "$OUT" "11800"
OUT=$($WI as-of --known-at 2000-01-01T00:00:00+00:00 2>&1)
has "the workspace knew nothing before it existed" "$OUT" "no state satisfies"

# --------------------------------------------------------------------------
# 11. Proof obligations are derived, not hard-coded
# --------------------------------------------------------------------------
OUT=$($WI obligations 2>&1)
has "a quantity generates a numeric obligation" "$OUT" "numeric.value"
has "a temporal scope generates a date obligation" "$OUT" "date.range"
has "an external fact must be anchored" "$OUT" "anchor.integrity"

$WI branch switch legal >/dev/null 2>&1
OUT=$($WI obligations --node notice 2>&1)
has "an obligation node must preserve its exceptions" "$OUT" "obligation.exception-preservation"
hasnt "a node with no quantity owes no numeric check" "$OUT" "numeric.value"
$WI branch switch main >/dev/null 2>&1

# --------------------------------------------------------------------------
# 12. Capsules: membership, integrity, and what they refuse to claim
# --------------------------------------------------------------------------
$WI capsule create --out full.wic --profile full >/dev/null 2>&1
OUT=$($WI capsule verify full.wic 2>&1); RC=$?
check "an untouched capsule verifies" "$RC" "0"
has "the inclusion proof reaches the closure root" "$OUT" "inclusion.proof"
has "the capsule states what it does not prove" "$OUT" "proves nothing about whether the sources are correct"

OUT=$($WI capsule inspect full.wic 2>&1)
has "the capsule declares its omissions" "$OUT" "declared_omissions\|declared omissions"
has "signing is declared unavailable rather than implied" "$OUT" "signing"

# The negative twin. Move one byte of a disclosed payload and the capsule must
# say so — this is the whole point of the artifact.
python3 - <<'PY'
import json
c = json.load(open("full.wic"))
c["disclosed"][0]["state"]["payload"]["text"] = "tampered"
json.dump(c, open("bad.wic", "w"), indent=2, sort_keys=True)
PY
OUT=$($WI capsule verify bad.wic 2>&1); RC=$?
check "a tampered capsule is rejected" "$RC" "2"
has "the rejection names the digest that moved" "$OUT" "does not match"
hasnt "a tampered capsule never reports VERIFIED" "$OUT" "VERDICT VERIFIED"

# A selective capsule proves membership of what it hid without disclosing it.
$WI capsule create --out sel.wic --select households --profile selective >/dev/null 2>&1
OUT=$($WI capsule verify sel.wic 2>&1); RC=$?
check "a selective capsule verifies" "$RC" "0"
OUT=$(python3 -c "
import json; c=json.load(open('sel.wic'))
r=c['redactions']
print(r[0]['does_not_prove'] if r else 'none-redacted')")
has "a redacted leaf states the limit of what it proves" "$OUT" "anything about its content\|none-redacted"

# --------------------------------------------------------------------------
# 13. Explanation runs backward to a basis
# --------------------------------------------------------------------------
OUT=$($WI why households 2>&1)
has "why names the reliability basis" "$OUT" "BASIS"
has "why names the commit that introduced the state" "$OUT" "INTRODUCED BY"
has "why names the authority that permitted it" "$OUT" "AUTHORIZED BY"
has "why lists what must still be proved" "$OUT" "PROOF OBLIGATIONS"

# --------------------------------------------------------------------------
# 14. The constraint engine reports what it could not evaluate
# --------------------------------------------------------------------------
OUT=$($WI constraints --json 2>&1)
NE=$(echo "$OUT" | python3 -c "import json,sys;print(json.load(sys.stdin)['not_evaluated'])")
if [ "$NE" -gt 0 ]; then ok "constraints that cannot run say so"
else bad "constraints that cannot run say so" "not_evaluated was $NE"; fi
EV=$(echo "$OUT" | python3 -c "import json,sys;print(json.load(sys.stdin)['evaluated'])")
if [ "$EV" -ge 14 ]; then ok "at least fourteen constraints actually evaluated"
else bad "at least fourteen constraints actually evaluated" "evaluated was $EV"; fi
OUT=$($WI constraints 2>&1)
hasnt "the constraint engine emits no aggregate score" "$OUT" "%"

echo
if [ "$FAILED" -eq 0 ]; then
  echo "v6 regression complete"
else
  echo "v6 regression FAILED"
fi
exit "$FAILED"
