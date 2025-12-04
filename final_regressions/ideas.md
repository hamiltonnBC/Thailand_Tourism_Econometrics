Run an event-study (country × year) first to check dynamics and pre-trends.

Fit a heterogeneous post model (country × Post) next — that’s the clean pivot from your failed single-treatment DiD.

Test mechanisms with post × characteristic interactions (RER, peace, visa, flights).

Use synthetic control and leave-one-out/placebo as robustness checks.

For a simple cross-section, compute a recovery_rate and run very small-N inference (bootstraps / permutation tests).

Always run the same battery of diagnostics (pre-trends, VIF, collinearity, cluster SEs, multiple testing).

Below: detailed evaluation, exact model formulas, implementation notes, diagnostics, and how to report.

A. Why your recommendations are correct (but conditional)

The placebo table you showed proves heterogeneity exists. That invalidates a single-treated unit inference as the only approach.

Modeling heterogeneity explicitly is the right response — either by estimating country-specific post effects or by interacting post with country characteristics.

But: 8 countries is small. Adding many parameters (country × post + other interactions) eats degrees of freedom and makes clustered SEs noisy. You must balance ambition with parsimonious specification and heavy robustness checks.

B. Prioritized plan and exact specifications
Step 1 — Event study (required)

Purpose: test parallel trends and show time path, country by country.

Estimate (panel with entity FE):

ln
⁡
(
arrivals
𝑖
𝑡
)
=
𝛼
𝑖
+
∑
𝑡
≠
2019
𝛿
𝑡
,
𝑖
1
{
𝑌
𝑒
𝑎
𝑟
=
𝑡
}
+
𝑋
𝑖
𝑡
𝛽
+
𝜀
𝑖
𝑡
ln(arrivals
it
	​

)=α
i
	​

+
t

=2019
∑
	​

δ
t,i
	​

1{Year=t}+X
it
	​

β+ε
it
	​


Practical implementation:

Replace 
∑
𝑡
≠
2019
𝛿
𝑡
,
𝑖
∑
t

=2019
	​

δ
t,i
	​

 with (Year × Country) interactions only for post period or for a reasonable window (2017–2024) to avoid too many parameters. But ideally show year dummies interacted with Thailand and with a few selected countries.

Plot the 
𝛿
𝑡
,
𝑖
δ
t,i
	​

 coefficients and CIs for each country. Check pre-2020 coefficients for trending. If pre-trends exist, DiD logic fails.

Key diagnostic: Do pre-2020 coefficients look flat (insignificant, near zero)? If not, you need a different identification strategy (no DiD).

Step 2 — Heterogeneous post model (your Option A)

Estimate:

ln
⁡
(
arrivals
𝑖
𝑡
)
=
𝛼
𝑖
+
𝛾
𝑡
+
𝑋
𝑖
𝑡
𝛽
+
∑
𝑗
=
1
𝑁
𝜃
𝑗
(
1
{
𝑖
=
𝑗
}
×
1
{
𝑃
𝑜
𝑠
𝑡
}
)
+
𝜀
𝑖
𝑡
ln(arrivals
it
	​

)=α
i
	​

+γ
t
	​

+X
it
	​

β+
j=1
∑
N
	​

θ
j
	​

(1{i=j}×1{Post})+ε
it
	​


Where:

𝛼
𝑖
α
i
	​

 = country FE

𝛾
𝑡
γ
t
	​

 = year FE (optional; include if you want to control for common shocks)

𝑋
𝑖
𝑡
X
it
	​

 = controls (ln(RER), ln(GDP_China), etc.)

𝜃
𝑗
θ
j
	​

 = country-specific post coefficients (compare 
𝜃
Thailand
θ
Thailand
	​

 to others)

Why: directly estimates each country's post effect. You get a vector of γ’s to compare.

Caveats:

