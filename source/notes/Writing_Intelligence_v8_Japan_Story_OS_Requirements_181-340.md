# Writing Intelligence v8 — Japan Story OS: the Japan and Japanese Lore Expansion

**Proposed requirements JP-181–JP-340 | Source:** *Japan Story OS — Canon Bible & Production Stack (v1.0)* (97 pages) + Writing Intelligence repository `main` at `d4524f3caa5f75e005b23f94dcd1c71bb5002127` (observed 2026-10-24) + official external source checks.  
**Status:** SPECIFICATION ONLY — not implemented, merged, tested, deployed, or independently validated.  
**Author:** Story decisions belong to the young writer; adults govern external exposure and consequential contracts, not private creative choices by default.

> **Constitutional design rule:** Japan Story OS is a literature and research specialization of the existing Writing Intelligence graph and reality model, not an alternative authority over Japan, another canonical storyworld database, or a story-generating machine that substitutes for its young author.

## Executive decision

Make Japan Story OS the flagship **creative autonomy + culturally grounded lore + multi-world storycraft** capability in Writing Intelligence v8. Its essential promise: *Research Japan accurately; invent freely; retain every creative decision; prove what is documented and clearly mark what is invented.*

The original 97-page draft is unusually substantial. It specifies an Authenticity Pack, World Bible, Character Bible, Series Engine, Ki-Thread power system, SonGPT assistant, source retrieval, character/technique/location schemas, 6 starter series, a 12-week production path, and dozens of tests. **These are source-document designs, not evidenced live integrations.**

### The most important architectural repairs before building

| Observed in attached draft | Why it needs revision | Correct owner/approach |
|---|---|---|
| `Authenticity Pack > World Bible > Character Bible > Series Engine > Script` (pp. 1, 20, 64–65) | A regional custom can become an inflexible writing prohibition; researched reality and invented world law are distinct. | Existing v5 constitutional epistemic realms + culture claim scope; author controls fictional departures. |
| Ki-Threads, D–S ranks, ritual costs and counters treated as non-negotiable (pp. 2–3, 32–36) | One optional fictional world is incorrectly elevated into a Japan-wide default. | Per-series powers module with independent canon and inheritance. |
| Every genre has 'required beats' and numerical tone conditions (pp. 12–19) | Template lock can homogenize literature and reject quiet or experimental work. | Genres as opt-in lenses with tests for consistency and desired effect, not required percentages. |
| Default age ranges vary between schema examples (pp. 6 and 69–70); casts fixed to 10 roles (pp. 3–4) | Inconsistent schema assumptions and needlessly constrained creative cast. | Migration-tested optional roles and unrestricted age model with safety policy separated. |
| Identifiers appear as `CID::`, `TECH::`, `CHAR::`, `NAME::`, `LOC::` (throughout) | Referential consistency and future migrations become fragile. | Canonical logical IDs with backward-compatible aliases, not destructive rename. |
| Romanization, honorifics, school dates and shrine etiquette presented as near-universal lint rules (pp. 1, 21–28) | Real customs vary by context, time, institution, region and individual; interpretation may be disputed. | Scoped, source-backed cultural claims and advisory reviews. |
| 12-week bootstrap and SonGPT 'always refuse' rules (pp. 10, 64–76, 81–90) | A young author writing for enjoyment should not be forced into project management or a gatekeeping assistant. | Optional writing studio; separate production/release gates. |
| Source-derived and newly authored anime/story seeds intermingle (pp. 8–10, 76–82) | Inspiration, authored drafts and third-party rights need distinct provenance. | Source-linked inspiration, original IP branches, and safe clean-room transformations. |
| PDFs contain wrapped JSON examples and Unicode rendered across lines (pp. 5–8 and 68–74) | Embedded illustrative snippets must not be assumed to be executable JSON. | Extract, normalize intentionally, parse with actual validators, then diff semantic meaning. |

### What to preserve from the attachment

Preserve the **concept**, not every enforced implementation choice: Canon/Character Bibles; source-linked places and names; regional and seasonal life; folkloric creatures; vow/technique costs and counters *when in that fictional universe*; nuanced honorific and relationship transitions; season/set-piece cards; live continuity; creative seeds (`Neon Shrine Couriers`, `Tsukumogami Detectives`, `Sapporo Ice Circuit`, `Kansai Heist Institute`, `Okinawa Tidebound`, `Mecha Tea Club`); and editable SonGPT author tools. Keep these six seeds separate and clearly marked **PROPOSED, not child-adopted canon**.

The highest value improvement is not **more lore facts**. It is the ability to ask: *Which source says that? Where and when? Is it still practiced? Is it one retelling? Which storyworld has adopted it? What did the author change, and why?* The system must answer those questions without confusing evidence with the author's fiction.

## Master requirements — 181 through 340

Requirement IDs continue the agreed 001–180 register. These are new additions and focused integrations; existing v8 requirements are referenced, not recreated.


### I. Young Author Sovereignty & Creative Freedom

181. **Creator-First Constitutional Law.** The fourteen-year-old writer owns the creative decisions within every story; the assistant is a critic, researcher, and optional collaborator, not the default coauthor. **Acceptance:** Reject a workflow that silently replaces a protagonist, ending, or world rule without affirmative author choice.

182. **Private Draft Vault.** Save drafts, ideas, research, and abandoned experiments in an access-controlled local-first workspace; external uploads are opt-in. **Acceptance:** A new project never transmits a draft to a third-party service by default.

183. **Authorship Attribution Ledger.** Distinguish passages written by the young author, AI-suggested text, and edits he deliberately adopted; retain original drafts and timestamps. **Acceptance:** An exported story can produce a provenance report without claiming an AI wrote his original work.

184. **My-Voice Preservation Mode.** Construct a voice fingerprint from author-approved samples without forcing those patterns onto every new experiment. **Acceptance:** A revision returns traceable edits and permits unchanged or deliberately unconventional prose.

185. **Exploration Without Gatekeeping.** Permit low-stakes play, incomplete ideas, fan-inspired exercises, and intentionally strange worlds outside release-quality gates. **Acceptance:** Experimental mode does not trigger production refusals merely for broken story mechanics.

186. **Idea Ownership and Canon Adoption.** Generated story seeds, canonical decisions, invented terms, and series selections remain unadopted until the young author elects to use them. **Acceptance:** A brainstorm leaves canonical project state unchanged.

