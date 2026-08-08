# Deliveries

Finished work that has been shipped somewhere — a landing page, a filing, a
covenant, a brief.

## What a delivery is under v6

Before v6, a delivery was a document that was written and then checked. The
document was the thing; the checking was something that happened to it
afterwards, and the record of that checking lived beside the file rather than
inside it.

v6 inverts that. **The semantic state is canonical and a rendering is a build
from it** — Law M. A delivery in this directory is therefore not the source of
truth for what it says. It is a rendering of governed meaning at a named point,
and the governed meaning is the thing that can be queried, simulated against,
merged, and proved to a stranger.

The practical consequence for anything filed here:

- **A delivery names the state it was built from**, so *what did this say* and
  *what did we believe when we said it* are separate questions with separate
  answers. Time is two clocks, not one.
- **A delivery is not edited in place to correct it.** A correction is a proposal
  against the state, decided by somebody holding a grant, and the delivery is
  rebuilt. Editing the rendering leaves the graph and the file disagreeing, and
  nothing in the toolchain is looking for that.
- **A delivery distinguishes direction from shipped capability.** If it describes
  something that does not run, it says so in its own text, in the place a reader
  will actually be.

The last one is Law C — never report work not done — applied to output rather
than to process.

## Current entries

| File | What it is |
|---|---|
| [`shigosen-intent-commons-covenant.md`](shigosen-intent-commons-covenant.md) | The SHIGOSEN Intent Commons Standard — 26 constitutional commitments for a consent-driven outcome network, with an explicit public-claim boundary separating direction from shipped capability. |

## Adding one

State the arena, the status, the attribution and the state it was built from.
If any part of it describes capability that is specified rather than executable,
the boundary belongs in the delivery itself, not in a note attached to it.

Working examples of the governed sequence that produces a state worth rendering:
[`../examples/v6/README.md`](../examples/v6/README.md).

## Author

Antonio T. Smith Jr. / Density6 LLC