With year FE and country FE you can still identify country×post interactions, but include year FE only if Post is not collinear with year dummies (Post is a multi-year dummy; that's fine).

Degrees of freedom: you add N country×post parameters (here 8). With 136 obs it's OK but SEs will be wide; cluster by country.

Inference:

Test H0: θ_Thailand = 0 (one-sided >0 if you expect stronger recovery).

Also test pairwise contrasts: θ_Thailand − θ_Vietnam = 0 to compare directly.

Multiple testing:

You will get many θ_j; control FDR (Benjamini-Hochberg) or report Bonferroni-adjusted p-values for multiple country comparisons.

Step 3 — Mechanism tests (your Option B)

Estimate:

ln
⁡
(
arrivals
𝑖
𝑡
)
=
𝛼
𝑖
+
𝛾
𝑡
+
𝑋
𝑖
𝑡
𝛽
+
𝜙
 
𝑃
𝑜
𝑠
𝑡
𝑡
+
𝜓
1
(
𝑃
𝑜
𝑠
𝑡
𝑡
×
Peace
𝑖
𝑡
)
+
𝜓
2
(
𝑃
𝑜
𝑠
𝑡
𝑡
×
ln
⁡
𝑅
𝐸
𝑅
𝑖
𝑡
)
+
…
+
𝜀
𝑖
𝑡
ln(arrivals
it
	​

)=α
i
	​

+γ
t
	​

+X
it
	​

β+ϕPost
t
	​

+ψ
1
	​

(Post
t
	​

×Peace
it
	​

)+ψ
2
	​

(Post
t
	​

×lnRER
it
	​

)+…+ε
it
	​


Interpretation:

𝜓
1
ψ
1
	​

 positive means countries whose peace index increased (or is higher) during post period recovered faster.

This reduces reliance on country dummies as cause and provides interpretable mechanisms.

Caveat: interactions consume variation. Keep the set small and theory-driven: peace, visa_dummy, flights_capacity (if available).

Step 4 — Synthetic control for Thailand (robustness)

Construct synthetic Thailand from other countries using pre-2020 data.

Check pre-fit; if synthetic closely tracks real Thailand pre-2020, credible. If not, method fails.

Run placebo synthetic controls: pretend each donor country is treated and compare gaps to get p-values.

Caveat: With only 7 donors synthetic control is fragile. Do it as a robustness check, not the main result.

Step 5 — Cross-sectional recovery_rate (simple, but n small)

Define for each country 
𝑖
i:

recovery
𝑖
=
arrivals
2023
−
arrivals
2021
arrivals
2019
recovery
i
	​

=
arrivals
2019
	​

arrivals
2023
	​

−arrivals
2021
	​

	​


Then run:

recovery
𝑖
=
𝛽
0
+
𝛽
1
Visa
𝑖
+
𝛽
2
PeaceMean
𝑖
+
𝛽
3
FlightsChange
𝑖
+
𝑢
𝑖
recovery
i
	​

=β
0
	​

+β
1
	​

Visa
i
	​

+β
2
	​

PeaceMean
i
	​

+β
3
	​

FlightsChange
i
	​

+u
i
	​


Important: n=8 → don’t include many covariates. Use simple bivariate plots and permutation tests or bootstrap for inference.

C. Diagnostics and robustness (must-run list)

Pre-trends test / event study. If pre-trends fail, drop DiD claims.

Cluster SEs by country. Optionally two-way cluster (country, year) if your software supports it.

Placebo / permutation tests. Randomly assign “treated” status to other countries and record distribution of estimated effects.

Leave-one-out sensitivity. Re-run key model dropping one country at a time—see if Thailand effect survives.

Check multicollinearity (VIFs). High VIFs for ln_cpi/ln_rer/ln_gdp → interpret with caution.

Check influential points. Cook’s distance or leverage on country-year observations (especially 2020).

Multiple testing correction for country × post coefficients.

Power / effective sample size check. With clustered inference and 8 clusters, p-values can be unreliable. Use wild cluster bootstrap for p-values if possible.

D. Practical cautions (why some ideas are weak)

Full country×year interactions (N×T parameters): visually useful but too many estimated parameters if you try to estimate all interactions — prefer event-study plots or a small subset.

Cross-sectional regressions on recovery_rate with many regressors: n=8 kills statistical power and leads to overfitting. Use descriptive evidence and bootstrapped inference.

Synthetic control with few donors: fragile; use as supporting evidence only.

Adding many interactions (Post × CPI × Peace): interpretability collapses and collinearity explodes.

E. How to report results (structure and wording)

Start with the event-study figure demonstrating dynamics and pre-trend check. If pre-trends fail, remove DiD causal language.

Present the heterogeneous post model table: show θ_j for each country with clustered CIs and BH-adjusted p-values. Highlight Thailand’s θ and direct contrasts vs key competitors.

Add mechanism regressions (Post × Peace, Post × Visa, Post × Flights). Emphasize effect sizes and standard errors.

Show synthetic control chart for Thailand with placebo distribution.

Run sensitivity checks: leave-one-out, placebo, wild bootstrap p-values. Put these in appendix.

Conclude cautiously: “Thailand’s post-COVID coefficient is X (CI Y–Z). After robustness checks, evidence suggests Thailand recovered faster/slower relative to the sample, and this difference is [partly/mostly] explained by [visa/flight/safety].”

F. Exact tests you must include (short list)

Pre-trend F-test or visual event-study.

H0: θ_Thailand = 0 (one-sided).

H0: θ_Thailand − θ_Vietnam = 0 (pairwise contrast).

Wild cluster bootstrap p-value for main contrasts.

Placebo distribution of country×post estimates (show where Thailand sits).