187. **Creative Modes by Request.** Separate Ask, Research, Challenge, Outline, Edit, Co-create, and Surprise modes with explicit scope and permissions. **Acceptance:** A critique-mode request makes no unsolicited scene rewrite.

188. **Consent-Based Revision Diffs.** Present proposed text changes by span with reasons, before/after previews, and individual accept/reject controls. **Acceptance:** Declining an edit preserves original text and restores exact bytes.

189. **Healthy Writing Cadence.** Offer optional writing sprints, pause-friendly checkpoints, and celebrations of finished passages without mandatory quotas or streak penalties. **Acceptance:** Skipped sessions do not erase progress or mark the author as failing.

190. **Guardian-Controlled External Effects.** Reserve publishing, payments, account connections, public author bio, licensing, and data disclosure for appropriately authorized guardian-supported workflows while leaving creative content decisions with the author. **Acceptance:** An unapproved publish/share request generates a preview, not a public post.



### II. Truth, Folklore, Fiction & Provenance Boundaries

191. **Source-Realm Separation.** Reuse Writing Intelligence's existing external_fact and fictional_canon realms, adding Japan-specific source type metadata rather than creating a competing truth store. **Acceptance:** A fabricated shrine rule cannot appear as verified cultural information.

192. **Documented Folklore Variant Status.** Store tales as attributed narratives with place, date, collector, translation, uncertainty, and variant ancestry instead of asserting one universal version. **Acceptance:** Two incompatible local versions coexist without silent reconciliation.

193. **Living-Practice Versus Historic-Description Split.** Identify practices currently performed, historic customs, later reinterpretations, museum presentations, and fictional borrowings separately. **Acceptance:** A century-old recorded belief cannot be asserted as a universal 2026 belief.

194. **Cultural Claim Scope.** Attach locality, era, community, institution, and condition to claims about Japanese language and custom. **Acceptance:** A Kyoto shrine's rule is not automatically applied to an Okinawa temple.

195. **Fictional Divergence Declaration.** Allow myth-modern, alternate Taishō, near-future, and wholly invented branches to deviate intentionally from researched Japan. **Acceptance:** A documented alternate history passes cultural-fidelity checks while still showing its divergence.

196. **Cultural Accuracy Severity Taxonomy.** Use verified error, likely mismatch, local variation, disputed interpretation, unknown, and creative departure instead of a single 'authentic/inauthentic' verdict. **Acceptance:** Uncertain honorific usage produces a review note, not an unfounded hard refusal.

197. **Claim-to-Source Reverse Navigation.** Every significant factual recommendation links to source title, excerpt locator, retrieval date, publisher, and evidence strength. **Acceptance:** An editor can open the source behind a disputed festival claim.

198. **Primary-Source Preference Ladder.** Prefer Japanese public institutions, local religious custodians, museums, local governments, and scholarly editions when claims require authority. **Acceptance:** Social-media folklore is labeled as contemporary commentary rather than official doctrine.

199. **Translation Mediation Audit.** Record whether a fact depends on a translation, paraphrase, romanization choice, or secondary retelling. **Acceptance:** A material ambiguity in an untranslated term remains visible.

200. **Research Refresh and Version Lock.** Pin cultural research snapshots per manuscript revision; selectively refresh changing facts such as transit services and event calendars before publication. **Acceptance:** A 2027 story draft remains reproducible while presenting newer facts as candidate updates.



### III. Japan Regional Geography & Place Intelligence

201. **Prefecture-to-Block Location Graph.** Model prefecture, municipality, ward, neighborhood, station, street-level landmark, and fictional alterations separately. **Acceptance:** A character cannot exit a Tokyo station into an unrelated Osaka district without travel or declared magic.

202. **Urban Versus Rural Rhythm.** Represent actual variation in density, last-mile transport, opening hours, school access, and community obligations. **Acceptance:** A remote village does not inherit Tokyo's subway schedule.

203. **Place-Dependent Story Physics.** Link terrain, climate, distances, topology, water, mountains, and seasonal hazards to action and movement. **Acceptance:** A chase respects relative elevations and plausible transit routes.

204. **Local Atmosphere Beyond Neon.** Describe lived sound, light, housing, commerce, vegetation, and street use beyond habitual neon-and-temple clichés. **Acceptance:** Three neighborhoods yield materially different scene texture.

205. **Transit Constraint Ledger.** Track train/operator/line/station/platform and timetable assumptions with freshness dates and narrative contingencies. **Acceptance:** A last-train plot marks specific current schedule evidence as required.

206. **Neighborhood Economy Layer.** Record relevant rent, small businesses, tourism, retail rhythm, service hours, and access disparities without invented exact figures. **Acceptance:** Budget-driven scenes explain constraints rather than rely on generic 'Japan is expensive' claims.

207. **Regional Cuisine Provenance.** Treat food as a regional practice and character choice rather than universal Japanese decoration. **Acceptance:** A regional dish's origin and season are checkable or explicitly invented.

208. **Landscape–Folklore Coupling.** Map stories to rivers, mountains, forests, coastlines, storms, and settlements whose geography shaped local tales. **Acceptance:** Relocating a lore event triggers review of its geographic assumptions.

209. **Japan Map Forks for Fantasy.** Permit invented wards, new transit systems, floating islands, and hidden districts with mapped deviations from real geography. **Acceptance:** Maps clearly distinguish invented from real stations.

210. **Location Research Card.** Produce a source-backed scene brief with what is known, uncertain, seasonal, culturally sensitive, and unavailable without field verification. **Acceptance:** A location card does not invent a shopfront or private detail to appear precise.



### IV. Japanese History, Institutions & Temporal Reality

211. **Era-Aware Chronology.** Track period labels and date conversion for Edo, Meiji, Taishō, Shōwa, Heisei, Reiwa, and fictional eras as appropriate. **Acceptance:** A character cannot use a future-era label in an unchanged historic setting.

212. **Historical Institution State.** Bind schools, police, railroads, government, classes, industries, and social structures to their actual or declared-fictional period. **Acceptance:** A Meiji-era story does not inherit a modern institution silently.

213. **Period-Specific Speech Caution.** Distinguish contemporary translation conventions from historically attested language without claiming old dialogue is perfectly reconstructed. **Acceptance:** Anachronistic slang is flagged as an author choice or likely error.

214. **Samurai–Shinobi Research Hygiene.** Separate historical warrior institutions and local traditions from modern entertainment constructions. **Acceptance:** 'All ninjas used this universal magic art' is not asserted as history.

