# Contributing to Writing Intelligence

Writing Intelligence improves when more writers contribute. Here's how.

## What We Accept

**New anti-patterns**: Phrases, structures, or cadence signatures you've identified in AI output that aren't in the current library. Include the pattern, why it flags, and the fix.

**New voiceprints**: Submit 3+ writing samples (500+ words each) from the same author, along with the extracted voice profile following the format in `references/voiceprints/custom_voiceprint_builder.md`.

**New genre packs**: Domain-specific compilation rules for genres not yet covered. Follow the format of existing genre packs in `references/genre_packs/`.

**New discipline primitives**: Reasoning primitives for academic disciplines not in `references/academic/discipline_primitives.md`. Include the primitives, a strong example, and a weak example.

**Before/after examples**: AI-generated input and compiler output pairs demonstrating transformation quality. Include the score delta and which passes were applied.

**Detector benchmark results**: If you run compiler output through Turnitin, GPTZero, Originality.ai, or other detectors, submit the results following the format in `tests/detector_benchmark_suite.md`.

**Bug reports**: Any case where the compiler produces output that still sounds AI-generated, gets flagged by a detector, or loses the author's voice during processing.

## How to Submit

1. Fork the repository
2. Create a branch: `git checkout -b your-contribution`
3. Add your files in the appropriate directory
4. Submit a pull request with a clear description of what you're adding and why

## Standards

- Every reference file must include a table of contents if longer than 100 lines
- Anti-patterns must include: the pattern, detection method, and fix
- Genre packs must include: weighting adjustments, architecture, voice notes, and common failures
- Voiceprints must include: all 8 dimension parameters, sentence/paragraph characteristics, vocabulary profile, and distinctive markers
- Examples must include scoring with rationale

## What We Don't Accept

- Content that promotes academic dishonesty
- Fabricated citations, statistics, or sources
- Discriminatory or harmful content
- Contributions that reduce the quality or specificity of existing files

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions

Open an issue. The community and maintainers will respond.
