// Pass 6 — Sentence Surgery. Deterministically removes/replaces banned phrases and
// records every transformation. Produces the "clean" asset with hard bans removed.
import { allBans, banRegex, type BanEntry } from "../bannedPhrases";
import type { ProseRewriteLogV3 } from "../../types";

export interface SurgeryResult {
  clean_text: string;
  log: ProseRewriteLogV3;
}

// Passes over the full ban list until no ban matches (a replacement can expose a shorter
// ban). Bounded iterations keep it deterministic and guarantee zero residual hard bans.
const MAX_SWEEPS = 6;

export function runSurgery(taskId: string, text: string): SurgeryResult {
  let working = text;
  const transformations: ProseRewriteLogV3["transformations"] = [];
  let hardCount = 0;
  let softCount = 0;
  let compressions = 0;
  let seq = 0;

  for (let sweep = 0; sweep < MAX_SWEEPS; sweep++) {
    let changedThisSweep = false;
    for (const ban of allBans()) {
      const re = banRegex(ban.phrase);
      const matches = working.match(re);
      if (!matches || matches.length === 0) continue;

      working = working.replace(re, ban.replacement);
      changedThisSweep = true;
      seq++;
      const op = ban.soft ? "soft_ban_removed" : "hard_ban_removed";
      if (ban.soft) softCount += matches.length;
      else hardCount += matches.length;
      if (ban.replacement === "") compressions += matches.length;

      transformations.push({
        transformation_id: `t${seq}`,
        op,
        before: ban.phrase,
        after: ban.replacement === "" ? "[removed]" : ban.replacement,
        rationale: ban.replacement === ""
          ? `Removed AI-slop phrase "${ban.phrase}" (${matches.length}× ).`
          : `Replaced "${ban.phrase}" with "${ban.replacement}" (${matches.length}× ).`,
        rule_id: ban.rule_id,
        voice_impact: ban.soft ? "neutral" : "increased_fidelity",
      });
    }
    if (!changedThisSweep) break;
  }

  const clean_text = tidy(working);

  const log: ProseRewriteLogV3 = {
    task_id: taskId,
    version: "3.0.0",
    transformations,
    summary: {
      total_transformations: transformations.length,
      hard_ban_count: hardCount,
      soft_ban_count: softCount,
      compressions,
      // Fidelity rises as slop is removed; deterministic proxy = hard bans cleared, capped at 1.
      voice_fidelity_delta: Math.min(1, hardCount * 0.05),
    },
  };

  return { clean_text, log };
}

// Deterministic whitespace + punctuation cleanup after phrase removal.
// Ordering matters: strip leading punctuation BEFORE recapitalizing, or the pass is not a
// fixpoint (a leading ", " would block capitalization on the first run but not the second).
function tidy(text: string): string {
  let t = text;
  t = t.replace(/[ \t]+/g, " ");                 // collapse runs of spaces
  t = t.replace(/ +([,.;:!?])/g, "$1");          // no space before punctuation
  t = t.replace(/([,.;:!?]){2,}/g, "$1");         // collapse doubled punctuation
  t = t.replace(/,\s*,/g, ",");                   // collapse stray comma pairs
  t = t.replace(/^\s*[,;:]\s*/gm, "");             // drop leading punctuation on each line
  t = t.replace(/([.!?])\s+[,;:]\s*/g, "$1 ");     // drop punctuation stranded after a sentence break
  t = t.replace(/[ \t]+\n/g, "\n").replace(/\n{3,}/g, "\n\n").trim();
  t = t.replace(/(^|[.!?]\s+)([a-z])/g, (_m, pre, ch) => pre + ch.toUpperCase()); // recapitalize sentence starts (last)
  return t;
}

// Exposed for the /score path where no rewrite is emitted but a count is still needed.
export function countBanReplacements(text: string): { hard: number; soft: number } {
  const lower = text.toLowerCase();
  let hard = 0;
  let soft = 0;
  for (const ban of allBans() as BanEntry[]) {
    const re = banRegex(ban.phrase);
    const m = lower.match(re);
    if (m) {
      if (ban.soft) soft += m.length;
      else hard += m.length;
    }
  }
  return { hard, soft };
}