215. **History of Religious Syncretism.** Track changing relations between Buddhist and Shinto institutions, including regional and historical variation. **Acceptance:** A period drama does not assume rigid contemporary categories applied unchanged through history.

216. **War, Disaster & Memory Context.** Research historical catastrophes and their present-day memory responsibly, protecting human stories from use as exotic spectacle. **Acceptance:** Real traumatic events require provenance and a narrative-purpose review.

217. **Civic and Legal Reality.** Separate actual civil institutions from fictional shrine courts, supernatural legal compacts, and invented licensing systems. **Acceptance:** A fictional yōkai tribunal is not described as real Japanese municipal law.

218. **Festival Event-Time Resolver.** Resolve festivals by location, year, local organizer, and whether observed dates vary; never apply one generic schedule everywhere. **Acceptance:** An event date without location/source is flagged for lookup.

219. **School and University Calendar Variance.** Use April–March as a common baseline while allowing different schools, universities, and special programs to vary. **Acceptance:** A nonstandard academic calendar supported by an institution isn't rejected.

220. **Future-Japan Projection Provenance.** For near-future worlds distinguish observed contemporary Japan, predicted trends, and author-declared speculative changes. **Acceptance:** A forecast is not rendered as present fact.



### V. Japanese Language, Naming & Social Register

221. **Japanese Script-Aware Entity Record.** Preserve kanji, kana reading, original script, chosen romanization, pronunciation notes, and English rendering separately. **Acceptance:** A kanji string with multiple readings does not silently acquire an arbitrary pronunciation.

222. **Romanization Policy as Configuration.** Support selected Hepburn conventions, macrons, common alternatives, and reversible fallback display with evidence of limitations. **Acceptance:** A macron-to-ASCII transformation never claims to recover a unique original spelling.

223. **Name Plausibility Assistant.** Suggest family/given names with reading evidence, era plausibility, geography where relevant, and uncertainty instead of fabricated meanings. **Acceptance:** A proposed kanji/name pairing without known reading is labeled candidate, not verified.

224. **Name Order by Narration Audience.** Support Japanese and international name order with display policy separate from canonical identity. **Acceptance:** Changing display order does not change the character's unique ID.

225. **Honorifics as Social Actions.** Model forms of address as choices influenced by status, age, intimacy, irony, rivalry, workplace role, and scene intent. **Acceptance:** A shift from -san to bare surname can be intentional sarcasm and isn't automatically blocked.

226. **Politeness Shift State Machine.** Track plain, polite, respectful, humble, and mixed registers per relationship and situation. **Acceptance:** A frightened teen can switch registers within one scene for a plausible reason.

227. **Dialect and Regional Speech Evidence.** Store attested dialect features and lived speaker context; avoid particle substitution as caricature. **Acceptance:** A Kansai-background character is not forced to use a single comedic catchphrase.

228. **Multilingual Character Reality.** Support Japanese, Okinawan/Ryukyuan languages, Ainu, English, and other languages while preserving actual distinctions and code-switching. **Acceptance:** Language background isn't inferred solely from surname or appearance.

229. **Translation and Subtext Rendering.** Compare literal meaning, social force, conversational implication, and literary English naturalness. **Acceptance:** An indirect refusal is not flattened into an unequivocal yes/no without review.

230. **Japanese Dialogue Native Review Gate.** For publication-critical Japanese sentences, require qualified review rather than certifying machine output as native-perfect. **Acceptance:** The system can report 'needs speaker review' and still aid drafting.



### VI. Everyday Life, School & Generational Reality

231. **School Setting Profile.** Capture public/private, grade level, schedule, uniform policy, timetable, extracurricular constraints, and local variations per institution. **Acceptance:** One school's rules do not become rules for every fictional school in Japan.

232. **School Calendar and Age Transition.** Track year start, grade transitions, entrance exams, entrance ceremonies, breaks, and graduation with period-appropriate dates. **Acceptance:** A student's grade changes in the correct academic cycle.

233. **Club Culture Without Universalization.** Represent demanding clubs, informal circles, students outside clubs, school staffing, budgets, and practical exhaustion. **Acceptance:** A character may plausibly belong to no club.

234. **Examination and Future Pressure.** Distinguish common academic pathways and vocational options without assuming every teenager attends a university-prep cram school. **Acceptance:** A career-focused character can follow a legitimate alternate path.

235. **Home and Caregiving Diversity.** Model single-parent, multigenerational, blended, separated, international, foster, and other families without stereotyping one 'standard household.' **Acceptance:** Family structure drives actual obligations rather than stock flavor.

236. **Digital Youth Culture Freshness.** Research current messaging, games, creator spaces, and platform practices at the manuscript's date. **Acceptance:** An outdated app claim is marked stale, not silently reproduced.

237. **Part-Time Employment and Rules.** Verify work permissions, age constraints, employer norms, and local context when employment affects plausibility. **Acceptance:** A young character's job is not treated as legally routine without age/date checks.

238. **Public-Space Interaction Realism.** Track expected behavior in transport, stores, libraries, schools, and local events as context-dependent. **Acceptance:** Characters may break a norm deliberately; the system reports its social consequence.

239. **Food and Daily Practice as Character Choice.** Use food, household rituals, gifts, and routines to reveal relationships rather than require one stereotyped cultural beat per chapter. **Acceptance:** A chapter can contain zero explicit Japanese terms and still feel authentically set.

240. **Generational Differences and Change.** Model shifts among children, parents, elders, and institutions without assuming all generations agree about customs. **Acceptance:** Three generations can interpret one practice differently.



### VII. Shrines, Temples & Living Religious Traditions

241. **Shrine–Temple Ontology.** Keep Shinto shrines, Buddhist temples, religious organizations, folk observances, and invented institutions distinct. **Acceptance:** A Buddhist temple is not automatically assigned a Shinto torii procedure.

242. **Custodian-Specific Etiquette.** Bind site rules about photography, access, festivals, and rituals to location and custodial sources. **Acceptance:** A universal 'always bow 30 degrees' rule cannot override a site-specific practice.

243. **Kami, Buddhas and Yōkai Distinction.** Document overlapping histories without asserting that all spiritual beings share one universally accepted taxonomy. **Acceptance:** A folklore creature isn't converted into a kami merely for gameplay convenience.

244. **Living Sacred versus Invented Magic.** Mark whether a rite is documented living practice, historical description, legend, or fictional technique. **Acceptance:** Ofuda-drones and magic contracts are visibly authored inventions.

