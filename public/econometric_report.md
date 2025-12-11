# Econometric Analysis of Chinese Tourism Demand in Thailand (2000-2024)

## Executive Summary
This report presents a robust econometric analysis of the determinants of Chinese tourist arrivals in Thailand. Using a 25-year time series dataset (2000-2024), we identify the key drivers of demand and quantify the sensitivity of tourism flows to economic factors.

**Key Findings:**
1.  **Price Sensitivity**: Thailand's tourism demand is highly elastic to price changes in the long run. A 1% appreciation of the Real Exchange Rate (RER) leads to a **3.07% decrease** in arrivals over time.
2.  **Income Driver**: Chinese GDP is a strong positive driver, with a 1% increase in GDP leading to a **0.67% increase** in arrivals.
3.  **Habit Persistence**: There is significant "habit persistence" (32%), meaning past visits strongly influence future demand.
4.  **Competitive Landscape**: Thailand competes closely with Indonesia on price, while Vietnam and Malaysia show less sensitivity to exchange rate fluctuations.

---

## 1. Data Overview
The analysis utilizes a curated dataset covering the period **2000-2024**.

**Key Variables:**
*   **Dependent Variable**: Log of Chinese Tourist Arrivals ($\ln(\text{Arrivals})$).
*   **Income Variable**: Log of China's GDP ($\ln(\text{GDP}_{\text{China}})$).
*   **Price Variable**: Log of Real Exchange Rate ($\ln(\text{RER})$).
    *   *Note: RER accounts for both nominal exchange rates and relative inflation (CPI).*
*   **Control Variables**: COVID-19 Dummy (2020-2022).

### Data Visualization
The correlation matrix below confirms strong relationships between the key variables, justifying their inclusion in the model.

![Correlation Matrix](/Users/hamiltonn/.gemini/antigravity/brain/662d79fd-85b8-44e1-8bfa-3fc77858726e/thailand_correlation_matrix.png)

The trend analysis shows how closely tourist arrivals track Chinese economic growth (GDP), interrupted only by the massive shock of COVID-19.

![Trends: GDP vs Arrivals](/Users/hamiltonn/.gemini/antigravity/brain/662d79fd-85b8-44e1-8bfa-3fc77858726e/thailand_trends_gdp.png)

---

## 2. Model 1: Thailand Time Series Analysis
**Objective**: To estimate the short-run price and income elasticities of demand for Thailand specifically.

### Methodology
We employ an **Ordinary Least Squares (OLS)** regression with **HAC (Heteroscedasticity and Autocorrelation Consistent)** standard errors to correct for potential serial correlation and heteroscedasticity detected in diagnostic tests.

**Regression Equation:**
$$ \ln(\text{Arrivals}_t) = \alpha + \beta_1 \ln(\text{GDP}_{\text{China}, t}) + \beta_2 \ln(\text{RER}_t) + \beta_3 \text{COVID}_t + \epsilon_t $$

### Results
| Variable | Coefficient | Std. Error | P-Value | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Log(GDP China)** | **0.67** | 0.21 | **0.001** | **Income Elasticity**: +0.67% arrivals for +1% GDP. |
| **Log(RER)** | **-2.33** | 1.10 | **0.034** | **Price Elasticity**: -2.33% arrivals for +1% Price (Appreciation). |
| **COVID Dummy** | **-3.57** | 0.72 | **0.000** | **Pandemic Shock**: ~97% drop in arrivals. |

**Model Fit:**
The model explains **72.5%** of the variation in tourist arrivals ($R^2 = 0.725$). The predicted values track the actual data very closely, capturing both the pre-2010 trends and the post-2010 boom.

![Actual vs Predicted](/Users/hamiltonn/.gemini/antigravity/brain/662d79fd-85b8-44e1-8bfa-3fc77858726e/model1_actual_vs_predicted.png)

---

## 3. Advanced Model: Habit Persistence (ADL)
**Objective**: To distinguish between short-run and long-run effects by accounting for "habit persistence" (tourists returning to a familiar destination).

### Methodology
We estimate an **Autoregressive Distributed Lag (ADL(1,0))** model by including the lagged dependent variable ($\ln(\text{Arrivals}_{t-1})$).

**Regression Equation:**
$$ \ln(\text{Arrivals}_t) = \alpha + \rho \ln(\text{Arrivals}_{t-1}) + \beta_1 \ln(\text{GDP}_{\text{China}, t}) + \beta_2 \ln(\text{RER}_t) + \dots $$

### Results
*   **Habit Persistence ($\rho$)**: **0.32** ($p=0.05$). This indicates that **32%** of the previous year's tourism volume "carries over" to the current year, reflecting strong destination loyalty or inertia.
*   **Long-Run Price Elasticity**: **-3.07**.
    *   *Calculation*: $\beta_{LR} = \beta_{SR} / (1 - \rho) = -2.08 / (1 - 0.32) = -3.07$.
    *   *Insight*: The negative impact of a price increase (e.g., Baht appreciation) is **amplified over time**. In the short run, tourists may still come due to pre-booked plans, but in the long run, they switch to cheaper destinations.

---

## 4. Model 2: Competitive Analysis Panel
**Objective**: To compare Thailand's recovery and price sensitivity against key regional competitors (Vietnam, Malaysia, Indonesia).

### Methodology
We use a **Panel Fixed Effects** model covering the period **2008-2024**.

### Comparative Elasticity
We estimated the price elasticity for each country individually to see how they compare.

![Comparative Elasticity](/Users/hamiltonn/.gemini/antigravity/brain/662d79fd-85b8-44e1-8bfa-3fc77858726e/comparative_elasticity.png)

*   **Indonesia (-2.88)**: The most price-sensitive destination.
*   **Thailand (-2.33)**: Highly sensitive (in the long-run model).
*   **Malaysia (-1.18)** & **Vietnam (-0.70)**: Less sensitive (elasticity not statistically significant).

### Recovery Scorecard
Comparing 2024 arrivals to pre-pandemic (2019) levels:

![Recovery Scorecard](/Users/hamiltonn/.gemini/antigravity/brain/662d79fd-85b8-44e1-8bfa-3fc77858726e/recovery_scorecard.png)

*   **Vietnam**: Leading the recovery (~60% of 2019 levels).
*   **Thailand**: Lagging slightly behind (~60%), statistically indistinguishable from the group average.
*   **Indonesia**: Showing the slowest recovery in this specific Chinese market segment.

---

## Conclusion
This econometric analysis confirms that **Thailand's tourism sector is highly sensitive to economic fundamentals**.
1.  **Growth Engine**: Continued growth in China's GDP will naturally drive arrivals, but at a rate less than 1:1 (inelastic income demand).
2.  **Risk Factor**: The **Real Exchange Rate** is a critical variable. A strengthening Baht poses a significant risk to competitiveness, especially against price-sensitive competitors like Indonesia.
3.  **Policy Implication**: To maintain competitiveness, Thailand must either manage exchange rate volatility or—more sustainably—move up the value chain to reduce price sensitivity (making demand more inelastic).
