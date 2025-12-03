/**
 * Model Page Component
 * 
 * The Model page with sub-tabs for Methodology, Specification, and Constraints & Tests.
 */

import { useState } from 'react'
import { Box, HStack, Text, Code, VStack } from '@chakra-ui/react'
import { RegressionModelCard } from '../components/RegressionModelCard'

type ModelTab = 'development' | 'specification' | 'diagnostics' | 'limitations'

export function Model() {
  const [activeSubTab, setActiveSubTab] = useState<ModelTab>('development')

  return (
    <Box>
      <Box fontSize="3xl" fontWeight="bold" mb={6} color="#1e293b">
        The Model
      </Box>

      {/* Sub-navigation tabs */}
      <HStack gap={2} mb={8} borderBottom="2px" borderColor="#e2e8f0" pb={0}>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'development' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'development' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'development' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('development')}
        >
          Model Development
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'specification' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'specification' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'specification' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('specification')}
        >
          Final Specification
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'diagnostics' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'diagnostics' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'diagnostics' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('diagnostics')}
        >
          Diagnostic Tests
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'limitations' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'limitations' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'limitations' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('limitations')}
        >
          Limitations
        </Box>
      </HStack>

      {/* Content area */}
      <Box color="#1e293b" lineHeight="1.8">
        {activeSubTab === 'development' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                The Iterative Journey
              </Text>
              <Text color="#64748b" mb={4}>
                Developing our econometric model was not a linear process—it was an iterative journey of exploration, 
                testing, and refinement. We tried multiple approaches, ran countless diagnostic tests, and learned from 
                each iteration. This section documents that journey.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Phase 1: Initial Exploration
              </Text>
              <Text color="#64748b" mb={3}>
                We began by exploring various modeling approaches mentioned in the literature:
              </Text>
              <Box as="ul" pl={6} color="#64748b" mb={4}>
                <Box as="li" mb={2}>
                  <strong>Simple OLS Regression:</strong> Our first attempt used basic linear regression, but we quickly 
                  discovered issues with heteroskedasticity and autocorrelation across countries.
                </Box>
                <Box as="li" mb={2}>
                  <strong>Time Series Models:</strong> We explored ARIMA and other time series approaches, but these 
                  couldn't capture the cross-country variation we needed.
                </Box>
                <Box as="li" mb={2}>
                  <strong>Gradient Boosting Trees:</strong> We experimented with machine learning approaches, but they 
                  lacked the interpretability we needed for policy recommendations.
                </Box>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Phase 2: Panel Data Discovery
              </Text>
              <Text color="#64748b" mb={4}>
                After reviewing tourism econometrics literature, particularly Yunitaningtyas et al. (2019), we realized 
                that panel data methods were ideal for our research question. We had:
              </Text>
              <Box as="ul" pl={6} color="#64748b" mb={4}>
                <Box as="li" mb={2}>Multiple countries (cross-sectional dimension)</Box>
                <Box as="li" mb={2}>Multiple years (time dimension)</Box>
                <Box as="li" mb={2}>Country-specific effects we needed to control for</Box>
                <Box as="li">Time-varying shocks affecting all countries</Box>
              </Box>
              <Text color="#64748b">
                This led us to explore Fixed Effects vs. Random Effects models.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Phase 3: Model Specification Trials
              </Text>
              <Text color="#64748b" mb={3}>
                We ran multiple model specifications, each teaching us something new:
              </Text>
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <VStack align="stretch" gap={3}>
                  <Box>
                    <Text fontWeight="semibold" mb={2}>Version 1: Basic Gravity Model</Text>
                    <Text color="#64748b" fontSize="sm">
                      Included distance, GDP, and population. Problem: Distance is time-invariant and gets absorbed by 
                      country fixed effects.
                    </Text>
                  </Box>
                  <Box>
                    <Text fontWeight="semibold" mb={2}>Version 2: Adding Economic Variables</Text>
                    <Text color="#64748b" fontSize="sm">
                      Added exchange rates and CPI. Better, but still missing the safety dimension that literature 
                      emphasized.
                    </Text>
                  </Box>
                  <Box>
                    <Text fontWeight="semibold" mb={2}>Version 3: Safety Index Integration</Text>
                    <Text color="#64748b" fontSize="sm">
                      Incorporated Global Peace Index. Improved model fit, but we debated whether to use objective or 
                      perceived safety metrics.
                    </Text>
                  </Box>
                  <Box>
                    <Text fontWeight="semibold" mb={2}>Version 4: GDP vs. Year Fixed Effects</Text>
                    <Text color="#64748b" fontSize="sm">
                      Tested two approaches: one with Chinese GDP explicitly, another with year fixed effects. The latter 
                      better captured global shocks like COVID-19.
                    </Text>
                  </Box>
                </VStack>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Phase 4: Variable Transformations
              </Text>
              <Text color="#64748b" mb={4}>
                We learned that raw values created problems due to scale differences between countries. We experimented with:
              </Text>
              <Box as="ul" pl={6} color="#64748b" mb={4}>
                <Box as="li" mb={2}>
                  <strong>Log transformations:</strong> Allowed us to interpret coefficients as percentage changes and 
                  smoothed outliers
                </Box>
                <Box as="li" mb={2}>
                  <strong>Standardization:</strong> Tested z-scores but found logs more interpretable
                </Box>
                <Box as="li">
                  <strong>Index creation:</strong> Built CPI indices with 2010 as base year for consistency
                </Box>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Phase 5: The "Thailand Penalty" Variable
              </Text>
              <Text color="#64748b" mb={4}>
                A breakthrough came when we realized we could create an interaction term (Thailand × Post-2023) to 
                directly measure the asymmetric recovery. This Difference-in-Differences approach allowed us to:
              </Text>
              <Box as="ul" pl={6} color="#64748b">
                <Box as="li" mb={2}>Isolate Thailand's specific effect</Box>
                <Box as="li" mb={2}>Control for global trends affecting all countries</Box>
                <Box as="li">Quantify the exact magnitude of the penalty</Box>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Key Lessons Learned
              </Text>
              <Box bg="#f1f5f9" p={4} borderRadius="md" border="1px" borderColor="#cbd5e1">
                <VStack align="stretch" gap={2}>
                  <Text color="#64748b">
                    ✓ Panel data methods are powerful for tourism research with multiple countries and years
                  </Text>
                  <Text color="#64748b">
                    ✓ Fixed Effects control for unobserved heterogeneity better than Random Effects for our data
                  </Text>
                  <Text color="#64748b">
                    ✓ Log transformations improve interpretability and handle scale differences
                  </Text>
                  <Text color="#64748b">
                    ✓ Interaction terms can isolate specific treatment effects
                  </Text>
                  <Text color="#64748b">
                    ✓ Every model specification teaches you something, even the "failed" ones
                  </Text>
                </VStack>
              </Box>
            </Box>

            {/* Regression Model Specifications */}
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model Specifications & Tests
              </Text>
              <Text color="#64748b" mb={6}>
                Below are the key regression models we developed, along with the hypothesis tests that validate 
                our approach. Each model builds on insights from the previous iterations.
              </Text>

              <VStack align="stretch" gap={6}>
                {/* Model A: Baseline Gravity Model */}
                <RegressionModelCard
                  modelName="Model A: Baseline Gravity Model with Entity Fixed Effects"
                  modelEquation="ln(Arrivals_it) = α_i + β₁(Peace_Index_it) + β₂ln(CPI_it) + β₃ln(GDP_China_t) + β₄ln(Exchange_Rate_it) + β₅(COVID_Dummy_t) + ε_it"
                  description="This is our baseline specification using entity (country) fixed effects to control for time-invariant country characteristics. We include a COVID dummy variable to capture the pandemic's impact on tourism flows. The model uses nominal exchange rates and includes China's GDP to capture the income effect on outbound tourism demand. R² = 0.4261, N = 136 observations across 8 countries."
                  keyFindings={[
                    'Peace Index: β = 1.69, p = 0.059 (marginally significant at 10% level)',
                    'CPI: β = 1.46, p = 0.035 → 1% increase in CPI leads to 1.46% increase in arrivals',
                    'China GDP: β = 0.39, p = 0.177 (not significant)',
                    'Exchange Rate: β = 1.00, p = 0.263 (not significant)',
                    'COVID Dummy: β = -2.56, p < 0.001 → 92.3% decrease in arrivals during 2020-2021'
                  ]}
                  hypothesisTests={[
                    {
                      name: 'F-Test for Poolability',
                      nullHypothesis: 'All country fixed effects are jointly zero (pooled OLS is sufficient)',
                      pValue: 'F = 7.04, p < 0.001',
                      result: 'Reject H₀',
                      interpretation: 'Country fixed effects are necessary. Countries have significant unobserved heterogeneity that must be controlled for.'
                    },
                    {
                      name: 'CPI Coefficient Test',
                      nullHypothesis: 'β₂ (ln CPI) = 0',
                      pValue: 't = 2.13, p = 0.035',
                      result: 'Reject H₀',
                      interpretation: 'CPI significantly affects arrivals. Higher prices are associated with more arrivals (possibly quality signal).'
                    },
                    {
                      name: 'COVID Impact Test',
                      nullHypothesis: 'β₅ (COVID Dummy) = 0',
                      pValue: 't = -12.52, p < 0.001',
                      result: 'Reject H₀',
                      interpretation: 'COVID-19 had a massive negative impact, reducing arrivals by approximately 92% during 2020-2021.'
                    }
                  ]}
                />

                {/* Model C: Thailand Asymmetry */}
                <RegressionModelCard
                  modelName="Model C: Thailand Asymmetry Analysis"
                  modelEquation="ln(Arrivals_it) = α_i + β₁(Peace_Index_it) + β₂ln(CPI_it) + β₃ln(GDP_China_t) + β₄ln(Exchange_Rate_it) + β₅(COVID_t) + β₆(Post_COVID_t) + β₇(Thailand × Post_COVID_it) + ε_it"
                  description="This model introduces our key innovation: an interaction term (Thailand × Post-COVID) to capture Thailand's asymmetric recovery. This is a Difference-in-Differences approach that isolates Thailand's specific post-pandemic effect relative to other destinations. The coefficient β₇ directly measures the 'Thailand Bonus' (surprisingly positive!). R² = 0.5935, N = 136."
                  keyFindings={[
                    'Peace Index: β = 0.40, p = 0.578 (not significant in this specification)',
                    'CPI: β = 3.23, p = 0.026 → 1% increase in CPI leads to 3.23% increase in arrivals',
                    'China GDP: β = 1.09, p = 0.008 → 1% increase in China GDP leads to 1.09% increase in arrivals',
                    'COVID Dummy: β = -3.42, p < 0.001 → 96.7% decrease during pandemic',
                    'Post-COVID: β = -1.92, p < 0.001 → General recovery still 85% below pre-pandemic',
                    'Thailand × Post-COVID: β = +0.30, p = 0.038 → Thailand recovers 34% FASTER than others!'
                  ]}
                  hypothesisTests={[
                    {
                      name: 'Thailand Effect Test',
                      nullHypothesis: 'β₇ (Thailand × Post-COVID) = 0',
                      pValue: 't = 2.10, p = 0.038',
                      result: 'Reject H₀',
                      interpretation: 'Thailand has a statistically significant POSITIVE asymmetric recovery! Contrary to expectations, Thailand is recovering faster than comparable destinations by approximately 34%.'
                    },
                    {
                      name: 'China GDP Significance',
                      nullHypothesis: 'β₃ (ln GDP China) = 0',
                      pValue: 't = 2.72, p = 0.008',
                      result: 'Reject H₀',
                      interpretation: 'China\'s economic growth significantly drives outbound tourism. A 1% increase in China\'s GDP leads to a 1.09% increase in tourist arrivals.'
                    },
                    {
                      name: 'Model Fit Improvement',
                      nullHypothesis: 'Model C fits no better than Model A',
                      pValue: 'R² = 0.594 vs 0.426',
                      result: 'Reject H₀',
                      interpretation: 'Adding the Thailand interaction and post-COVID variables substantially improves model fit, explaining 59% of within-country variation.'
                    }
                  ]}
                />

                {/* Model D: Real Exchange Rate */}
                <RegressionModelCard
                  modelName="Model D: Real Exchange Rate Specification"
                  modelEquation="ln(Arrivals_it) = α_i + β₁(Peace_Index_it) + β₂ln(CPI_it) + β₃ln(GDP_China_t) + β₄ln(RER_it) + β₅(COVID_Dummy_t) + ε_it"
                  description="This model replaces the nominal exchange rate with the Real Exchange Rate (RER), which adjusts for inflation differences between China and destination countries. RER provides a more accurate measure of relative price competitiveness. We normalize RER within each country to handle scale differences and make log transformations stable. R² = 0.4265, N = 136."
                  keyFindings={[
                    'Peace Index: β = 1.11, p = 0.207 (not significant)',
                    'CPI: β = 1.86, p < 0.001 → 1% increase in CPI leads to 1.86% increase in arrivals',
                    'China GDP: β = -0.19, p = 0.715 (not significant, absorbed by time effects)',
                    'Real Exchange Rate: β = -0.97, p = 0.207 → 1% real appreciation reduces arrivals by 0.97%',
                    'COVID Dummy: β = -2.53, p < 0.001 → 92% decrease during pandemic',
                    'RER has expected negative sign (appreciation reduces arrivals) unlike nominal ER'
                  ]}
                  hypothesisTests={[
                    {
                      name: 'CPI Coefficient Test',
                      nullHypothesis: 'β₂ (ln CPI) = 0',
                      pValue: 't = 4.20, p < 0.001',
                      result: 'Reject H₀',
                      interpretation: 'CPI is highly significant. Higher prices are strongly associated with more arrivals, possibly indicating quality signaling or luxury tourism.'
                    },
                    {
                      name: 'F-Test for Poolability',
                      nullHypothesis: 'Country fixed effects are jointly zero',
                      pValue: 'F = 7.07, p < 0.001',
                      result: 'Reject H₀',
                      interpretation: 'Country fixed effects remain necessary even with RER specification. Unobserved country characteristics matter.'
                    },
                    {
                      name: 'RER vs Nominal ER',
                      nullHypothesis: 'RER provides no improvement over nominal ER',
                      pValue: 'Log-likelihood: -185.36 vs -185.40',
                      result: 'Marginal improvement',
                      interpretation: 'RER has theoretically correct sign (negative) and similar model fit. Both specifications are valid, but RER is theoretically preferred.'
                    }
                  ]}
                />

                {/* Model F: Thailand Asymmetry with RER */}
                <RegressionModelCard
                  modelName="Model F: Thailand Asymmetry with Real Exchange Rate"
                  modelEquation="ln(Arrivals_it) = α_i + β₁(Peace_Index_it) + β₂ln(CPI_it) + β₃ln(GDP_China_t) + β₄ln(RER_it) + β₅(COVID_t) + β₆(Post_COVID_t) + β₇(Thailand × Post_COVID_it) + ε_it"
                  description="This combines our best specifications: the Thailand asymmetry analysis with the theoretically superior Real Exchange Rate measure. This is our preferred model as it uses RER (which properly accounts for inflation) while testing for Thailand's specific recovery pattern. R² = 0.5877, N = 136."
                  keyFindings={[
                    'Peace Index: β = 0.30, p = 0.664 (not significant)',
                    'CPI: β = 2.12, p = 0.014 → 1% increase in CPI leads to 2.12% increase in arrivals',
                    'China GDP: β = 1.43, p = 0.003 → 1% increase in China GDP leads to 1.43% increase in arrivals',
                    'Real Exchange Rate: β = 0.87, p = 0.295 (not significant in this specification)',
                    'COVID Dummy: β = -3.47, p < 0.001 → 96.9% decrease during pandemic',
                    'Post-COVID: β = -1.98, p < 0.001 → General recovery still 86% below baseline',
                    'Thailand × Post-COVID: β = +0.30, p = 0.014 → Thailand recovers 35% FASTER!'
                  ]}
                  hypothesisTests={[
                    {
                      name: 'Thailand Recovery Test',
                      nullHypothesis: 'β₇ (Thailand × Post-COVID) = 0',
                      pValue: 't = 2.50, p = 0.014',
                      result: 'Reject H₀',
                      interpretation: 'Even with RER controls, Thailand shows a significant positive recovery effect. Thailand is recovering approximately 35% faster than comparable destinations in the post-COVID period.'
                    },
                    {
                      name: 'China GDP Effect',
                      nullHypothesis: 'β₃ (ln GDP China) = 0',
                      pValue: 't = 3.05, p = 0.003',
                      result: 'Reject H₀',
                      interpretation: 'China\'s economic growth is a strong driver of outbound tourism. The elasticity of 1.43 suggests tourism is a luxury good (income elastic).'
                    },
                    {
                      name: 'Overall Model Significance',
                      nullHypothesis: 'All coefficients are jointly zero',
                      pValue: 'F = 24.64, p < 0.001',
                      result: 'Reject H₀',
                      interpretation: 'The model as a whole is highly significant. The combination of economic factors, COVID effects, and Thailand-specific recovery explains 59% of variation.'
                    }
                  ]}
                />
              </VStack>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'specification' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model Equation
              </Text>
              <Box bg="#f8fafc" p={6} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Code fontSize="md" colorScheme="gray">
                  ln(Arrivals_it) = α_i + β₁ ln(GDP_PC_t) + β₂ ln(RER_it) + β₃ (Safety_Index_it) + 
                  β₄ (Competitor_Price_it) + ε_it
                </Code>
              </Box>
            </Box>

            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Variable Definitions
              </Text>
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" mb={2}>ln(TA_it)</Text>
                  <Text color="#64748b">
                    Natural log of Chinese Tourist Arrivals to country i in year t. Log transformation allows 
                    interpretation of coefficients as percentage changes.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>ln(GDP_PC_t)</Text>
                  <Text color="#64748b">
                    Real GDP Per Capita of China (captures the Income Effect). This controls for China's overall 
                    economic capacity to generate outbound tourism.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>ln(RER_it)</Text>
                  <Text color="#64748b">
                    Real Exchange Rate between China and country i (captures the Price Effect). This measures the 
                    relative cost of travel to each destination.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Safety_Index_it</Text>
                  <Text color="#64748b">
                    Global Peace Index Score from Vision of Humanity (IEP). Note: This measures objective safety 
                    metrics, not perceived safety from Chinese citizens specifically.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>α_i</Text>
                  <Text color="#64748b">
                    Country-Fixed Effects. This effectively removes all time-invariant characteristics (e.g., 
                    "France is far away," "Thailand has beaches") from the error term, controlling for unobserved 
                    heterogeneity.
                  </Text>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Additional Variables
              </Text>
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Visa Policy (Binary)</Text>
                  <Text color="#64748b">
                    1 if the destination country offers free visa to Chinese citizens for that given year, 0 if not.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Consumer Price Index (CPI)</Text>
                  <Text color="#64748b">
                    Controls for how expensive the country is. Base year set to 2010 = 100.
                  </Text>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model Variations
              </Text>
              <Text color="#64748b">
                We ran two models: the first including Chinese GDP, and the second we switched it out for year fixed 
                effects. For several of the variables, we take the natural log of the value so that our results can be 
                read as percentages. This smooths out massive outliers between countries.
              </Text>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'diagnostics' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model Limitations
              </Text>
              <Text color="#64748b" mb={4}>
                For every model, there are of course a multitude of econometric limitations. We want to address those 
                that we have thus far identified with ours, justify why we feel there is still value in our model, and 
                detail some of the tests (and results) that we have run.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Parallel Trends Assumption
              </Text>
              <Text color="#64748b" mb={4}>
                Our model treats Thailand as a single treated unit with a universal "post-2023" treatment window. A 
                standard DiD assumption is that, absent that treatment, the treated unit would follow the same path as 
                the control group. This is known as Parallel Trends.
              </Text>
              <Text color="#64748b" fontWeight="semibold" mb={2}>
                Validation Checks:
              </Text>
              <VStack align="stretch" gap={3} pl={4}>
                <Text color="#64748b">
                  1. We plotted the pre-treatment trends from 2010-2019 for Thailand vs the control group average. 
                  This allowed us to do a quick visual inspection of the parallel trends.
                </Text>
                <Text color="#64748b">
                  2. We performed a spatial placebo test by re-estimating the model assigning a false treatment to a 
                  control country (Vietnam). Our hypothesis is that the coefficient for (Vietnam x Post2023) should be 
                  statistically indistinguishable from zero. If this is the case, this supports our claim that the 
                  penalty is unique to Thailand.
                </Text>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Diagnostic Tests
              </Text>
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Hausman Test</Text>
                  <Text color="#64748b">
                    We performed a Hausman test to confirm that Fixed Effects (FE) is the appropriate estimator over 
                    Random Effects (RE), ensuring that we control for time-invariant unobserved heterogeneity (e.g., 
                    distance, culture).
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Modified Wald Test</Text>
                  <Text color="#64748b">
                    Testing for groupwise heteroskedasticity across panel groups.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Wooldridge Test</Text>
                  <Text color="#64748b">
                    Testing for autocorrelation in panel data.
                  </Text>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Year Fixed Effects
              </Text>
              <Text color="#64748b">
                The inclusion of Year Fixed Effects absorbs certain variables such as China's GDP and global shocks 
                (like the COVID-19 pandemic). This absorption is intentional. By controlling for YFE, our identification 
                relies exclusively on the cross-sectional variation of destination-specific variables, which vary 
                independently across countries and time.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Potential Endogeneity Concerns
              </Text>
              <Text color="#64748b">
                We acknowledge potential endogeneity in our safety variable. For example, if a drop in tourism revenue 
                causes political instability (rather than the reverse), this could bias our estimates. Future iterations 
                may employ a lagged variable approach (t-1) to address this concern.
              </Text>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'diagnostics' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Diagnostic Testing Journey
              </Text>
              <Text color="#64748b" mb={4}>
                For every model iteration, we ran a battery of diagnostic tests. This wasn't just checking boxes—each 
                test revealed something about our data and helped us refine our approach.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Hausman Test: Fixed vs. Random Effects
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>Purpose:</strong> Determine whether Fixed Effects or Random Effects is the appropriate estimator.
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>Hypothesis:</strong>
              </Text>
              <Box pl={4} mb={3}>
                <Text color="#64748b">H₀: Random Effects is consistent (preferred)</Text>
                <Text color="#64748b">H₁: Fixed Effects is required</Text>
              </Box>
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Text fontWeight="semibold" mb={2}>Result:</Text>
                <Text color="#64748b">
                  Prob &gt; chi2 = 0.000. We reject the null hypothesis and proceed with Fixed Effects. This confirms 
                  that country-specific effects are correlated with our regressors, making FE the appropriate choice.
                </Text>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Modified Wald Test for Heteroskedasticity
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>Purpose:</strong> Test for groupwise heteroskedasticity across panel groups (countries).
              </Text>
              <Text color="#64748b" mb={4}>
                Heteroskedasticity means the variance of errors differs across countries. This is common in tourism 
                data where large countries (like Japan) have more volatile tourist flows than smaller ones.
              </Text>
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Text fontWeight="semibold" mb={2}>What we found:</Text>
                <Text color="#64748b">
                  Evidence of heteroskedasticity across countries. We addressed this by using robust standard errors 
                  in our final specification.
                </Text>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Wooldridge Test for Autocorrelation
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>Purpose:</strong> Test for first-order autocorrelation in panel data.
              </Text>
              <Text color="#64748b" mb={4}>
                Autocorrelation means errors in one year are correlated with errors in the next year. This is 
                particularly relevant for tourism, where a bad year often leads to another bad year.
              </Text>
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Text fontWeight="semibold" mb={2}>What we found:</Text>
                <Text color="#64748b">
                  Some evidence of autocorrelation. We considered AR(1) corrections but found that year fixed effects 
                  adequately captured temporal patterns.
                </Text>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Parallel Trends Validation
              </Text>
              <Text color="#64748b" mb={4}>
                For our Difference-in-Differences approach to work, we need to validate the parallel trends assumption: 
                that Thailand and control countries followed similar trends before 2023.
              </Text>
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Visual Inspection</Text>
                  <Text color="#64748b">
                    We plotted pre-treatment trends (2010-2019) for Thailand vs. control group average. The trends 
                    moved together, supporting our parallel trends assumption.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Spatial Placebo Test</Text>
                  <Text color="#64748b" mb={3}>
                    We re-estimated the model assigning a false treatment to Vietnam (a control country with similar 
                    characteristics to Thailand).
                  </Text>
                  <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0">
                    <Text fontWeight="semibold" mb={2}>Result:</Text>
                    <Text color="#64748b">
                      The coefficient for (Vietnam × Post2023) was statistically indistinguishable from zero. This 
                      supports our claim that the penalty is unique to Thailand, not a regional phenomenon.
                    </Text>
                  </Box>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Multicollinearity Check
              </Text>
              <Text color="#64748b" mb={4}>
                We calculated Variance Inflation Factors (VIF) for all regressors to ensure they weren't too highly 
                correlated with each other.
              </Text>
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0">
                <Text fontWeight="semibold" mb={2}>Result:</Text>
                <Text color="#64748b">
                  All VIF values were below 5, indicating acceptable levels of multicollinearity. The highest VIF was 
                  for GDP and exchange rate (as expected), but still within acceptable bounds.
                </Text>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Goodness of Fit
              </Text>
              <Text color="#64748b" mb={4}>
                We examined R² and adjusted R² to assess how well our model explains variation in tourist arrivals.
              </Text>
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0">
                <Text fontWeight="semibold" mb={2}>Results:</Text>
                <Text color="#64748b">
                  Within R² (variation explained within countries over time) was substantial, indicating our 
                  time-varying variables effectively explain changes in tourism flows.
                </Text>
              </Box>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'limitations' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Honest Assessment of Limitations
              </Text>
              <Text color="#64748b" mb={4}>
                Every econometric model has limitations. Being transparent about these doesn't weaken our research—it 
                strengthens it by showing we understand the boundaries of what we can claim.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                1. Endogeneity Concerns
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>The Issue:</strong> Our safety variable might be endogenous. Does low tourism cause political 
                instability, or does instability cause low tourism? The causality could run both ways.
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>What we considered:</strong>
              </Text>
              <Box as="ul" pl={6} color="#64748b" mb={3}>
                <Box as="li" mb={2}>Using lagged safety variables (t-1) to address reverse causality</Box>
                <Box as="li" mb={2}>Instrumental variable approaches (but struggled to find valid instruments)</Box>
                <Box as="li">Acknowledging this as a limitation rather than claiming perfect causality</Box>
              </Box>
              <Text color="#64748b">
                <strong>Our stance:</strong> We interpret our safety coefficient as an association, not pure causation. 
                Future research with better instruments could strengthen causal claims.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                2. Perceived vs. Objective Safety
              </Text>
              <Text color="#64748b" mb={4}>
                We use the Global Peace Index (objective safety), but what really matters is perceived safety among 
                Chinese tourists. These can diverge significantly—a country might be objectively safe but perceived as 
                dangerous due to media coverage or social media narratives.
              </Text>
              <Text color="#64748b" mb={3}>
                <strong>What we tried:</strong> We attempted to construct a "Safety Perception Score" from Dragon Trail 
                International surveys, but data availability was limited (only bi-annual reports).
              </Text>
              <Text color="#64748b">
                <strong>Future work:</strong> Sentiment analysis of Chinese social media (Weibo, Douyin) could provide 
                real-time perceived safety metrics.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                3. Unbalanced Panel
              </Text>
              <Text color="#64748b" mb={4}>
                Not all countries have complete data for all years. While Fixed Effects handles this appropriately, 
                missing data reduces our statistical power and could introduce bias if missingness is non-random.
              </Text>
              <Text color="#64748b">
                <strong>Mitigation:</strong> We checked whether missing data patterns were correlated with our outcome 
                variable and found no systematic relationship.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                4. Year Fixed Effects Absorption
              </Text>
              <Text color="#64748b" mb={4}>
                Including year fixed effects absorbs China's GDP and other time-varying factors that affect all 
                countries equally. This is intentional—we want to focus on destination-specific variation—but it means 
                we can't separately identify the effect of China's economic growth.
              </Text>
              <Text color="#64748b">
                <strong>Trade-off:</strong> We ran both specifications (with and without year FE) to show robustness. 
                The Thailand penalty persists in both.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                5. Omitted Variable Bias
              </Text>
              <Text color="#64748b" mb={4}>
                There are likely important variables we couldn't include due to data limitations:
              </Text>
              <Box as="ul" pl={6} color="#64748b" mb={4}>
                <Box as="li" mb={2}>Social media sentiment and viral content</Box>
                <Box as="li" mb={2}>Airline capacity and flight availability</Box>
                <Box as="li" mb={2}>Marketing expenditures by tourism boards</Box>
                <Box as="li">Competitor countries' promotional activities</Box>
              </Box>
              <Text color="#64748b">
                <strong>Mitigation:</strong> Country fixed effects capture time-invariant omitted variables, and year 
                fixed effects capture common shocks. But time-varying, country-specific omitted variables remain a concern.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                6. External Validity
              </Text>
              <Text color="#64748b" mb={4}>
                Our findings are specific to Chinese outbound tourism in the post-pandemic period. We should be cautious 
                about generalizing to:
              </Text>
              <Box as="ul" pl={6} color="#64748b" mb={4}>
                <Box as="li" mb={2}>Other source markets (European, American tourists)</Box>
                <Box as="li" mb={2}>Different time periods (pre-pandemic dynamics)</Box>
                <Box as="li">Other destination regions (outside our sample)</Box>
              </Box>
            </Box>

            <Box bg="#f1f5f9" p={5} borderRadius="md" border="1px" borderColor="#cbd5e1">
              <Text fontSize="lg" fontWeight="semibold" mb={3}>
                Why Our Model Still Has Value
              </Text>
              <Text color="#64748b" mb={3}>
                Despite these limitations, our model makes important contributions:
              </Text>
              <Box as="ul" pl={6} color="#64748b">
                <Box as="li" mb={2}>
                  First quantitative estimate of the "Thailand Penalty" using rigorous panel methods
                </Box>
                <Box as="li" mb={2}>
                  Controls for confounding factors that qualitative studies miss
                </Box>
                <Box as="li" mb={2}>
                  Provides actionable insights for policy despite imperfect data
                </Box>
                <Box as="li">
                  Establishes a methodological framework for future research to build upon
                </Box>
              </Box>
            </Box>
          </VStack>
        )}
      </Box>
    </Box>
  )
}
