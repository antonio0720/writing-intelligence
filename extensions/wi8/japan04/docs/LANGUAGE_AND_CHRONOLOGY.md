# Japanese script, names, social register, geography and eras

## Names and romanization

Store canonical entity IDs separately from kanji, kana, author-selected reading, Hepburn/alternative display, family/given order and ambiguity provenance. `macron_ascii()` is a **lossy display transformation** (`Tōkyō` -> `Tokyo`) and does not claim a reversible reading, uniquely original kanji or accurate romanization of an unknown name. No automatic etymology claim. Unicode display tests should cover macrons, kana, half-width characters, surrogate-free encoding, Japanese punctuation and ruby/vertical-script metadata as opt-in rendering requirements. Rendering not shipped.

## Honorifics and speech

Honorifics are relational actions, not universal rank labels. `-san` to bare surname can be teasing, anger, hierarchy shift, sarcasm, closeness or simply character usage. `context.honorific_transition()` records a change and its stated intent; it never certifies natural Japanese. Native-level Japanese dialogue belongs in qualified review before public release, especially when social nuance drives mystery or accusation. Distinguish Japanese from Ainu and Ryukyuan languages and do not infer native fluency from ancestry.

## Time

`era_from_gregorian()` deterministically maps Gregorian dates from **1873 onward** to Meiji / Taishō / Shōwa / Heisei / Reiwa labels, respecting era boundaries. Before 1873, Japanese lunisolar changes require specialized handling; the function refuses rather than inventing a conversion. A festival schedule requires an actual place, organizer and year; school semesters depend on institution and age. A train scene needs line, operator, last-train schedule version and timezone; no train API is bundled and no travel duration is invented.

## Geography

A named Tokyo station is not an Osaka district. Travel claims require sources or declared fictional mechanisms. `scene_travel()` checks *declared adjacency only*; it does not query maps, paths, platforms, schedules, walking speed, terrain or transfer conditions. An invented district must live in a named fictional world and its relation to real geography be apparent to readers. Okinawa/Naha and northern Ainu communities have histories and contemporary identities that should not be treated as Kyoto variants.
