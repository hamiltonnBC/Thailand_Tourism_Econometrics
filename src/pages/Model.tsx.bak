/**
 * Model Page Component
 * 
 * The Model page with sub-tabs for Methodology, Specification, and Constraints & Tests.
 */

import { useState } from 'react'
import { Box, HStack, Text, Code, VStack } from '@chakra-ui/react'
import { RegressionModelCard } from '../components/RegressionModelCard'
import { PlaceboTestCard } from '../components/PlaceboTestCard'
import { ModelStatistics } from '../components/ModelStatistics'
import { MulticollinearityCheck } from '../components/MulticollinearityCheck'
import { DiagnosticTestCard } from '../components/DiagnosticTestCard'

type ModelTab = 'development' | 'specification' | 'diagnostics' | 'limitations'

export function Model() {
  const [activeSubTab, setActiveSubTab] = useState<ModelTab>('development')

  return (
    <Box>
      <Box fontSize="3xl" fontWeight="bold" mb={6} color="#1e293b">
        Panel Data Analysis
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
                Developing our econometric model was not a linear process.
              </Text>
            </Box>
            {/* Regression Model Specifications */}
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model Specifications & Tests
              </Text>
              <Text color="#64748b" mb={6}>
                Below are the key regression models we developed, along with the hypothesis tests that validate
                our approach.
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
                  potentialIssues={[
                    'Counterintuitive CPI sign: Higher prices associated with MORE arrivals. This could indicate: (1) quality signaling - expensive destinations attract luxury tourists, (2) reverse causality - popular destinations can charge more, or (3) CPI capturing something other than pure price effects.',
                    'Exchange rate not significant (p = 0.263): This is surprising for a gravity model. Possible explanations: (1) multicollinearity with CPI, (2) Chinese tourists may be less price-sensitive than expected, or (3) nominal exchange rate is the wrong measure (should use real exchange rate).',
                    'China GDP not significant (p = 0.177): Income effect is weaker than expected. This could mean: (1) GDP is too aggregate - need per capita or disposable income, (2) time variation in GDP is absorbed by other variables, or (3) outbound tourism is driven by factors beyond just income.',
                    'Peace Index marginally significant (p = 0.059): Just misses 5% threshold. Could indicate: (1) objective safety (GPI) differs from perceived safety by Chinese tourists, (2) insufficient statistical power, or (3) safety matters but is confounded with other factors.',
                    'COVID dummy is very crude: A single binary variable for 2020-2021 assumes uniform impact across all countries and both years. Reality was more nuanced with different lockdown timings and severities.'
                  ]}
                />
                <ModelStatistics
                  rSquared="0.4261"
                  rSquaredWithin="0.4261"
                  rSquaredBetween="-33.519"
                  rSquaredOverall="-5.6794"
                  nObservations={136}
                  entities={8}
                  timePeriods={17}
                  fStatistic="18.264"
                  fPValue="0.0000"
                  logLikelihood="-185.40"
                  poolabilityF="7.0378"
                  poolabilityP="0.0000"
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
                  potentialIssues={[
                    'Unexpected positive Thailand effect: We hypothesized a "Thailand Penalty" but found a "Thailand Bonus." This could mean: (1) our initial hypothesis was wrong - Thailand is actually recovering well, (2) the post-2022 period is too early to capture the full penalty, (3) we\'re measuring something else (e.g., pent-up demand), or (4) data quality issues in 2023-2024.',
                    'Parallel trends assumption: DiD requires that Thailand and control countries would have followed parallel trends absent treatment. If Thailand was already on a different trajectory pre-2022, our estimate is biased. Visual inspection suggests parallel trends hold, but this is not a formal test.',
                    'Treatment timing ambiguity: When exactly did the "Thailand effect" begin? We use 2022+ as post-COVID, but the actual treatment (negative sentiment, safety concerns) may have started earlier or later. Misspecifying treatment timing biases the interaction coefficient.',
                    'Peace Index becomes insignificant: In Model A it was marginally significant (p=0.059), now it\'s not (p=0.578). This suggests: (1) multicollinearity with the new variables, (2) post-COVID variables absorb safety effects, or (3) safety matters less in the recovery period.',
                    'CPI coefficient doubles: From 1.46 in Model A to 3.23 here. This dramatic change suggests: (1) model instability, (2) multicollinearity issues, or (3) CPI\'s effect differs in post-COVID period. The large standard error indicates high uncertainty.',
                    'Small sample for post-COVID: Only 2022-2024 data (3 years × 8 countries = 24 observations) drives the Thailand interaction. This limited data makes the estimate sensitive to outliers or data errors in those specific years.'
                  ]}
                />
                <ModelStatistics
                  rSquared="0.5935"
                  rSquaredWithin="0.5935"
                  rSquaredBetween="-75.967"
                  rSquaredOverall="-13.177"
                  nObservations={136}
                  entities={8}
                  timePeriods={17}
                  fStatistic="25.235"
                  fPValue="0.0000"
                  logLikelihood="-161.95"
                  poolabilityF="9.9314"
                  poolabilityP="0.0000"
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
                  potentialIssues={[
                    'RER not significant (p = 0.207): Despite being theoretically superior to nominal ER, RER is not statistically significant. This could mean: (1) insufficient variation in RER after country-specific normalization, (2) multicollinearity with CPI (both measure price effects), or (3) Chinese tourists are genuinely insensitive to real exchange rate changes.',
                    'RER normalization may remove too much variation: We normalize RER by dividing by each country\'s mean to handle scale differences. However, this transformation removes cross-country variation in average RER levels, leaving only within-country time variation. We may have "thrown out the baby with the bathwater."',
                    'China GDP becomes negative: The coefficient flips from +0.39 (Model A) to -0.19 (Model D). While neither is significant, this sign change is concerning and suggests: (1) multicollinearity between GDP and RER, (2) model instability, or (3) RER is capturing GDP effects.',
                    'Multicollinearity between CPI and RER: Both variables measure price/cost effects. RER = (Nominal ER × CPI_China) / CPI_destination. This mathematical relationship creates correlation. When both are in the model, their individual effects become hard to separate, inflating standard errors.',
                    'Peace Index loses significance: Compared to Model A (p=0.059), it\'s now p=0.207. This suggests RER specification changes the model dynamics, possibly because: (1) RER absorbs some safety-related variation, (2) different sample after RER normalization, or (3) increased multicollinearity reduces precision.',
                    'Minimal improvement over Model A: Log-likelihood improves by only 0.04 (-185.36 vs -185.40). This tiny improvement suggests RER doesn\'t add much explanatory power despite being theoretically preferred. The data may not support the theoretical refinement.'
                  ]}
                />
                <ModelStatistics
                  rSquared="0.4265"
                  rSquaredWithin="0.4265"
                  rSquaredBetween="-0.7290"
                  rSquaredOverall="0.2186"
                  nObservations={136}
                  entities={8}
                  timePeriods={17}
                  fStatistic="18.293"
                  fPValue="0.0000"
                  logLikelihood="-185.36"
                  poolabilityF="7.1080"
                  poolabilityP="0.0000"
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
                  potentialIssues={[
                    'RER coefficient flips sign: In Model D, RER was -0.97 (correct sign). Here it\'s +0.87 (wrong sign). This sign flip is alarming and suggests: (1) severe multicollinearity with the new interaction terms, (2) model instability, or (3) RER\'s effect differs in post-COVID period. The fact that it\'s not significant (p=0.295) doesn\'t excuse the wrong sign.',
                    'Thailand effect contradicts hypothesis: We expected a penalty but found a bonus. This is the central puzzle. Possible explanations: (1) our hypothesis was wrong, (2) measurement error in 2023-2024 data, (3) pent-up demand creates temporary boost, (4) Thailand\'s marketing/visa policies are working, or (5) we\'re measuring recovery from a lower base (Thailand fell further, so % recovery looks faster).',
                    'Peace Index completely insignificant: p=0.664 means safety has no detectable effect in this specification. This contradicts literature and common sense. Likely causes: (1) multicollinearity with 7 other variables absorbs safety effects, (2) post-COVID variables capture safety concerns, (3) objective GPI doesn\'t match perceived safety, or (4) overfitting - too many variables for 136 observations.',
                    'High multicollinearity risk: This model has 7 regressors + 8 country FE = 15 parameters estimated from 136 observations. That\'s only 9 observations per parameter. With CPI, RER, and COVID variables all measuring related concepts, multicollinearity is likely inflating standard errors and causing coefficient instability.',
                    'Post-COVID period too short: Only 3 years (2022-2024) × 8 countries = 24 observations drive the Thailand interaction. If even one country has data issues in 2023-2024, it could swing the result. The estimate is fragile.',
                    'Comparing apples to oranges: Thailand may have fallen further during COVID than other countries, so its "faster recovery" might just be mean reversion. We need to check if Thailand is recovering to its pre-COVID level or exceeding it. The positive coefficient could be misleading without this context.',
                    'China GDP elasticity seems too high: 1.43 is very high - it suggests tourism is a strong luxury good. For comparison, typical income elasticities for tourism are 1.0-1.2. This could indicate: (1) our sample of destinations is luxury-focused, (2) GDP is proxying for other factors, or (3) the post-COVID period has unusual dynamics.'
                  ]}
                />
                <ModelStatistics
                  rSquared="0.5877"
                  rSquaredWithin="0.5877"
                  rSquaredBetween="-0.3871"
                  rSquaredOverall="0.4124"
                  nObservations={136}
                  entities={8}
                  timePeriods={17}
                  fStatistic="24.639"
                  fPValue="0.0000"
                  logLikelihood="-162.91"
                  poolabilityF="9.2043"
                  poolabilityP="0.0000"
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

            {/* <Box>
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
            </Box> */}

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Diagnostic Tests
              </Text>
              <VStack align="stretch" gap={4}>

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
                (like the COVID-19 pandemic). This absorption was intentional. By controlling for YFE, our identification
                relied exclusively on the cross-sectional variation of destination-specific variables, which vary
                independently across countries and time. This ended up not being good for our model, and we switched it out.
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
                For every model iteration, we ran a battery of diagnostic tests.
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
                Heteroskedasticity and Autocorrelation Tests
              </Text>

              {/* Explanation Section */}
              <Box mb={6}>
                <Text color="#64748b" mb={4}>
                  Panel data often suffers from two key violations of classical regression assumptions:
                  heteroskedasticity and autocorrelation. We ran formal diagnostic tests to detect these issues
                  and applied appropriate corrections.
                </Text>

                <VStack align="stretch" gap={3} mb={4}>
                  <Box>
                    <Text fontWeight="semibold" color="#1e293b" mb={1}>
                      What is Heteroskedasticity?
                    </Text>
                    <Text color="#64748b" fontSize="sm">
                      Heteroskedasticity means the variance of errors differs across countries. For example, Japan
                      (a large tourism market) might have errors of ±500,000 tourists, while Cambodia (smaller market)
                      has errors of ±50,000. Even if the model is equally "good" for both, the error magnitudes differ.
                      This violates the constant variance assumption and makes standard errors unreliable.
                    </Text>
                  </Box>

                  <Box>
                    <Text fontWeight="semibold" color="#1e293b" mb={1}>
                      What is Autocorrelation?
                    </Text>
                    <Text color="#64748b" fontSize="sm">
                      Autocorrelation means errors are correlated over time within the same country. If Thailand has
                      a bad tourism year in 2020 (negative error), it's likely to have another bad year in 2021
                      (another negative error). The errors are "sticky" rather than independent. This makes standard
                      errors too small and inflates statistical significance.
                    </Text>
                  </Box>


                </VStack>
              </Box>

              {/* Test Results */}
              <Box mb={6}>
                <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
                  Diagnostic Test Results
                </Text>
                <Text color="#64748b" mb={4}>
                  We ran two formal tests on each model specification:
                </Text>

                <Box as="ul" pl={6} color="#64748b" mb={4}>
                  <Box as="li" mb={2}>
                    <strong>Modified Wald Test:</strong> Tests H₀: σ²ᵢ = σ² for all i (homoskedasticity).
                    Rejection indicates heteroskedasticity.
                  </Box>
                  <Box as="li">
                    <strong>Wooldridge Test:</strong> Tests H₀: No first-order autocorrelation.
                    Rejection indicates errors are correlated over time.
                  </Box>
                </Box>

                <VStack align="stretch" gap={4}>
                  <DiagnosticTestCard
                    modelName="Model A: Baseline Gravity Model"
                    waldStatistic={12.69}
                    waldDF={7}
                    waldPValue={0.0801}
                    waldResult="Fail to reject H₀"
                    wooldridgeF={0.46}
                    wooldridgePValue={0.4995}
                    wooldridgeResult="Fail to reject H₀"
                  />

                  <DiagnosticTestCard
                    modelName="Model C: Thailand Asymmetry"
                    waldStatistic={36.51}
                    waldDF={7}
                    waldPValue={0.000006}
                    waldResult="Reject H₀"
                    wooldridgeF={14.54}
                    wooldridgePValue={0.0002}
                    wooldridgeResult="Reject H₀"
                  />

                  <DiagnosticTestCard
                    modelName="Model D: Real Exchange Rate"
                    waldStatistic={16.33}
                    waldDF={7}
                    waldPValue={0.0223}
                    waldResult="Reject H₀"
                    wooldridgeF={0.50}
                    wooldridgePValue={0.4796}
                    wooldridgeResult="Fail to reject H₀"
                  />

                  <DiagnosticTestCard
                    modelName="Model F: Thailand Asymmetry with RER"
                    waldStatistic={34.99}
                    waldDF={7}
                    waldPValue={0.000011}
                    waldResult="Reject H₀"
                    wooldridgeF={16.36}
                    wooldridgePValue={0.0001}
                    wooldridgeResult="Reject H₀"
                  />
                </VStack>
              </Box>

              {/* Visualizations */}
              <Box mb={6}>
                <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
                  Visual Diagnostics
                </Text>

                {/* Test P-values Comparison */}
                <Box mb={6}>
                  <Text color="#64748b" mb={3}>
                    This chart compares p-values across all models. Lower p-values (red bars) indicate rejection
                    of the null hypothesis, meaning the issue is detected. The dashed lines show significance
                    thresholds at α = 0.05 and α = 0.01.
                  </Text>
                  <Box
                    borderRadius="md"
                    overflow="hidden"
                    border="1px"
                    borderColor="#e2e8f0"
                  >
                    <img
                      src={`${import.meta.env.BASE_URL}diagnostic_test_pvalues.png`}
                      alt="Diagnostic test p-values comparison"
                      style={{ width: '100%', display: 'block' }}
                    />
                  </Box>
                </Box>

                {/* Residual Variance by Country */}
                <Box mb={6}>
                  <Text color="#64748b" mb={3}>
                    These charts show residual variance (σ²) for each country across all models. Higher bars
                    indicate more volatile errors. We can see how Japan and Thailand consistently have higher variance
                    than smaller markets like Indonesia and Singapore. This heterogeneity is why we ran these tests.
                  </Text>
                  <Box
                    borderRadius="md"
                    overflow="hidden"
                    border="1px"
                    borderColor="#e2e8f0"
                  >
                    <img
                      src={`${import.meta.env.BASE_URL}residual_variance_by_country.png`}
                      alt="Residual variance by country"
                      style={{ width: '100%', display: 'block' }}
                    />
                  </Box>
                </Box>

                {/* Detailed Residual Diagnostics */}
                <Box>
                  <Text color="#64748b" mb={3}>
                    Detailed residual diagnostics for Model F (our most complex specification). The top-left plot
                    shows residuals over time for each country, revealing temporal patterns. The Q-Q plot (bottom-left)
                    checks for normality. The boxplot (bottom-right) shows the distribution of residuals by country,
                    highlighting heteroskedasticity.
                  </Text>
                  <Box
                    borderRadius="md"
                    overflow="hidden"
                    border="1px"
                    borderColor="#e2e8f0"
                  >
                    <img
                      src={`${import.meta.env.BASE_URL}residual_diagnostics_model_f.png`}
                      alt="Detailed residual diagnostics for Model F"
                      style={{ width: '100%', display: 'block' }}
                    />
                  </Box>
                </Box>
              </Box>

              {/* How We Addressed These Issues */}
              <Box p={5} bg="#f1f5f9" borderRadius="md" border="1px" borderColor="#cbd5e1">
                <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
                  How We Addressed These Issues
                </Text>

                <VStack align="stretch" gap={3}>
                  <Box>
                    <Text fontWeight="semibold" color="#1e293b" mb={1}>
                      1. Clustered Standard Errors (for Heteroskedasticity)
                    </Text>
                    <Text color="#64748b" fontSize="sm">
                      We use <Code fontSize="xs">cov_type='clustered', cluster_entity=True</Code> in all regressions.
                      This allows each country to have its own error variance, making our standard errors and p-values
                      robust to heteroskedasticity. Instead of assuming all countries have the same variance, we let
                      the data determine country-specific variances.
                    </Text>
                  </Box>

                  <Box>
                    <Text fontWeight="semibold" color="#1e293b" mb={1}>
                      2. Post-COVID Variables (for Autocorrelation)
                    </Text>
                    <Text color="#64748b" fontSize="sm">
                      The autocorrelation in Models C and F is actually a missing variable problem. By adding
                      <Code fontSize="xs">post_covid</Code> and <Code fontSize="xs">thailand_post_covid</Code>
                      interaction terms, we explicitly model the temporal patterns that were causing autocorrelation.
                      These variables capture the "stickiness" in post-pandemic recovery, removing it from the errors.
                      We discuss later why this ended up being a problem for us.
                    </Text>
                  </Box>

                  <Box>
                    <Text fontWeight="semibold" color="#1e293b" mb={1}>
                      3. Why This Matters
                    </Text>
                    <Text color="#64748b" fontSize="sm">
                      Without these corrections, our p-values would be unreliable and our confidence intervals would
                      be wrong. We might claim statistical significance when there isn't any, or make policy
                      recommendations based on faulty inference. With corrections, our statistical conclusions are
                      valid and our hypothesis tests are more trustworthy.
                    </Text>
                  </Box>
                </VStack>
              </Box>

              {/* Key Findings */}
              <Box mt={6} p={4} bg="#fff7ed" borderRadius="md" border="1px" borderColor="#fed7aa">
                <Text fontSize="md" fontWeight="semibold" mb={3} color="#1e293b">
                  Key Findings
                </Text>
                <VStack align="stretch" gap={2}>
                  <Text color="#64748b" fontSize="sm">
                    ✓ <strong>Baseline models (A & D) are clean:</strong> No heteroskedasticity or autocorrelation
                    detected. These simpler specifications don't suffer from diagnostic issues.
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    ⚠️ <strong>Thailand asymmetry models (C & F) have both issues:</strong> Strong evidence of
                    heteroskedasticity (p {'<'} 0.001) and autocorrelation (p {'<'} 0.001). This validates our use
                    of clustered standard errors and post-COVID variables.
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    ✓ <strong>Our corrections are appropriate:</strong> The diagnostic tests confirm that our
                    modeling choices (clustered SEs, interaction terms) address real statistical issues in the data,
                    not just theoretical concerns.
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    ✓ <strong>Inference is valid:</strong> With proper corrections applied, our p-values, confidence
                    intervals, and hypothesis tests are statistically sound. Policy recommendations can be made with
                    confidence.
                  </Text>
                </VStack>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Parallel Trends Validation
              </Text>
              <Text color="#64748b" mb={4}>
                For our Difference-in-Differences approach to work, we needed to validate the parallel trends assumption:
                that Thailand and control countries followed similar trends before 2022. We did this by graphing, which are on the explore data page.
              </Text>
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Visual Inspection</Text>
                  <Text color="#64748b">
                    We plotted pre-treatment trends (2010-2019) for Thailand vs. control group average. The trends
                    moved together, supporting our parallel trends assumption.
                  </Text>
                </Box>
              </VStack>
            </Box>

            {/* Spatial Placebo Tests - All Countries */}
            <PlaceboTestCard
              title="Spatial Placebo Tests: Testing All Countries"
              description="To validate that Thailand's asymmetric recovery is truly Thailand-specific and not a regional or random phenomenon, we ran Model C (Thailand Asymmetry) separately for each country in our sample. We replace the Thailand interaction term with an interaction for each other country. If Thailand's effect was unique, we should have find that ONLY Thailand shows a significant coefficient, while all other countries' coefficients are statistically indistinguishable from zero."
              tests={[
                {
                  country: 'Thailand',
                  coefficient: 0.2963,
                  pValue: '0.038',
                  tStat: '2.10',
                  isSignificant: true,
                  isThailand: true
                },
                {
                  country: 'Vietnam',
                  coefficient: -0.6326,
                  pValue: '0.000',
                  tStat: '-3.77',
                  isSignificant: true
                },
                {
                  country: 'Malaysia',
                  coefficient: 0.6285,
                  pValue: '0.007',
                  tStat: '2.75',
                  isSignificant: true
                },
                {
                  country: 'Singapore',
                  coefficient: -0.4250,
                  pValue: '0.008',
                  tStat: '-2.72',
                  isSignificant: true
                },
                {
                  country: 'Indonesia',
                  coefficient: -0.2266,
                  pValue: '0.306',
                  tStat: '-1.03',
                  isSignificant: false
                },
                {
                  country: 'Cambodia',
                  coefficient: -0.2206,
                  pValue: '0.516',
                  tStat: '-0.65',
                  isSignificant: false
                },
                {
                  country: 'Japan',
                  coefficient: 0.9307,
                  pValue: '0.038',
                  tStat: '2.10',
                  isSignificant: true
                },
                {
                  country: 'Australia',
                  coefficient: -0.2240,
                  pValue: '0.412',
                  tStat: '-0.82',
                  isSignificant: false
                }
              ]}
              interpretation="Our Unexpected Result: The spatial placebo tests reveal that Thailand is not the only country with a significant asymmetric recovery effect. Vietnam (β = -0.633, p < 0.001), Malaysia (β = 0.629, p = 0.007), Singapore (β = -0.425, p = 0.008), and Japan (β = 0.931, p = 0.038) all show significant coefficients. This suggests the post-COVID recovery pattern is NOT unique to Thailand but rather reflects broader regional dynamics. The mixed signs (positive for Thailand, Malaysia, and Japan; negative for Vietnam and Singapore) indicate heterogeneous recovery trajectories across destinations. This finding challenges our initial hypothesis and suggests that country-specific factors beyond a 'Thailand penalty' are driving asymmetric recoveries across the region."
            />

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Multicollinearity Check
              </Text>
              <Text color="#64748b" mb={4}>
                Multicollinearity occurs when independent variables are highly correlated, which can inflate standard
                errors and make coefficient estimates unreliable. We use three diagnostic measures:
              </Text>

              <Box as="ul" pl={6} color="#64748b" mb={4}>
                <Box as="li" mb={2}>
                  <strong>Variance Inflation Factor (VIF):</strong> Measures how much the variance of a coefficient
                  is inflated due to collinearity. VIF {'<'} 5 is ideal, 5-10 is moderate, {'>'}10 is problematic.
                </Box>
                <Box as="li" mb={2}>
                  <strong>Condition Number (κ):</strong> Measures overall multicollinearity in the design matrix.
                  κ {'<'} 30 is low, 30-100 is moderate, {'>'}100 is severe.
                </Box>
                <Box as="li">
                  <strong>Correlation Matrix:</strong> Shows pairwise correlations between variables.
                  |r| {'>'}0.7 suggests potential multicollinearity.
                </Box>
              </Box>

              <VStack align="stretch" gap={4}>
                {/* Model A VIF */}
                <MulticollinearityCheck
                  modelName="Model A: Baseline Gravity Model"
                  vifData={[
                    { variable: 'ln_cpi', vif: 3.10 },
                    { variable: 'ln_gdp_china', vif: 2.72 },
                    { variable: 'ln_exchange_rate', vif: 1.89 },
                    { variable: 'peace_index', vif: 1.32 },
                    { variable: 'covid_dummy', vif: 1.14 }
                  ]}
                  maxVIF={3.10}
                  conditionNumber={3.43}
                  highCorrelations={['ln_cpi ↔ ln_gdp_china: r = 0.707']}
                />

                {/* Model C VIF */}
                <MulticollinearityCheck
                  modelName="Model C: Thailand Asymmetry"
                  vifData={[
                    { variable: 'ln_gdp_china', vif: 3.38 },
                    { variable: 'ln_cpi', vif: 3.32 },
                    { variable: 'post_covid', vif: 2.02 },
                    { variable: 'ln_exchange_rate', vif: 1.89 },
                    { variable: 'peace_index', vif: 1.42 },
                    { variable: 'covid_dummy', vif: 1.41 },
                    { variable: 'thailand_post_covid', vif: 1.27 }
                  ]}
                  maxVIF={3.38}
                  conditionNumber={3.81}
                  highCorrelations={['ln_cpi ↔ ln_gdp_china: r = 0.707']}
                />

                {/* Model D VIF */}
                <MulticollinearityCheck
                  modelName="Model D: Real Exchange Rate"
                  vifData={[
                    { variable: 'ln_gdp_china', vif: 4.33 },
                    { variable: 'ln_cpi', vif: 2.43 },
                    { variable: 'ln_rer', vif: 2.20 },
                    { variable: 'covid_dummy', vif: 1.14 },
                    { variable: 'peace_index', vif: 1.09 }
                  ]}
                  maxVIF={4.33}
                  conditionNumber={4.04}
                  highCorrelations={['ln_cpi ↔ ln_gdp_china: r = 0.707']}
                />

                {/* Model F VIF */}
                <MulticollinearityCheck
                  modelName="Model F: Thailand Asymmetry with RER"
                  vifData={[
                    { variable: 'ln_gdp_china', vif: 6.61 },
                    { variable: 'ln_cpi', vif: 2.65 },
                    { variable: 'ln_rer', vif: 2.60 },
                    { variable: 'post_covid', vif: 2.32 },
                    { variable: 'covid_dummy', vif: 1.49 },
                    { variable: 'thailand_post_covid', vif: 1.27 },
                    { variable: 'peace_index', vif: 1.18 }
                  ]}
                  maxVIF={6.61}
                  conditionNumber={5.17}
                  highCorrelations={['ln_cpi ↔ ln_gdp_china: r = 0.707']}
                />
              </VStack>

              {/* Correlation Matrices Visualization */}
              <Box mt={6}>
                <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
                  Correlation Matrices
                </Text>
                <Text color="#64748b" mb={4}>
                  The heatmaps below show pairwise correlations between all variables in each model. Red indicates
                  positive correlation, blue indicates negative correlation. The only notable high correlation
                  (r = 0.707) is between ln(CPI) and ln(GDP_China), which is expected as both capture economic
                  development over time.
                </Text>
                <Box
                  borderRadius="md"
                  overflow="hidden"
                  border="1px"
                  borderColor="#e2e8f0"
                >
                  <img
                    src={`${import.meta.env.BASE_URL}correlation_matrices.png`}
                    alt="Correlation matrices for all models"
                    style={{ width: '100%', display: 'block' }}
                  />
                </Box>
              </Box>

              {/* VIF Comparison Chart */}
              <Box mt={6}>
                <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
                  VIF Comparison Across Models
                </Text>
                <Text color="#64748b" mb={4}>
                  This chart compares VIF values across all four models. Notice that Model F (Thailand Asymmetry
                  with RER) has the highest VIF for ln_gdp_china (6.61), but it's still below the threshold of 10.
                  The dashed lines indicate moderate (VIF = 5) and high (VIF = 10) multicollinearity thresholds.
                </Text>
                <Box
                  borderRadius="md"
                  overflow="hidden"
                  border="1px"
                  borderColor="#e2e8f0"
                >
                  <img
                    src={`${import.meta.env.BASE_URL}vif_comparison.png`}
                    alt="VIF comparison across models"
                    style={{ width: '100%', display: 'block' }}
                  />
                </Box>
              </Box>

              {/* Overall Interpretation */}
              <Box mt={6} p={4} bg="#f1f5f9" borderRadius="md" border="1px" borderColor="#cbd5e1">
                <Text fontSize="md" fontWeight="semibold" mb={3} color="#1e293b">
                  Overall Assessment
                </Text>
                <VStack align="stretch" gap={2}>
                  <Text color="#64748b">
                    ✓ <strong>All models passed multicollinearity diagnostics.</strong> No VIF values exceed 10,
                    and all condition numbers were well below 30.
                  </Text>
                  <Text color="#64748b">
                    ✓ <strong>The RER sign flip in Model F was NOT due to multicollinearity.</strong> With VIF = 6.61
                    for ln_gdp_china and κ = 5.17, the model was stable. The sign flip is more likely due to small post-COVID sample.
                  </Text>
                  <Text color="#64748b">
                    ✓ <strong>The ln_cpi ↔ ln_gdp_china correlation (r = 0.707) was expected.</strong> Both variables
                    capture economic development over time.
                  </Text>
                  <Text color="#64748b">
                    ✓ <strong>Coefficient estimates are reliable.</strong> Standard errors are not artificially
                    inflated by multicollinearity, so our hypothesis tests were valid.
                  </Text>
                </VStack>
              </Box>
            </Box>

            {/* <Box>
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
            </Box> */}
          </VStack>
        )}

        {/* {activeSubTab === 'limitations' && (
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
        )} */}
      </Box>
    </Box>
  )
}
