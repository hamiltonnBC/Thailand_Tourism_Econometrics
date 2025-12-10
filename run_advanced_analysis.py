import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'final_regressions/new_models_data')
output_dir = script_dir

# Load Data
thailand_ts = pd.read_csv(os.path.join(data_dir, 'thailand_timeseries.csv'))
panel_df = pd.read_csv(os.path.join(data_dir, 'competitor_panel.csv'))

# Output file
results_file = os.path.join(output_dir, 'advanced_analysis_results.txt')

with open(results_file, 'w') as f:
    f.write("=" * 80 + "\n")
    f.write("ADVANCED ECONOMETRIC ANALYSIS RESULTS\n")
    f.write("=" * 80 + "\n\n")

    # ==========================================
    # 1. DIAGNOSTIC TESTS (Thailand Model 1)
    # ==========================================
    f.write("1. DIAGNOSTIC TESTS (Thailand Time Series Model)\n")
    f.write("-" * 80 + "\n")
    
    # Re-estimate Model 1
    y = thailand_ts['ln_arrivals']
    X = thailand_ts[['ln_gdp_china', 'ln_rer', 'covid_dummy']]
    X = sm.add_constant(X)
    model1 = sm.OLS(y, X).fit()
    
    # A. Multicollinearity (VIF)
    f.write("\nA. Multicollinearity (VIF):\n")
    vif_data = pd.DataFrame()
    vif_data["Variable"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    f.write(vif_data.to_string(index=False) + "\n")
    f.write("   > Rule of Thumb: VIF > 10 indicates high multicollinearity.\n")
    
    # B. Heteroscedasticity (Breusch-Pagan)
    f.write("\nB. Heteroscedasticity (Breusch-Pagan Test):\n")
    bp_test = het_breuschpagan(model1.resid, model1.model.exog)
    f.write(f"   Lagrange Multiplier Statistic: {bp_test[0]:.4f}\n")
    f.write(f"   P-value: {bp_test[1]:.4f}\n")
    if bp_test[1] < 0.05:
        f.write("   > Result: Heteroscedasticity detected (P < 0.05). Use robust standard errors (HC1/HAC).\n")
    else:
        f.write("   > Result: Homoscedasticity assumed (P >= 0.05).\n")
        
    # C. Autocorrelation (Durbin-Watson)
    f.write("\nC. Autocorrelation (Durbin-Watson):\n")
    dw_stat = durbin_watson(model1.resid)
    f.write(f"   D-W Statistic: {dw_stat:.4f}\n")
    f.write("   > Rule of Thumb: Values near 2.0 indicate no autocorrelation. < 1.5 suggests positive autocorrelation.\n")
    
    # D. Normality of Residuals (Shapiro-Wilk)
    f.write("\nD. Normality of Residuals (Shapiro-Wilk Test):\n")
    sw_stat, sw_p = stats.shapiro(model1.resid)
    f.write(f"   Statistic: {sw_stat:.4f}, P-value: {sw_p:.4f}\n")
    if sw_p < 0.05:
        f.write("   > Result: Residuals are NOT normally distributed (P < 0.05).\n")
    else:
        f.write("   > Result: Residuals are normally distributed (P >= 0.05).\n")

    # ==========================================
    # 2. ADVANCED MODEL: ADL(1,0)
    # ==========================================
    f.write("\n\n2. ADVANCED MODEL: ADL(1,0) (Habit Persistence)\n")
    f.write("-" * 80 + "\n")
    
    # Create lagged dependent variable
    thailand_ts['ln_arrivals_lag1'] = thailand_ts['ln_arrivals'].shift(1)
    
    # Drop first observation (NaN due to lag)
    thailand_adl = thailand_ts.dropna().copy()
    
    y_adl = thailand_adl['ln_arrivals']
    X_adl = thailand_adl[['ln_arrivals_lag1', 'ln_gdp_china', 'ln_rer', 'covid_dummy']]
    X_adl = sm.add_constant(X_adl)
    
    model_adl = sm.OLS(y_adl, X_adl).fit(cov_type='HAC', cov_kwds={'maxlags': 1})
    f.write(model_adl.summary().as_text() + "\n")
    
    # Calculate Long-Run Elasticities
    # LR_beta = Short_Run_beta / (1 - rho)
    rho = model_adl.params['ln_arrivals_lag1']
    sr_price_elast = model_adl.params['ln_rer']
    lr_price_elast = sr_price_elast / (1 - rho)
    
    f.write("\nELASTICITY ANALYSIS:\n")
    f.write(f"   Habit Persistence (rho): {rho:.4f}\n")
    f.write(f"   Short-Run Price Elasticity: {sr_price_elast:.4f}\n")
    f.write(f"   Long-Run Price Elasticity: {lr_price_elast:.4f}\n")
    
    # ==========================================
    # 3. COMPARATIVE ELASTICITY ANALYSIS
    # ==========================================
    f.write("\n\n3. COMPARATIVE ELASTICITY ANALYSIS (Thailand vs Competitors)\n")
    f.write("-" * 80 + "\n")
    f.write(f"{'Country':<15} {'Price Elasticity':<20} {'P-Value':<10} {'Significance':<15}\n")
    f.write("-" * 60 + "\n")
    
    competitors = ['Thailand', 'Viet Nam', 'Malaysia', 'Indonesia']
    elasticity_results = []
    
    for country in competitors:
        country_data = panel_df[panel_df['Country'] == country].copy()
        
        # Simple Time Series Model for each country
        # Note: Using same variables as Thailand Model 1 for comparability
        y_c = country_data['ln_arrivals']
        X_c = country_data[['ln_gdp_china', 'ln_rer', 'covid_dummy']]
        X_c = sm.add_constant(X_c)
        
        try:
            mod_c = sm.OLS(y_c, X_c).fit(cov_type='HAC', cov_kwds={'maxlags': 1})
            pe = mod_c.params['ln_rer']
            pval = mod_c.pvalues['ln_rer']
            sig = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else "ns"
            
            f.write(f"{country:<15} {pe:<20.4f} {pval:<10.4f} {sig:<15}\n")
            elasticity_results.append({'Country': country, 'Elasticity': pe, 'Lower': mod_c.conf_int().loc['ln_rer'][0], 'Upper': mod_c.conf_int().loc['ln_rer'][1]})
            
        except Exception as e:
            f.write(f"{country:<15} ERROR: {str(e)}\n")

print(f"Analysis complete. Results saved to {results_file}")

# Visualization: Comparative Elasticity
if elasticity_results:
    elast_df = pd.DataFrame(elasticity_results)
    
    plt.figure(figsize=(10, 6))
    # Create error bars
    yerr = [elast_df['Elasticity'] - elast_df['Lower'], elast_df['Upper'] - elast_df['Elasticity']]
    
    plt.bar(elast_df['Country'], elast_df['Elasticity'], yerr=yerr, capsize=10, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'], alpha=0.8)
    plt.axhline(y=0, color='black', linewidth=1)
    plt.title('Price Elasticity of Demand by Destination\n(Sensitivity to Exchange Rate Changes)', fontsize=14)
    plt.ylabel('Price Elasticity\n(Negative value = More sensitive)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, v in enumerate(elast_df['Elasticity']):
        plt.text(i, v + (0.1 if v > 0 else -0.3), f"{v:.2f}", ha='center', fontweight='bold')
        
    plt.savefig(os.path.join(output_dir, 'comparative_elasticity.png'), dpi=300)
    print("Saved comparative_elasticity.png")
