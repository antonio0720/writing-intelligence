# Compiler Auto-Mode Engine

## Purpose

Automatically configure the 6-pass pipeline based on analysis of the input
text, declared intent, and detected genre. The writer should not need to
manually select voiceprints, genre packs, or pass configurations for
standard tasks. The auto-mode reads the input and assembles the optimal
compilation stack.

---

## Mode Detection Protocol

### Step 1: Intent Classification

Analyze the user's request and classify into one of these modes:

| Mode | Trigger Signals | Pipeline Config |
|---|---|---|
| **Draft** | "write," "draft," "create," "compose" | Full 6-pass, heavy on Pass 0 + Pass 4 |
| **Rewrite** | "rewrite," "improve," "make better," "strengthen" | Pass 1 diagnostic first, then targeted passes |
| **Edit** | "edit," "clean up," "fix," "polish" | Pass 1 + Pass 3 + Pass 4, light touch |
| **Score** | "score," "grade," "audit," "evaluate," "diagnose" | Pass 1 diagnostic → auto-diagnostic report only |
| **Transfer** | "convert," "rewrite as," "turn this into," "make it sound like" | Style transfer engine with full pipeline |
| **Compress** | "shorten," "compress," "make tighter," "cut," "reduce" | Pass 3 surgery + kill_padding operator |
| **Expand** | "expand," "develop," "flesh out," "add detail" | Pass 2 structure + scene grounding + evidence moves |
| **Voice Match** | "make it sound like me," "match my voice," "in my style" | Custom voiceprint builder → Pass 4 restoration |
| **Academic** | "essay," "paper," "thesis," "assignment," "research" | Academic mode full stack + discipline primitives |
| **Longform** | "chapter," "book," "series," "doctrine," "next section" | Memory system + continuity + full pipeline |

### Step 2: Genre Detection

If the user doesn't declare a genre, detect from content signals:

| Signal | Detected Genre |
|---|---|
| Citations, hedging language, methodology terms | Academic |
| Revenue, metrics, recommendations, owners, timelines | Strategy |
| Scene description, dialogue, character action | Fiction |
| "You" address, objections, CTA, guarantee | Sales |
| Scripture, congregation address, testimony | Sermon |
| Slide references, TAM, team, ask | Pitch Deck |
| Statutory references, "shall," "pursuant to" | Legal |
| Dosing, clinical terms, IMRAD structure | Medical |
| Claim language, "comprising," embodiments | Patent |
| BLUF, agency references, fiscal year notation | Government |
| Shot descriptions, sensory density, cut transitions | Cinematic |
| Attribution tags, character speech patterns | Dialogue |
| Subject line, action items, brevity | Email |
| Applause cues, audience address, landing lines | Speech |

### Step 3: Voice Detection

If no voiceprint is declared, analyze the input for:

- Sentence length distribution → match to closest voiceprint
- Vocabulary tier → match formality band
- Emotional temperature → match warmth/coldness
- First-person frequency → match authority posture

If the input has enough text (500+ words), build a provisional custom voiceprint
from the input itself and use that for Pass 4.

### Step 4: Audience Detection

Infer from vocabulary, complexity, and context:

| Signal | Audience |
|---|---|
| Technical jargon without definition | Expert |
| Defined terms, analogies, examples | Mixed/general |
| Short sentences, basic vocabulary | Broad public |
| "Professor," "assignment," course terms | Academic evaluator |
| "Investors," "board," financial metrics | C-suite/investors |
| "Congregation," "brothers and sisters" | Faith community |

---

## Auto-Configuration Output

After detection, the engine assembles a configuration block:

```
AUTO-MODE CONFIGURATION
═══════════════════════════════════════
Mode:           [Draft/Rewrite/Edit/Score/Transfer/...]
Genre:          [detected or declared]
Genre Pack:     [filename]
Voiceprint:     [name or "custom from input"]
Audience:       [detected or declared]
Passes Active:  [0,1,2,3,4,5,6] or subset
Special Modules:
  - [academic mode / memory system / style transfer / etc.]
Detection Risk Target: [LOW required / LOW preferred / acceptable]
═══════════════════════════════════════
```

This configuration is internal. Do not show it to the user unless they ask
"what mode are you using?" or similar.

---

## Mode-Specific Pipeline Configurations

### Draft Mode
```
Pass 0: FULL — declare everything before writing
Pass 1: SKIP — nothing to diagnose yet
Pass 2: FULL — build structure before prose
Pass 3: FULL — apply anti-slop during writing
Pass 4: FULL — voice must be present from the start
Pass 5: FULL — stress-test before delivery
Pass 6: Default to clean output
```

### Rewrite Mode
```
Pass 0: LIGHT — inherit intent from original
Pass 1: FULL — diagnose everything
Pass 2: AS NEEDED — restructure only if architecture is broken
Pass 3: FULL — sentence-level surgery
Pass 4: FULL — voice must survive the rewrite
Pass 5: FULL — verify improvements
Pass 6: Default to clean + violations list
```

### Edit Mode
```
Pass 0: SKIP — intent is preservation
Pass 1: LIGHT — flag only clear violations
Pass 2: SKIP — preserve original structure
Pass 3: TARGETED — fix flagged issues only
Pass 4: LIGHT — restore voice if cleanup flattened it
Pass 5: SKIP — light edit doesn't need full stress-test
Pass 6: Default to clean
```

### Score Mode
```
Pass 0: INFER — detect genre, voice, audience from content
Pass 1: FULL — comprehensive diagnostic
Pass 2-5: SKIP — scoring only, no modification
Pass 6: Auto-diagnostic report format only
```

### Transfer Mode
```
Pass 0: FULL — declare source AND target genre/voice
Pass 1: FULL — diagnose source text
TRANSFER: Run style transfer engine
Pass 2: FULL — rebuild in target architecture
Pass 3: FULL — apply target genre's anti-slop rules
Pass 4: FULL — apply target voiceprint
Pass 5: FULL — verify transfer fidelity
Pass 6: Default to clean + transfer verification notes
```

### Academic Mode
```
Pass 0: FULL — rubric compiler, discipline identification
Pass 1: FULL — with academic-specific checks
Pass 2: FULL — with rubric mapping
Pass 3: FULL — with academic anti-detection rules
Pass 4: FULL — with academic voiceprint
Pass 5: FULL — with professor calibration
Pass 6: Default to clean + citation check + detection risk
```

### Longform Mode
```
PRE-PASS: Load or create Project Memory File
Pass 0: FULL — with continuity checks against PMF
Pass 1: FULL — with cross-section consistency
Pass 2: FULL — section job must serve overall arc
Pass 3: FULL — standard
Pass 4: FULL — voice must match PMF baseline
Pass 5: FULL — with thread tracking
Pass 6: Default to clean
POST-PASS: Update PMF with session results
```

---

## Override Rules

The user can always override auto-detection:
- "Use sovereign commander voice" → lock voiceprint regardless of detection
- "This is a strategy document" → lock genre regardless of detection
- "Skip the stress test" → disable Pass 5
- "Just clean it up, don't restructure" → Edit mode even if Rewrite was detected
- "Score only" → Score mode regardless of other signals

User declarations always override auto-detection.

---

## Fallback

If detection confidence is low (mixed signals, ambiguous input):
- Default to Rewrite mode (safest general-purpose config)
- Default to casual_sharp voiceprint (most versatile)
- Default to no genre pack (apply only universal rules)
- Flag uncertainty in internal config: "LOW CONFIDENCE — may need user clarification"