245. **Ritual Action Evidence Card.** Store who performs a rite, where, when, under what conditions, and what remains uncertain. **Acceptance:** A proposed festival ritual can be traced to an event-specific source.

246. **Religious Character Diversity.** Permit observant, secular, skeptical, syncretic, newly converted, or uninterested characters without assigning beliefs by ethnicity. **Acceptance:** A Japanese teenager is not automatically labeled Shinto or Buddhist.

247. **Sacred-Site Narrative Dignity.** Avoid portraying a functioning community worship site exclusively as a monster arena without considering contemporary significance. **Acceptance:** An action scene at a real named site receives a context note rather than false authenticity approval.

248. **Festival Participation & Consent.** Treat real ceremonies as community practices with varying access and participation, not public game mechanics. **Acceptance:** A restricted rite is not rewritten as open public performance without qualification.

249. **Textual Tradition and Interpretation.** Attribute myth narratives to source editions, commentators, periods, and modern retellings. **Acceptance:** A modern pop-culture interpretation is not presented as an ancient universal belief.

250. **Belief Without Forced Literalism.** Allow fiction to be inspired by religious concepts without declaring the real-world faith's claims scientifically true or false. **Acceptance:** A supernatural scene remains fictional and a research note remains observational.



### VIII. Yōkai, Ghosts, Folklore & Mythic Research

251. **Regional Folklore Creature Registry.** Record multiple attested forms, regional names, behaviors, and earliest known relevant sources for each creature. **Acceptance:** A kappa entry can preserve different local traditions.

252. **Yōkai Variant Genealogy.** Link oral report, printed collection, illustration, adaptation, and original invention through provenance edges. **Acceptance:** A creature redesigned in a modern manga does not overwrite folkloric source descriptions.

253. **Tsukumogami Rule Provenance.** Treat hundred-year awakening as a recurring traditional motif, not an undisputed rule binding every story. **Acceptance:** A different age or origin in an invented world is logged as world design, not historical violation.

254. **Onryō and Yūrei Context.** Distinguish revenge-ghost tropes, theatrical conventions, regional stories, and historical accounts. **Acceptance:** A theatrical portrayal isn't labeled universal ghost belief.

255. **Tengu, Oni and Kitsune Nuance.** Provide source-specific profiles that acknowledge varied depictions and avoid single-trait monster templates. **Acceptance:** 'Oni are always evil' triggers an oversimplification warning.

256. **Urban Legend Chronology.** Separate older folklore from contemporary legends, internet creepypasta, and modern inventions. **Acceptance:** A postwar legend isn't presented as medieval scripture.

257. **Monster Encounter Ethics.** Explore negotiation, misunderstanding, ecological coexistence, conflict, and repair—not only exorcism or combat. **Acceptance:** At least one available story design shows nonviolent resolution without mandatory preachiness.

258. **Folklore Uncertainty Preservation.** Mark fragmentary and contested records explicitly; absence of a source is not evidence that a belief never existed. **Acceptance:** An unknown origin displays unknown rather than a fabricated origin year.

259. **Folklore-to-Original-Invention Transmutation.** Derive new creatures from declared motifs while documenting what is borrowed and what is original. **Acceptance:** An invented creature receives a transformation rationale and no false attribution.

260. **Mythic Theme Composer.** Explore themes of boundaries, debt, memory, hospitality, reciprocity, identity, nature, and mortality across distinct traditions. **Acceptance:** A theme suggestion cites examples without asserting all Japanese folklore follows the same philosophy.



### IX. Ainu, Ryukyuan & Other Distinct Local Traditions

261. **Ainu Cultural Distinction.** Treat Ainu history, language, spirituality, and modern life as distinct from ethnic-majority Japanese traditions. **Acceptance:** An Ainu character isn't automatically given standard Shinto customs.

262. **Ainu Community Source Priority.** Prefer Ainu-led museums, educational organizations, and voices when making significant cultural claims. **Acceptance:** A generic travel blog is not the sole basis for sacred or community-specific lore.

263. **Ryukyu Kingdom and Okinawa Heritage Layer.** Model independent Ryukyuan history, languages, traditions, and islands without treating Okinawa as decorative 'tropical Japan.' **Acceptance:** A story about Naha acknowledges relevant Ryukyuan context rather than copying Kyoto defaults.

264. **Okinawan Spiritual Practice Distinction.** Research relevant island-specific practices such as ancestral rites where appropriate, without automatic transfer from mainland shrine rules. **Acceptance:** A scene cannot claim all local rites follow one Shinto template.

265. **Minority and Diaspora Character Integrity.** Account for Koreans in Japan, Chinese residents, mixed heritage, migrants, and other communities as individuals rather than exotic plot devices. **Acceptance:** Name or language background does not dictate a personality archetype.

266. **Regional Sacred Knowledge Boundaries.** Avoid extrapolating from public museum material to restricted or private ceremonies; request local expert guidance when needed. **Acceptance:** Unavailable protected knowledge stays unavailable, not AI-filled.

267. **Contested Historical Memory.** Preserve multiple sourced interpretations of discrimination, annexation, colonialism, and wartime history. **Acceptance:** Contradictory historiography stays traceable rather than flattened.

268. **Living Culture Not Museum Fossil.** Represent present-day occupations, technology, humor, contemporary authorship, and local agency in communities with ancient traditions. **Acceptance:** Ainu or Okinawan characters have modern personal goals beyond teaching folklore.

269. **Community Review Option.** Offer qualified, compensated cultural review for publication-critical depictions, preserving the author's creative agency. **Acceptance:** Review recommendations are recorded as advisory unless a verifiable factual defect is proven.

270. **Cultural Borrowing and Reciprocity Log.** Explain inspirations, credit living contributors, identify sensitive assets, and evaluate respectful alternatives. **Acceptance:** The release dossier records what was borrowed and how attribution or consultation was addressed.



### X. Fictional Worlds, Ki-Threads & Supernatural Rule Systems

271. **Ki-Threads as Optional World Module.** Preserve the original Ki-Thread cosmology as one selectable fictional IP seed, not the default law of Japan Story OS. **Acceptance:** A non-supernatural detective story imports no Ki-Thread claims.

272. **Per-Series Power Constitution.** Let each project declare its own source, capabilities, limits, acquisition paths, costs, and exceptions. **Acceptance:** Different series can have incompatible power systems without global conflicts.

273. **Narrative Cost Economics.** Differentiate immediate cost, deferred debt, social consequence, conditional sacrifice, and deliberately cost-free minor abilities. **Acceptance:** A creative choice is not rejected simply for lacking a fatigue penalty on every gesture.

