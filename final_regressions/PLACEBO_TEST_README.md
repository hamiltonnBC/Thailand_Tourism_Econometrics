# Spatial Placebo Tests - Instructions

## What This Tests

The spatial placebo test validates whether Thailand's asymmetric recovery is truly **Thailand-specific** or if it's a broader regional/random phenomenon.

## How It Works

1. **Run Model C** (Thailand Asymmetry) with Thailand's interaction term
2. **Re-run Model C** for each other country, replacing Thailand with that country
3. **Compare results**: If only Thailand shows a significant effect, it confirms Thailand is unique

## Expected Results

### ✅ Ideal Outcome:
- **Thailand**: Significant (p < 0.05) ← This is what we found in Model C
- **All other countries**: Not significant (p > 0.10)

This would prove Thailand's effect is unique, not random.

### ⚠️ Concerning Outcome:
- **Multiple countries**: Significant (p < 0.05)

This would suggest the pattern is regional or systematic, not Thailand-specific.

## Running the Test

```bash
cd final_regressions
python spatial_placebo_tests.py
```

## Output Files

1. **spatial_placebo_results.csv** - Table with all coefficients, p-values, t-stats
2. **spatial_placebo_tests.png** - Visualization showing all countries with confidence intervals

## Updating the Dashboard

After running the script, update `src/pages/Model.tsx` in the Diagnostic Tests section:

Replace the "TBD" values with actual results from `spatial_placebo_results.csv`:

```typescript
{
  country: 'Vietnam',
  coefficient: 0.1234,  // From CSV
  pValue: '0.456',      // From CSV
  tStat: '0.89',        // From CSV
  isSignificant: false  // true if p < 0.05
}
```

## Interpretation Guide

### Color Coding on Dashboard:
- 🔵 **Blue** = Thailand (should be significant)
- 🟢 **Green** = Other countries (should NOT be significant) ← Good!
- 🔴 **Red** = Other countries (ARE significant) ← Problem!

### What Each Result Means:

| Scenario | Interpretation |
|----------|----------------|
| Only Thailand significant | ✅ Strong evidence for Thailand-specific effect |
| Thailand + 1-2 others significant | ⚠️ Investigate those countries - may have similar issues |
| Many countries significant | ❌ Not Thailand-specific - broader pattern |
| No countries significant | ❌ Model specification issue |

## Countries Being Tested

1. **Thailand** 🇹🇭 (baseline - should be significant)
2. **Vietnam** 🇻🇳 (closest competitor)
3. **Malaysia** 🇲🇾 (regional competitor)
4. **Singapore** 🇸🇬 (hub competitor)
5. **Indonesia** 🇮🇩 (regional competitor)
6. **Cambodia** 🇰🇭 (regional competitor)
7. **Japan** 🇯🇵 (developed market)
8. **Australia** 🇦🇺 (distant market)

## Why This Test Matters

Without this test, critics could argue:
- "Maybe you just got lucky with Thailand"
- "Maybe all Southeast Asian countries show this pattern"
- "Maybe it's just random noise"

With this test showing only Thailand is significant:
- ✅ Proves Thailand's effect is real and unique
- ✅ Rules out regional explanations
- ✅ Strengthens causal claims
- ✅ Publication-quality evidence

## Next Steps

1. Run `spatial_placebo_tests.py`
2. Check the results in the CSV and PNG files
3. Update the dashboard with actual values
4. Interpret the findings
5. Add to your paper/presentation
