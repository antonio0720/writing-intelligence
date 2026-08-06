# Voice and Consent

Voiceprints model how a specific person writes. When that person is real and identifiable, that is a different act from modeling a tone, and it carries obligations that vary by jurisdiction — personality rights are strong across much of Europe and Latin America, and post-mortem publicity rights vary enormously.

Read this before building a voiceprint from samples attributable to a named person.

---

## Five bases, three of them unrestricted

| Subject | Basis needed |
|---|---|
| **The author themselves** | None. Their own writing, their own voice. |
| **A fictional character** | None. No person exists to have rights. |
| **A synthetic voice** built from stated traits, not samples | None. |
| **A team or house voice**, from work the organization owns | The author's statement that the organization owns it. |
| **A named third party** | An explicit statement that the author is authorized. |

For the last row, ask once, plainly, and take the answer: *"Do you have authorization to model this person's voice? I'll note it either way."* Do not interrogate, do not demand documents, and do not refuse the work if the answer is yes. The point is that the question was asked and the answer recorded — which is what protects the author when someone else asks it later.

**Public figures are not an exception.** Quoting a public figure is journalism, and the proof protocol handles it with verbatim spans. Generating new text in their voice is a different act with the same requirement as anyone else.

**Deceased persons vary by jurisdiction.** If it comes up, note the variance once and move on. That is the honest answer.

## Sample provenance

When building from samples, note where each came from: authored by the subject · work-for-hire owned by the organization · licensed · public domain · the author holds the rights.

This matters most in the case that actually recurs: a team voiceprint built partly from an employee who has since left. Whether those samples remain usable depends on whether the work was theirs or the organization's, and that is worth knowing before the profile is in production rather than after.

## What a voiceprint is not

Not an impersonation engine and not a style-transfer model. It is a **measurement profile** — ranges the writing should fall within, patterns to preserve, patterns to avoid. It tells you where text moved away from a baseline. It does not generate text "as" someone.

Keep that distinction visible in how results are presented. "This section is more formal than your usual range" is measurement. "Written in the style of [person]" is something else, and the difference is legible to a court.

## Drift reporting

Lead with passages, never with a percentage:

> Two sections moved away from your usual range.
>
> **Section 3, paragraphs 4–9** — sentences stayed long and uniform where you normally alternate short and long.
> **Closing** — lost the compression you usually end with.
>
> Alignment: 6 of 9 measurable dimensions in range. [what's measured]

The author can act on a passage. They cannot act on 88%.

## Intentional departures

When an author says a shift was deliberate, that governs — for this document. Do not generalize it to their permanent profile without asking. A voice that quietly absorbs every one-off decision stops being a baseline and becomes a running average of accidents.