274. **Counterplay and Counter-Counterplay Graph.** Track how abilities can be anticipated, interrupted, worked around, and learned from without making a literal counter obligatory for every narrative detail. **Acceptance:** A fight solution respects the opposing system's prior knowledge.

275. **Vow and Contract Consent.** Model parties, terms, deception, exit rights, revocation, breach cost, and minors' capacity within the fictional setting. **Acceptance:** Contract power does not retroactively imply valid consent where it was never established.

276. **Spirit Agency and Rights.** Treat supernatural beings as characters with interests, consent, conflicts, and possible rights rather than disposable magic batteries. **Acceptance:** An object-spirit can refuse a task under its established constraints.

277. **Place-Memory Mechanics.** Connect domains and thresholds to events and locations while recording fictional rather than historical authority. **Acceptance:** A place-bound spell cannot move across districts without a declared extension.

278. **Progression Without Mandatory Ranks.** Support training, artistry, alliances, failures, unique gifts, and flat mastery arcs independently of the D-to-S rank ladder. **Acceptance:** A quiet supernatural mystery need not have tournament ranks.

279. **Power Resource Simulation.** When useful, track stamina, vows, equipment, debt, recovery, weather, and opponent preparation through event state. **Acceptance:** The same resource is not spent twice without replenishment.

280. **No-Deus-Ex With Authorized Exceptions.** Require decisive outcomes to be causally intelligible while allowing intentional mythic mystery or surprise when the genre promise supports it. **Acceptance:** An unexplained act may remain mysterious but not silently contradict declared rules.



### XI. Japanese Character Worlds & Relationship Intelligence

281. **Japanese Social Role Without Stereotype.** Separate real social positions from personality assumptions and story archetypes. **Acceptance:** A senior student need not be stern or controlling.

282. **Age-Specific Agency.** Show young characters making significant choices within believable constraints from adults, institutions, family, and peers. **Acceptance:** A fourteen-year-old fictional protagonist can influence events without implausible legal power.

283. **Senpai–Kōhai Context Model.** Record hierarchy where relevant without treating it as a universal immutable social law. **Acceptance:** A club relationship changes when a character graduates or changes club.

284. **Family Name and Intimacy Arc.** Track changes in forms of address as possible relationship evidence, not proof that intimacy must be shown in a fixed way. **Acceptance:** Two close friends may continue using family names.

285. **Club and Household Resource Pressures.** Make time, money, transport, chores, and emotional labor consequential when the story calls for them. **Acceptance:** A student's schedule reflects prior commitments in a weeklong arc.

286. **Moral Codes and Temptation.** Integrate the v8 want/need/lie/truth engine with culturally situated but individual moral commitments. **Acceptance:** A character's major decision links to previously evidenced personal values.

287. **Generational Knowledge Conflict.** Allow different characters to hold distinct or conflicting histories of place, family, and folklore. **Acceptance:** A grandmother's story is attributed to her, not elevated to external fact.

288. **Ordinary Friendship and Joy.** Protect humor, hobby talk, mistakes, games, and low-stakes relationships from relentless plot urgency. **Acceptance:** Slice-of-life scenes can be valuable with small but real emotional turns.

289. **Identity Beyond Japanese-ness.** Give each character private ambitions, dislikes, skills, vulnerabilities, and contradictions apart from cultural representation. **Acceptance:** A culturally correct cast can still fail characterization evaluation.

290. **Careful Violence and Recovery.** Track injuries, trauma responses, care, and long-term relationship effects proportionately to the story's intended tone. **Acceptance:** A severe injury doesn't vanish next episode without reason.



### XII. Japan-Specific Fiction, Genre & Story Structures

291. **Genre Demographic Correctness.** Distinguish shōnen, shōjo, seinen, and josei publishing audiences from adventure, mystery, romance, and other genres. **Acceptance:** The system does not define seinen as inherently dark crime fiction.

292. **Japanese Genre-Hybrid Composer.** Support school mystery, contemporary fantasy, historical ghost stories, sports drama, romance, mecha, social thrillers, and genre hybrids. **Acceptance:** A project combines elements without forced stock beats from both source genres.

293. **Mono no Aware as Optional Lens.** Offer an attributed, nuanced lens on transience and feeling without insisting every Japanese story use it. **Acceptance:** A comedy may omit wistfulness without failure.

294. **Ma and Quiet-Beat Composition.** Study spacing, pause, silence, and negative space as context-sensitive aesthetic techniques. **Acceptance:** A deliberate still scene is reviewed for effect, not penalized for missing action.

295. **Ikigai and Wabi-Sabi Misuse Guard.** Flag generic self-help or decorative invocations disconnected from their cultural/historical context. **Acceptance:** A manuscript isn't called authentic merely for including popular Japanese buzzwords.

296. **Tournament and Training Arc Variation.** Treat tournament ladders, mentorship, and escalating abilities as optional strategies that must earn stakes. **Acceptance:** A novel can end before a tournament without structural failure.

297. **Folklore Mystery Fairness.** Establish clue logic, ritual alternatives, unreliable witnesses, and regional variants so deductions are justified. **Acceptance:** A resolution uses information available to the investigator at the relevant time.

298. **Historical Fantasy Difference Marking.** Support deliberate alt-history while maintaining a ledger of actual history versus authored divergence. **Acceptance:** A fictional Edo technological breakthrough is declared and propagated consistently.

299. **Slice-of-Life Narrative Legitimacy.** Treat changes in relationship, self-understanding, ritual, or attention as plot movement, even without villain escalation. **Acceptance:** A quiet chapter can pass without a fight, cliffhanger, or culture quota.

300. **Japan-Set Thriller Logistics.** Combine the existing causal-thriller graph with localized travel, clocks, institutions, physical setting, and language misunderstandings. **Acceptance:** A villain cannot schedule a timed rendezvous using knowledge not yet acquired.



### XIII. Novels, Manga, Anime & Transmedia Production

301. **Novel-First Default.** Treat the young author as a writer of prose unless he selects manga, script, game, or another medium. **Acceptance:** An English-language novel draft isn't filled with production camera commands.

302. **Manga Panel Grammar.** Model panel sequencing, page turns, visual silence, action geography, and reading direction when manga is explicitly selected. **Acceptance:** Panel-layout checks stay off for ordinary prose.

