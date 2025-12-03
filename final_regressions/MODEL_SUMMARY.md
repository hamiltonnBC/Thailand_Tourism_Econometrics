# Gravity Panel Regression Analysis Summary
## Chinese Tourist Arrivals to Asian Destinations (2008-2024)

---

## Dataset Specification
- **Countries**: 8 destinations (Australia, Cambodia, Indonesia, Japan, Malaysia, Singapore, Thailand, Vietnam)
- **Time Period**: 2008-2024 (17 years)
- **Total Observations**: 136 (perfectly balanced panel: 8 countries × 17 years)
- **Missing Countries**: Korea (missing 2024), Philippines (missing 2023-2024), UK (missing 2020, 2023-2024), Maldives (missing peace_index)

---

## Model Specifications

### MODEL A: Baseline Gravity Model (Entity FE + COVID Dummy)
**Purpose**: Standard gravity model with COVID control

**Variables**:
- Dependent: `ln(arrivals_from_china)`
- Independent: `peace_index`, `ln(cpi_index)`, `ln(gdp_china)`, `ln(exchange_rate)`, `covid_dummy`

**Key Results**:
- **R² Within**: 0.425 (42.5% of within-country variation explained)
- **COVID Impact**: -256% (massive drop during 2020-2021) ✓ Highly significant (p < 0.001)
- **CPI Effect**: +1.44% per 1% CPI increase ✓ Significant (p = 0.034)
- **Peace Index**: +165.8% per 1 unit increase (marginally significant, p = 0.064)
- **China GDP**: +0.39% per 1% GDP increase (not significant)
- **Exchange Rate**: +0.98% per 1% appreciation (not significant)

**Interpretation**: 
- COVID had a devastating impact on tourism
- Higher prices (CPI) surprisingly correlate with MORE tourism (possibly quality signal)
- Less peaceful destinations see fewer tourists (as expected)

---

### MODEL B: Entity FE + Time FE
**Purpose**: Control for all time-varying shocks (including COVID, global trends)

**Variables**:
- Dependent: `ln(arrivals_from_china)`
- Independent: `peace_index`, `ln(cpi_index)`, `ln(exchange_rate)`
- Note: `gdp_china` excluded (absorbed by time FE - same for all countries each year)

**Key Results**:
- **R² Within**: -0.0002 (essentially 0 - time FE absorbs all variation)
- **None of the variables are significant**

**Interpretation**: 
- Time fixed effects absorb most variation (COVID, China's economic cycles, policy changes)
- This model is too restrictive - removes the variation we want to study
- **Recommendation**: Use Model A or C instead

---

### MODEL C: Thailand Asymmetry Analysis ⭐ RECOMMENDED
**Purpose**: Test if Thailand's post-COVID recovery differs from other countries

**Variables**:
- Dependent: `ln(arrivals_from_china)`
- Independent: `peace_index`, `ln(cpi_index)`, `ln(gdp_china)`, `ln(exchange_rate)`, `covid_dummy`, `post_covid`, `thailand_post_covid`

**Key Results**:
- **R² Within**: 0.593 (59.3% of within-country variation explained) - BEST FIT
- **COVID Impact**: -342% during 2020-2021 ✓ Highly significant
- **Post-COVID Recovery (all countries)**: -192% (still below pre-COVID) ✓ Highly significant
- **Thailand-Specific Effect**: +29% ADDITIONAL recovery ✓ Significant (p = 0.040)
- **Total Thailand Post-COVID**: -163% (= -192% + 29%)

**Critical Finding**:
Thailand is recovering FASTER than other countries by 29%, but BOTH Thailand and other countries are still significantly below pre-COVID levels in 2022-2024.

**Interpretation**:
- All countries show incomplete recovery post-COVID
- Thailand shows LESS asymmetry than expected - actually recovering slightly better
- This contradicts the hypothesis of Thailand lagging behind
- **Possible explanations**:
  1. Thailand's visa policies improved
  2. Other countries face different constraints (e.g., Japan's strict entry rules)
  3. Thailand's tourism infrastructure recovered faster
  4. The "asymmetry" might be in absolute numbers, not percentage recovery

---

## Statistical Quality Checks

### Model A & C Pass All Tests:
✓ **F-test for Poolability**: p < 0.001 (entity FE justified)
✓ **Robust Standard Errors**: Clustered by entity (controls for autocorrelation)
✓ **Overall F-statistic**: Highly significant (p < 0.001)

### Potential Issues:
⚠️ **Negative R² Between**: Indicates entity FE model fits poorly for between-country variation (expected - we care about within-country changes)
⚠️ **Exchange Rate Not Significant**: Might be multicollinear with CPI or absorbed by entity FE

---

## Recommendations for Your Econometrics Project

### Primary Model: MODEL C (Thailand Asymmetry)
**Why**: 
- Highest explanatory power (R² = 0.593)
- Directly tests your research question
- Significant Thailand-specific effect
- Controls for COVID appropriately

### Robustness Checks to Add:
1. **Log-log specification** (already done ✓)
2. **Alternative time periods**: 
   - Pre-COVID only (2008-2019)
   - Exclude 2020-2021 entirely
3. **Alternative COVID definitions**:
   - Separate 2020, 2021, 2022 dummies
   - COVID × Country interactions (test if all countries differ)
4. **Add lagged dependent variable**: Test for persistence
5. **First differences**: Address potential non-stationarity

### Additional Variables to Consider:
- **Distance from China** (time-invariant, absorbed by entity FE)
- **Visa policy changes** (if you have data)
- **Flight capacity/routes** (supply-side constraint)
- **Chinese government policy** (outbound tourism restrictions)

---

## Key Takeaway for Your Paper

**Research Question**: Why is there asymmetry in Chinese tourists returning to Thailand?

**Finding**: The data shows Thailand is actually recovering FASTER (+29%) than comparable destinations, though all countries remain below pre-COVID levels. The "asymmetry" may be:
1. In absolute numbers (Thailand had higher baseline)
2. In expectations (Thailand expected to recover more given its tourism dependence)
3. In specific segments (leisure vs. business travel)
4. A perception vs. reality gap

**Recommendation**: Reframe your research question or investigate why Thailand appears to be recovering relatively well despite perceptions of asymmetry.

---

## Files Generated
1. `regression_results_model1.txt` - Full regression output
2. `regression_coefficients_model1.csv` - Coefficients for tables
3. `arrivals_by_country.png` - Time series visualization
4. `thailand_asymmetry.png` - Thailand vs others comparison
5. `log_arrivals_by_country.png` - Log-transformed view
6. `correlation_matrix.png` - Variable correlations

---

**Date**: December 3, 2025
**Script**: `running_panel_data_regression.py`
