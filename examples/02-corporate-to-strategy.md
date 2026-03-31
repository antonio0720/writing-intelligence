# Example 2: Corporate Speak → Strategy Memo

**Transformation**: Buzzword-laden corporate prose → Actionable strategy with numbers and owners
**Passes used**: Full pipeline
**Voice**: sovereign commander
**Genre**: strategy
**Score delta**: 28 → 93

---

## Before (Score: 28/100)

We are excited to announce that our organization is embarking on a transformative journey to strategically realign our operational priorities. By leveraging our core competencies and fostering a culture of innovation, we aim to unlock significant value for all stakeholders.

Moving forward, it will be critical to ensure that our strategic priorities are properly communicated and that all team members are aligned on our shared vision for growth and excellence. We believe that by optimizing our go-to-market strategy and strengthening our competitive positioning, we can drive meaningful results across all business units.

Our leadership team is committed to empowering our people to deliver best-in-class solutions that meet the evolving needs of our customers. Together, we can navigate the challenges ahead and emerge stronger than ever.

### Violations Found
- Hard-ban phrases: "transformative journey," "leveraging core competencies," "unlock value," "stakeholders," "moving forward," "best-in-class," "navigate"
- Zero numbers anywhere
- No owners named
- No timelines
- No specific actions
- No risk acknowledged
- Could describe any company doing anything

---

## After (Score: 93/100)

**Situation**: Revenue is flat at $8.4M ARR for three consecutive quarters. Net revenue retention dropped from 108% to 94% since January. Two of our ten largest accounts — Meridian Health ($380K ARR) and Cortex Labs ($290K ARR) — are in active procurement review with competitors.

**Complication**: Our product serves the mid-market buyer who signed in 2022. That buyer now has 14 alternatives that didn't exist at signing. We haven't shipped a differentiation feature since the dashboard redesign in September 2024. The engineering team spent Q4 on infrastructure debt that was necessary but invisible to customers.

**Implication**: If we don't ship a visible, differentiation-grade feature by June 30, the two accounts in review will likely churn: $670K ARR. Projecting the current retention curve forward, we lose an additional $1.1M ARR by Q4 from accounts not yet in review but showing declining usage.

**Recommendation**: Ship the API integration layer by June 30. Seven of our ten at-risk accounts have requested this specific feature. Engineering estimates 11 weeks. I'm requesting 8 by reassigning Chen and Rivera from the mobile project, which absorbs a 6-week delay without revenue impact until Q1 2027.

**Risk**: The mobile launch slips from October to December. If the API layer doesn't retain the two accounts in review, we've traded a delay for nothing. Mitigation: both accounts have confirmed in writing that API integration is their primary evaluation criterion.

**Decision required by Friday**: Approve the engineering reassignment. I brief the mobile team Monday.

### What Changed
- Structure: SCIR (Situation → Complication → Implication → Recommendation)
- 11 specific numbers
- 2 named accounts, 2 named engineers
- Timeline with specific dates
- Risk section with mitigation
- Decision point with deadline
- Zero buzzwords. Zero adjectives substituting for data.
- Every sentence either provides data or recommends action

---

*Try it yourself: paste the "Before" text and ask "Rewrite this as a strategy memo using the sovereign commander voice and strategy genre pack."*