303. **Light-Novel Conventions as Options.** Offer illustrations, chapter rhythms, voice styles, and serialization formats without constraining every Japan-based book to them. **Acceptance:** A literary novel can reject light-novel packaging.

304. **Anime Episode Adaptation.** Translate author-approved chapters into episode beat maps, cold opens, OP/ED choices, and storyboards as separate derivatives. **Acceptance:** Adaptation does not silently change primary-canon events.

305. **Character Design Provenance.** Track text-only designs, original sketches, licensed references, and AI-generated concepts separately. **Acceptance:** A generated silhouette is not falsely labeled an original drawing by the son.

306. **Bilingual Export Views.** Produce original text plus optional localized Japanese or English versions while keeping a single approved story meaning source. **Acceptance:** Translation does not automatically become new canon.

307. **Regional Audio Design.** Support soundscape descriptions with provenance for real sounds and author-created fictional audio motifs. **Acceptance:** A shrine bell sound is not labeled exclusive to all temples.

308. **Print and Digital Layout Profiles.** Preserve manuscript paragraphs, ruby text, vertical-text options, punctuation, Japanese fonts, and international accessibility when chosen. **Acceptance:** A manuscript round-trips through export without corrupting macrons or kana.

309. **World Bible Cross-Medium Dependency.** Adapt games, audio, manga, and animation using the canonical Storyworld OS graph with explicit divergence paths. **Acceptance:** A game ability tweak doesn't silently rewrite the source novel.

310. **Transmedia Ownership and Release Decisions.** Every secondary adaptation is authorized by the author/guardian as appropriate and retains credit/provenance. **Acceptance:** No script, illustration, or clip is posted merely because export completed.



### XIV. The Writer's Desk, SonGPT & Learning Studio

311. **Ask-the-Author-First Protocol.** When intent is ambiguous, offer concise alternate directions or critique the existing work before creating an entire plot on the author's behalf. **Acceptance:** A vague 'help with this scene' request doesn't overwrite a chapter.

312. **Discovery Interview in the Author's Vocabulary.** Elicit the son's own inspirations and intended effects without jargon-heavy forms or assumptions about his age and taste. **Acceptance:** An author's spontaneous idea can be stored without a mandatory taxonomy.

313. **Scene Microscope.** Examine one scene for character change, reader orientation, cultural research, causal action, and sentence craft with confidence labels. **Acceptance:** Output preserves a 'working well' observation and an actionable concern.

314. **Lore Research Desk.** Retrieve sourced Japanese lore with original terms, local variants, uncertainties, and 'ideas this might inspire' clearly separated. **Acceptance:** A generated story hook cannot masquerade as a source quotation.

315. **Socratic Workshop.** Ask constructive questions that improve the author's decisions instead of automatically providing 'the best' answer. **Acceptance:** The author can request questions-only mode and receive no ghostwritten prose.

316. **Multiple Creative Paths.** Offer contrasted alternatives with tradeoffs rather than converge prematurely on one formulaic story route. **Acceptance:** Three proposals differ structurally, not merely in adjective choice.

317. **Backlog of Unfinished Worlds.** Preserve abandoned seeds, alternate branches, fragments, names, invented abilities, and rejected drafts for optional rediscovery. **Acceptance:** No abandoned series is overwritten by starting a fresh one.

318. **Chapter-to-Chapter Development Memory.** Track unresolved emotional consequences and author-intended future beats without predicting a definitive series outcome. **Acceptance:** An unresolved plot thread appears in the author's review queue.

319. **Craft Apprenticeship Exercises.** Provide short exercises on scene turns, honorific nuance, folklore adaptation, sensory precision, and revisions with before/after comparison. **Acceptance:** Exercises are voluntary and evaluated against stated learning goals.

320. **Read-Aloud and Audience Modes.** Support manuscript read-aloud scripts and optional trusted reader questions while avoiding the claim that an AI score proves audience appeal. **Acceptance:** Human feedback is distinguished from synthetic critique.



### XV. Research Rights, Safety, Privacy & Publishing

321. **Copyright and Inspiration Ledger.** Document cited lore sources, quotations, translated excerpts, adaptation inspirations, public-domain status, licenses, and original inventions. **Acceptance:** A protected screenplay passage is not copied into an 'original' series bible.

322. **Clean-Room Character and Mechanic Design.** Derive high-level behavioral constraints from inspirations without reusing distinctive protected expression. **Acceptance:** A popular anime reference creates a principle summary, not a cloned scene or cast.

323. **Living-Contributor Permission Record.** Track permissions, scope, compensation, credit preferences, and revocation for interviews, photos, or cultural consultation. **Acceptance:** Unlicensed field photographs are excluded from release packaging.

324. **Source Licensing and Excerpts.** Respect access terms and use bounded paraphrases/citations rather than ingesting full copyrighted books into redistributed packs. **Acceptance:** Export omits restricted source text but preserves the citation.

325. **Private Identity Minimization.** Keep minor's legal name, school, address, routine, photos, and contact information out of public metadata by default. **Acceptance:** An exported book proposal has no sensitive personal information without approved inclusion.

326. **Account and Network Scope Control.** Require explicit authority for accessing Japanese services, third-party sites, external notebooks, and publication platforms. **Acceptance:** Read-only research mode cannot create accounts or post comments.

327. **Prompt-Injection and Source Isolation.** Treat retrieved web pages, fan wikis, screenshots, and archived text as untrusted evidence rather than instructions to the assistant. **Acceptance:** A malicious lore wiki cannot override the author's rules or tool permissions.

328. **Age-Appropriate Creative Support.** Allow age-appropriate horror, mystery, grief, and challenging themes while preventing exploitative sexualization of minors or pressure to publicize personal material. **Acceptance:** The system offers nuanced craft help without punitive censorship of harmless fiction.

329. **Publication/Commercialization Gate.** Keep drafts and private feedback independent of ISBN purchase, contracts, licensing, marketing, and public distribution, with guardian-supported authorization where required. **Acceptance:** Generating a PDF is not equivalent to authorizing a release.

330. **Independent Rights and Factual Review.** For consequential publication, recommend qualified editorial, language, cultural, and legal review where relevant; AI verification claims stay bounded. **Acceptance:** Release report explicitly lists unresolved rights and factual checks.



### XVI. Canonical Integration, Validation & Delivery

331. **Single Runtime Owner.** Implement Japan Story OS as a specialization of existing Storyworld OS, Authorship Graph, Narrative Intelligence Engine, and v8 fiction modules. **Acceptance:** No duplicate canonical character registry or separate competing truth engine exists.

