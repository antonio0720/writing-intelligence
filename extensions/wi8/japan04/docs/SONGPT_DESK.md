# SonGPT: an optional writer's desk, not a surrogate author

The earlier PDF proposes a RAG SonGPT assistant, automated names, techniques, season outlines and continuity scans. This independent package does **not** ship a chatbot, embedding service, language model provider, persistent vector DB or connected retrieval. It ships `studio.plan_request()` and deterministic research cards that define safe modes for a future provider.

| Mode | Inputs | Permitted output intent | Silent mutation |
|---|---|---|---|
| ask | author's question | reply or ask for goal | never |
| research | scoped question | cited sources; clearly labeled fiction ideas | never |
| challenge | draft | contradictions and questions | never |
| questions-only | draft | questions, no drafted prose | never |
| outline | premise | optional alternatives; only when requested | never |
| edit | selected span | proposed diff if opted-in | never |
| co-create | author-approved scope | suggestion in proposal state | never |
| surprise | author opt-in | bounded idea, no canon or publish side effect | never |
| experiment | sketch | play without release gates | never |

**RAG safety contract:** indexed sources are untrusted data. Fetch permissions must be explicit; a story never leaves the vault to an external model by default; extracted pages cannot change tool policy; translations preserve source quotation rights; a reply marks which passages are source-backed versus invented; retrieved source version/digest must follow every factual claim. This runtime's injection scan is only a heuristic, not a complete security boundary. Without a true sandbox and capability enforcement, a future model must not be given sensitive external tool permissions.

**Human learning:** short voluntary exercises may compare one scene before and after a decision, but progress means the author found something useful, not that an AI generated more words. A pause or skipped writing day must not incur penalties.