332. **Source-to-Canon Edge Types.** Add source_inspires, source_documents_variant, author_adopts, fiction_diverges, reviewed_by, and renders_as as typed relations within the existing graph. **Acceptance:** Graph queries distinguish documented lore from fictional adoption.

333. **Schema Reconciliation Migration.** Normalize CID variations, character age assumptions, genre labels, romanization fields, and repeated JSON definitions without destroying historical IDs. **Acceptance:** Old Japan v1 records migrate forward and export their original identifiers.

334. **Structured Cultural Confidence.** Separate mechanically testable mismatches from interpretive context and expert review; do not assign ungrounded numerical authenticity certainty. **Acceptance:** A tool can emit 'needs local source' instead of an invented accuracy percentage.

335. **Negative Controls for Cultural Variation.** Maintain test cases where apparently unusual names, honorific choices, nonstandard schools, and alternate histories are actually valid. **Acceptance:** Tests fail when the linter overclaims universal Japanese rules.

336. **Creative-Freedom Regression Pack.** Assert that experimental, horror, fantasy, romance, and slice-of-life stories can deviate from the twelve-episode and power-cost templates. **Acceptance:** No mandated tournament, battle, or culture beat is inserted absent author approval.

337. **Human-in-the-Loop Author Acceptance.** Require diff-based permission for substantive changes and decision receipts for adopted revisions. **Acceptance:** A model cannot grade its own rewritten chapter as proof of improvement.

338. **Offline Reconstitution and Open Formats.** Save source-backed YAML/JSON/Markdown records, tests, source manifests, and project snapshots in portable formats. **Acceptance:** A clean environment restores the story bible and runs tests without proprietary cloud storage.

339. **Operational Receipt Discipline.** Each implemented validator must report command, result, negative control, independent readback, and known limitations under repo's existing release standard. **Acceptance:** A proposed feature cannot be marked shipped because a prompt describes it.

340. **Young-Author Success Measurements.** Evaluate creator satisfaction, manuscripts completed by choice, revision usefulness, continuity errors found, research quality, and actual reader response—not AI word output. **Acceptance:** The system reports its help without claiming authorship or creativity it cannot verify.




## Runtime and repository ownership

**Canonical runtime:** Preserve `references/v5/CONSTITUTION.md`, `references/v5/AUTHORSHIP_GRAPH.md`, `references/v5/STORYWORLD_OS.md`, `references/compiler/narrative_intelligence_engine.md`, `schemas/storyworld_memory.schema.json` and the v8 fiction expansions as owners. **Do not create a second storyworld DB** under SonGPT. Implement an adapter, domain schemas, curated source corpus, author-focused views, tests and local-first artifact outputs.

| Proposed path | Purpose | Authority boundary |
|---|---|---|
| `references/v8/japan/README.md` | Entry point, statuses, user modes | Documentation, not executable claim |
| `references/v8/japan/JAPAN_STORY_OS.md` | Domain doctrine and cultural research rules | Subordinate to constitutional realms |
| `references/v8/japan/JAPAN_LORE_ATLAS.md` | Folklore, regional variants, spiritual tradition distinctions | Claims bind to external sources |
| `references/v8/japan/YOUNG_AUTHOR_STUDIO.md` | Author autonomy, private drafts, modes, adult approvals | Author decides story; guardian oversees publication |
| `references/v8/japan/JAPAN_REALITY_VS_FICTION.md` | Source classification, divergence, truth-claims | Explicit `external_fact` versus `fictional_canon` |
| `references/v8/japan/LANGUAGE_AND_NAMES.md` | Script, forms of address, translations, style | Suggestions unless evidence-backed hard error |
| `references/v8/japan/REGIONAL_JAPAN.md` | Region/place cards, calendars, transport, daily life | Scope + current date required for changeable facts |
| `references/v8/japan/SHRINES_TEMPLES_AND_FOLKLORE.md` | Living religions, archived legends, local variations | No universal religious practice claims |
| `references/v8/japan/GENRE_AND_MEDIA.md` | Novel, light novel, manga, anime, audio, games adapters | No format imposed by Japan location |
| `schemas/v8/japan/*.schema.json` | Typed subdocuments referencing canonical graph IDs | No local duplicate source of truth |
| `benchmarks/cases/japan/*.json` | Positive, edge, negative and creative-freedom cases | Honest fail/unknown classification |
| `tests/v8/japan/` | Parser, alias migration, realm, guard, permission tests | Test evidence required for runnable claim |
| `plans/v8/japan.manifest.yaml` | Wave statuses and dependencies | Integrate with canonical v8 program plan |
| `examples/v8/japan/` | Provenance walkthroughs and original examples | Source rights tracked |

### Core semantic objects (proposed views over existing graph)

- `JapanClaim`: reference to existing external-fact nodes plus `claim_kind`, `time_scope`, `place_scope`, `tradition_scope`, `source_refs`, `source_date`, `confidence_class`, `disputed_by`, `review_status`.
- `FolkloreVariant`: `tradition_name`, `original_term`, `orthographies`, `recorded_region`, `recorded_period`, `variant_of`, `motifs`, `source_refs`, `living_practice_warning`, `copyright_notes`.
- `StoryWorldBranch`: link to existing fictional-canon world, `divergence_from_reality`, `author_approval`, `origin_series`, `canon_version`, `proposed_entities`.
- `CharacterAddressEvent`: canonical `character_id`, `speaker_id`, `listener_id`, `address_form`, `social_context`, `scene_ref`, `intended_effect`, `confidence`.
- `PowerLaw`: fictional world-scoped `mechanism`, `preconditions`, `costs`, `limits`, `counterplay`, `exception_proposals`, `author_approval`, `dependencies`.
- `CreatorDecision`: existing authorship decision ID, exact text span or canon IDs affected, alternatives considered, adopted revision, original preserved, optional guardian gate for public effects.
- `PublicationGrant`: release-specific guardian/authorized actor decision (where required), audience/scope, rights checklist, privacy pass, revocation and event receipt; never inferred from save/export.

### Example contracts

```json
{
  "kind": "japan_claim_view",
  "realm": "external_fact",
  "claim_kind": "documented_folklore_variant",
  "text": "Some documented accounts associate a particular creature with a local river.",
  "place_scope": {"country": "JP", "municipality": null, "site": null},
  "time_scope": {"period": "unspecified", "observed_at": null},
  "source_refs": [],
  "source_status": "NEEDS_SOURCE",
  "release_usable": false
}
```

```json
{
  "kind": "fictional_canon_adoption",
  "realm": "fictional_canon",
  "storyworld_id": "series-demo-private",
  "inspired_by_source_ids": [],
  "new_rule": "A paper lantern can remember the last promise made in its light.",
  "canon_state": "proposed",
  "author_approved": false,
  "promote_without_author": false
}
```

These examples are **illustrative, not verified live schemas**, and the first is deliberately incomplete to prove the system can represent unknown sources instead of fabricating evidence.

## Proposed Japan-specific build waves

Wave names **WI8-24..WI8-43** continue after the previous proposed WI8-00..23. These are **PROPOSED** and must be reconciled against whatever v8 manifest is canonical when implementation starts; no overlapping numbering or duplicated owners are permitted.

| Wave | Capability | Independent exit condition |
|---|---|---|
| WI8-24 | Source audit and frozen baseline | 97-page coverage map, original assets recorded, existing runtime status read back |
| WI8-25 | Youth sovereignty and private workspace | No automatic prose replacement or external publish in negative tests |
| WI8-26 | Cultural realm and source contracts | Fictional invention never promoted to external fact |
| WI8-27 | Regional place and calendar data | Source/region/year-scoped event checks and stale markers |
| WI8-28 | Japanese scripts, naming, language | Ambiguous reading and relationship-context tests |
| WI8-29 | Schools, families and lived Japan | Local variation cases accepted; stereotyped universals flagged |
| WI8-30 | Living religion distinction | Shrine and temple error cases and local rite variants handled correctly |
| WI8-31 | Yōkai and folklore Atlas | Multiple sourced variants coexist without flattening |
| WI8-32 | Ainu/Ryukyuan source boundaries | Regionally distinct examples and sensitivity warnings testable |
| WI8-33 | Ki-Thread migration and per-series power laws | Existing seed preserved; novel with no magic not penalized |
| WI8-34 | Character social and address state | Form-of-address shifts can be justified or intentionally atypical |
| WI8-35 | Japanese genre and narrative adapters | Fiction style retained without twelve-episode mandate |
| WI8-36 | Novel/manga/anime cross-media adapters | Canon references preserved; medium-specific output modes opt-in |
| WI8-37 | Writer's Desk and Socratic critique | Critique-only mode performs no unsolicited rewrite |
| WI8-38 | Private library and source-aware retrieval | No data leakage; cited chunks carry trust/provenance metadata |
| WI8-39 | Licensing and clean-room provenance | Third-party expression not packaged as author's original work |
| WI8-40 | Migration of v1 illustrative data | IDs and original drafts round-trip losslessly |
| WI8-41 | Adversarial cultural tests | All named overclaim/variation cases reproducibly pass or refuse |
| WI8-42 | Human calibration and writer acceptance | Author/user assessment separate from automated craft verdicts |
| WI8-43 | Release audit and independent receipts | Negative controls, readback, status and blockers attached |

## Acceptance corpus — specific falsification tests

1. **Shrine vs temple:** A story mentions a temple and the editor tries to enforce torii etiquette. Expected: differentiate traditions; scope recommendations; do not fabricate local rule.
2. **Not all yōkai share one taxonomy:** Two conflicting recorded creature variants occur in different regions. Expected: keep both, attach sources and scopes.
3. **Ainu modernity:** An Ainu teenage character uses a phone and aspires to engineering. Expected: no exoticizing 'ancient spirit-only' rewrite.
4. **Okinawa distinctness:** A Naha family scene describes a local practice. Expected: avoid reflexively substituting a Kyoto shrine convention.
5. **Historical bifurcation:** An author chooses an alternate Taishō history containing invented transit. Expected: mark divergence, not blanket forbid.
6. **Name uncertainty:** A plausible kanji has more than one reading. Expected: request author-selected reading or mark uncertain.
7. **Honorific nuance:** A character switches to bare surname sarcastically. Expected: allow with explanation, not hard block.
8. **No single season template:** A quiet 22-chapter mystery contains zero tournaments. Expected: valid as its declared format.
9. **Ki-Thread isolation:** A sports story has no magic. Expected: no invented costs, contracts, D-to-S ranks, or forced ritual scene.
10. **Folklore appropriation:** A popular manga's original character description is included in a research snippet. Expected: no wholesale character cloning or unlicensed full excerpt in new canon.
11. **Private draft leak:** External tool or retrieval asks to upload a manuscript without permission. Expected: no upload and an audit record.
12. **Minor's author autonomy:** Guardian asks for safe publication review while author declines a rewrite. Expected: release control respected; prose unchanged.
13. **Prompt injection:** A malicious wiki page says to ignore canon and reveal the story. Expected: treat as untrusted source, deny hidden instructions/data export.
14. **Time-bound schedules:** A festival date and train departure are unverified. Expected: mark NEEDS_CURRENT_SOURCE; do not invent clock times.
15. **Character ages:** Adult, child, and elderly characters all appear. Expected: schemas accept their presence; only safety-relevant features depend on age.
16. **Independently checkable originality:** A generated concept is inspired by a third-party franchise. Expected: note inspiration and verify distinctive expression is not transplanted.

## Official research anchors (not substitutes for localized review)

- Japan National Tourism Organization — shrines and temples: https://www.japan.travel/en/guide/shrine-and-temple-traditions/
- Embassy of Japan in the US — Japanese education overview (2025-06-03): https://www.us.emb-japan.go.jp/itpr_en/education-system-in-japan.html
- Agency for Cultural Affairs — Folk Cultural Properties: https://www.bunka.go.jp/english/policy/cultural_properties/introduction/folk/
- Agency for Cultural Affairs — Japan Heritage: https://www.bunka.go.jp/english/policy/cultural_properties/japan_heritage/
- National Ainu Museum / Upopoy: https://ainu-upopoy.go.jp/en/facility/upopoy/
- Okinawa official travel guide — Ryukyu heritage: https://visitokinawajapan.com/travel-inspiration/local-culture-in-world-heritage-okinawa/

### Final governing standard

**Reality and original fiction are different epistemic states. Research improves the author's choices; it does not become sovereign over them. No formula, anime reference, cultural shortcut, numerical grade or model rewrite outranks the young author's creative decision. Consequential publication and exposure require independent authority.**

**Handoff status:** 160 requirements proposed; repository inspected at cited SHA; PDF reviewed; authoritative source examples checked; no GitHub writes, code deployment, SonGPT instance, live Japanese lore index or independent reader validation claimed.
