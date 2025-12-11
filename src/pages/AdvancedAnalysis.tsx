/**
 * Time Series Analysis Page Component
 * 
 * Thailand-specific time series analysis with ADL model and competitive analysis.
 */

import { useState } from 'react'
import { Box, HStack, Text, VStack, Code } from '@chakra-ui/react'

type AnalysisTab = 'overview' | 'timeseries' | 'adl' | 'competitive'

export function AdvancedAnalysis() {
  const [activeSubTab, setActiveSubTab] = useState<AnalysisTab>('overview')

  return (
    <Box>
      <Box fontSize="3xl" fontWeight="bold" mb={6} color="#1e293b">
        Time Series Analysis: Thailand Focus
      </Box>

      {/* Sub-navigation tabs */}
      <HStack gap={2} mb={8} borderBottom="2px" borderColor="#e2e8f0" pb={0}>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'overview' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'overview' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'overview' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('overview')}
        >
          Overview & Data
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'timeseries' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'timeseries' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'timeseries' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('timeseries')}
        >
          Time Series Model
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'adl' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'adl' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'adl' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('adl')}
        >
          ADL Model
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'competitive' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'competitive' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'competitive' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('competitive')}
        >
          Competitive Analysis
        </Box>
      </HStack>

      {/* Content area */}
      <Box color="#1e293b" lineHeight="1.8">
        {activeSubTab === 'overview' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Executive Summary
              </Text>
              <Text color="#64748b" mb={4}>
                This report presents a robust econometric analysis of the determinants of Chinese tourist arrivals 
                in Thailand. Using a 25-year time series dataset (2000-2024), we identify the key drivers of demand 
                and quantify the sensitivity of tourism flows to economic factors.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Key Findings
              </Text>
              <VStack align="stretch" gap={3} pl={4}>
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={1}>
                    1. Price Sensitivity
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    Thailand's tourism demand is highly elastic to price changes in the long run. A 1% appreciation 
                    of the Real Exchange Rate (RER) leads to a <strong>3.07% decrease</strong> in arrivals over time.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={1}>
                    2. Income Driver
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    Chinese GDP is a strong positive driver, with a 1% increase in GDP leading to a <strong>0.67% increase</strong> in arrivals.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={1}>
                    3. Habit Persistence
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    There is significant "habit persistence" (32%), meaning past visits strongly influence future demand.
                  </Text>
                </Box>
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={1}>
                    4. Competitive Landscape
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    Thailand competes closely with Indonesia on price, while Vietnam and Malaysia show less sensitivity 
                    to exchange rate fluctuations.
                  </Text>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Data Overview (2000-2024)
              </Text>
              <Text color="#64748b" mb={4}>
                The analysis utilizes a curated dataset covering 25 years of Chinese tourism to Thailand.
              </Text>
              
              <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Text fontWeight="semibold" mb={3}>Key Variables:</Text>
                <VStack align="stretch" gap={2}>
                  <Text color="#64748b" fontSize="sm">
                    <strong>Dependent Variable:</strong> Log of Chinese Tourist Arrivals (ln(Arrivals))
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    <strong>Income Variable:</strong> Log of China's GDP (ln(GDP_China))
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    <strong>Price Variable:</strong> Log of Real Exchange Rate (ln(RER))
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    <strong>Control Variables:</strong> COVID-19 Dummy (2020-2022)
                  </Text>
                </VStack>
              </Box>

              <Text color="#64748b" mb={4}>
                <em>Note: RER accounts for both nominal exchange rates and relative inflation (CPI).</em>
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Data Visualizations
              </Text>
              <Text color="#64748b" mb={4}>
                The correlation matrix confirms strong relationships between the key variables, justifying their 
                inclusion in the model. The trend analysis shows how closely tourist arrivals track Chinese 
                economic growth (GDP), interrupted only by the massive shock of COVID-19.
              </Text>
              
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" mb={2}>Correlation Matrix</Text>
                  <Box 
                    borderRadius="md" 
                    overflow="hidden" 
                    border="1px" 
                    borderColor="#e2e8f0"
                  >
                    <img 
                      src={`${import.meta.env.BASE_URL}thailand_correlation_matrix.png`}
                      alt="Thailand correlation matrix"
                      style={{ width: '100%', display: 'block' }}
                    />
                  </Box>
                </Box>
                
                <Box>
                  <Text fontWeight="semibold" mb={2}>GDP vs Arrivals Trends</Text>
                  <Box 
                    borderRadius="md" 
                    overflow="hidden" 
                    border="1px" 
                    borderColor="#e2e8f0"
                  >
                    <img 
                      src={`${import.meta.env.BASE_URL}thailand_trends_gdp.png`}
                      alt="Thailand trends GDP vs arrivals"
                      style={{ width: '100%', display: 'block' }}
                    />
                  </Box>
                </Box>
              </VStack>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'timeseries' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model 1: Thailand Time Series Analysis
              </Text>
              <Text color="#64748b" mb={4}>
                <strong>Objective:</strong> To estimate the short-run price and income elasticities of demand for Thailand specifically.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Methodology
              </Text>
              <Text color="#64748b" mb={4}>
                We employ an <strong>Ordinary Least Squares (OLS)</strong> regression with <strong>HAC 
                (Heteroscedasticity and Autocorrelation Consistent)</strong> standard errors to correct for 
                potential serial correlation and heteroscedasticity detected in diagnostic tests.
              </Text>
              
              <Box bg="#f8fafc" p={6} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Text fontWeight="semibold" mb={3}>Regression Equation:</Text>
                <Code fontSize="md" colorScheme="gray" display="block" whiteSpace="pre-wrap">
                  ln(Arrivals_t) = α + β₁ ln(GDP_China,t) + β₂ ln(RER_t) + β₃ COVID_t + ε_t
                </Code>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Results
              </Text>
              <Box
                border="1px"
                borderColor="#e2e8f0"
                borderRadius="md"
                overflow="hidden"
              >
                {/* Table Header */}
                <HStack 
                  bg="#f1f5f9" 
                  p={3}
                  borderBottom="1px"
                  borderColor="#e2e8f0"
                  fontSize="sm"
                  fontWeight="semibold"
                  color="#64748b"
                >
                  <Box flex="2">Variable</Box>
                  <Box flex="1" textAlign="center">Coefficient</Box>
                  <Box flex="1" textAlign="center">Std. Error</Box>
                  <Box flex="1" textAlign="center">P-Value</Box>
                  <Box flex="3">Interpretation</Box>
                </HStack>

                {/* Table Rows */}
                <VStack align="stretch" gap={0}>
                  <HStack 
                    p={3}
                    borderBottom="1px"
                    borderColor="#f1f5f9"
                    fontSize="sm"
                    _hover={{ bg: "#f8fafc" }}
                  >
                    <Box flex="2" fontWeight="semibold">Log(GDP China)</Box>
                    <Box flex="1" textAlign="center" fontWeight="semibold" color="green.600">0.67</Box>
                    <Box flex="1" textAlign="center">0.21</Box>
                    <Box flex="1" textAlign="center" fontWeight="semibold" color="green.600">0.001</Box>
                    <Box flex="3">Income Elasticity: +0.67% arrivals for +1% GDP</Box>
                  </HStack>
                  
                  <HStack 
                    p={3}
                    borderBottom="1px"
                    borderColor="#f1f5f9"
                    fontSize="sm"
                    _hover={{ bg: "#f8fafc" }}
                  >
                    <Box flex="2" fontWeight="semibold">Log(RER)</Box>
                    <Box flex="1" textAlign="center" fontWeight="semibold" color="red.600">-2.33</Box>
                    <Box flex="1" textAlign="center">1.10</Box>
                    <Box flex="1" textAlign="center" fontWeight="semibold" color="green.600">0.034</Box>
                    <Box flex="3">Price Elasticity: -2.33% arrivals for +1% Price (Appreciation)</Box>
                  </HStack>
                  
                  <HStack 
                    p={3}
                    fontSize="sm"
                    _hover={{ bg: "#f8fafc" }}
                  >
                    <Box flex="2" fontWeight="semibold">COVID Dummy</Box>
                    <Box flex="1" textAlign="center" fontWeight="semibold" color="red.600">-3.57</Box>
                    <Box flex="1" textAlign="center">0.72</Box>
                    <Box flex="1" textAlign="center" fontWeight="semibold" color="green.600">0.000</Box>
                    <Box flex="3">Pandemic Shock: ~97% drop in arrivals</Box>
                  </HStack>
                </VStack>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Model Fit
              </Text>
              <Text color="#64748b" mb={4}>
                The model explains <strong>72.5%</strong> of the variation in tourist arrivals (R² = 0.725). 
                The predicted values track the actual data very closely, capturing both the pre-2010 trends 
                and the post-2010 boom.
              </Text>
              
              <Box>
                <Text fontWeight="semibold" mb={2}>Actual vs Predicted Values</Text>
                <Box 
                  borderRadius="md" 
                  overflow="hidden" 
                  border="1px" 
                  borderColor="#e2e8f0"
                >
                  <img 
                    src={`${import.meta.env.BASE_URL}model1_actual_vs_predicted.png`}
                    alt="Model 1 actual vs predicted"
                    style={{ width: '100%', display: 'block' }}
                  />
                </Box>
              </Box>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'adl' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Advanced Model: Habit Persistence (ADL)
              </Text>
              <Text color="#64748b" mb={4}>
                <strong>Objective:</strong> To distinguish between short-run and long-run effects by accounting 
                for "habit persistence" (tourists returning to a familiar destination).
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Methodology
              </Text>
              <Text color="#64748b" mb={4}>
                We estimate an <strong>Autoregressive Distributed Lag (ADL(1,0))</strong> model by including 
                the lagged dependent variable (ln(Arrivals_{'{'}t-1{'}'})).
              </Text>
              
              <Box bg="#f8fafc" p={6} borderRadius="md" border="1px" borderColor="#e2e8f0" mb={4}>
                <Text fontWeight="semibold" mb={3}>Regression Equation:</Text>
                <Code fontSize="md" colorScheme="gray" display="block" whiteSpace="pre-wrap">
                  ln(Arrivals_t) = α + ρ ln(Arrivals_{'{'}t-1{'}'}) + β₁ ln(GDP_China,t) + β₂ ln(RER_t) + ...
                </Code>
              </Box>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Key Results
              </Text>
              <VStack align="stretch" gap={4}>
                <Box p={4} bg="#f1f5f9" borderRadius="md" border="1px" borderColor="#cbd5e1">
                  <Text fontWeight="semibold" mb={2} color="#1e293b">
                    Habit Persistence (ρ): 0.32 (p = 0.05)
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    This indicates that <strong>32%</strong> of the previous year's tourism volume "carries over" 
                    to the current year, reflecting strong destination loyalty or inertia.
                  </Text>
                </Box>

                <Box p={4} bg="#fff7ed" borderRadius="md" border="1px" borderColor="#fed7aa">
                  <Text fontWeight="semibold" mb={2} color="#1e293b">
                    Long-Run Price Elasticity: -3.07
                  </Text>
                  <Text color="#64748b" fontSize="sm" mb={2}>
                    <strong>Calculation:</strong> β_LR = β_SR / (1 - ρ) = -2.08 / (1 - 0.32) = -3.07
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    <strong>Insight:</strong> The negative impact of a price increase (e.g., Baht appreciation) 
                    is <strong>amplified over time</strong>. In the short run, tourists may still come due to 
                    pre-booked plans, but in the long run, they switch to cheaper destinations.
                  </Text>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Short-Run vs Long-Run Effects
              </Text>
              <Box
                border="1px"
                borderColor="#e2e8f0"
                borderRadius="md"
                overflow="hidden"
              >
                {/* Table Header */}
                <HStack 
                  bg="#f1f5f9" 
                  p={3}
                  borderBottom="1px"
                  borderColor="#e2e8f0"
                  fontSize="sm"
                  fontWeight="semibold"
                  color="#64748b"
                >
                  <Box flex="2">Effect Type</Box>
                  <Box flex="2" textAlign="center">Price Elasticity</Box>
                  <Box flex="2" textAlign="center">Income Elasticity</Box>
                  <Box flex="3">Interpretation</Box>
                </HStack>

                {/* Table Rows */}
                <VStack align="stretch" gap={0}>
                  <HStack 
                    p={3}
                    borderBottom="1px"
                    borderColor="#f1f5f9"
                    fontSize="sm"
                    _hover={{ bg: "#f8fafc" }}
                  >
                    <Box flex="2" fontWeight="semibold">Short-Run</Box>
                    <Box flex="2" textAlign="center" color="red.600">-2.08</Box>
                    <Box flex="2" textAlign="center" color="green.600">+0.67</Box>
                    <Box flex="3">Immediate response to price/income changes</Box>
                  </HStack>
                  
                  <HStack 
                    p={3}
                    fontSize="sm"
                    _hover={{ bg: "#f8fafc" }}
                  >
                    <Box flex="2" fontWeight="semibold">Long-Run</Box>
                    <Box flex="2" textAlign="center" color="red.600">-3.07</Box>
                    <Box flex="2" textAlign="center" color="green.600">+0.99</Box>
                    <Box flex="3">Full adjustment after habit persistence effects</Box>
                  </HStack>
                </VStack>
              </Box>
            </Box>

            <Box p={4} bg="#f0f9ff" borderRadius="md" border="1px" borderColor="#bae6fd">
              <Text fontSize="md" fontWeight="semibold" mb={3} color="#1e293b">
                Economic Interpretation
              </Text>
              <Text color="#64748b" fontSize="sm">
                The ADL model reveals that Thailand's tourism market exhibits significant <strong>habit persistence</strong>. 
                This means that policy interventions (like exchange rate management or marketing campaigns) have 
                <strong>cumulative effects</strong> that build over time. A temporary price advantage doesn't just 
                boost arrivals in the current year—it creates a base of repeat visitors who are likely to return, 
                amplifying the long-term benefits.
              </Text>
            </Box>
          </VStack>
        )}

        {activeSubTab === 'competitive' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model 2: Competitive Analysis Panel
              </Text>
              <Text color="#64748b" mb={4}>
                <strong>Objective:</strong> To compare Thailand's recovery and price sensitivity against key 
                regional competitors (Vietnam, Malaysia, Indonesia).
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Methodology
              </Text>
              <Text color="#64748b" mb={4}>
                We use a <strong>Panel Fixed Effects</strong> model covering the period <strong>2008-2024</strong> 
                to compare price elasticities across destinations.
              </Text>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Comparative Price Elasticity
              </Text>
              <Text color="#64748b" mb={4}>
                We estimated the price elasticity for each country individually to see how they compare in terms 
                of price sensitivity.
              </Text>
              
              <Box mb={6}>
                <Box 
                  borderRadius="md" 
                  overflow="hidden" 
                  border="1px" 
                  borderColor="#e2e8f0"
                >
                  <img 
                    src={`${import.meta.env.BASE_URL}comparative_elasticity.png`}
                    alt="Comparative elasticity across countries"
                    style={{ width: '100%', display: 'block' }}
                  />
                </Box>
              </Box>

              <VStack align="stretch" gap={3}>
                <Box p={3} bg="#fef2f2" borderRadius="md" border="1px" borderColor="#fecaca">
                  <Text fontWeight="semibold" color="#dc2626">Indonesia (-2.88)</Text>
                  <Text color="#64748b" fontSize="sm">The most price-sensitive destination</Text>
                </Box>
                <Box p={3} bg="#fff7ed" borderRadius="md" border="1px" borderColor="#fed7aa">
                  <Text fontWeight="semibold" color="#ea580c">Thailand (-2.33)</Text>
                  <Text color="#64748b" fontSize="sm">Highly sensitive (in the long-run model)</Text>
                </Box>
                <Box p={3} bg="#f0fdf4" borderRadius="md" border="1px" borderColor="#bbf7d0">
                  <Text fontWeight="semibold" color="#16a34a">Malaysia (-1.18) & Vietnam (-0.70)</Text>
                  <Text color="#64748b" fontSize="sm">Less sensitive (elasticity not statistically significant)</Text>
                </Box>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Recovery Scorecard
              </Text>
              <Text color="#64748b" mb={4}>
                Comparing 2024 arrivals to pre-pandemic (2019) levels across destinations:
              </Text>
              
              <Box mb={6}>
                <Box 
                  borderRadius="md" 
                  overflow="hidden" 
                  border="1px" 
                  borderColor="#e2e8f0"
                >
                  <img 
                    src={`${import.meta.env.BASE_URL}recovery_scorecard.png`}
                    alt="Recovery scorecard by country"
                    style={{ width: '100%', display: 'block' }}
                  />
                </Box>
              </Box>

              <VStack align="stretch" gap={3}>
                <Box p={3} bg="#f0fdf4" borderRadius="md" border="1px" borderColor="#bbf7d0">
                  <Text fontWeight="semibold" color="#16a34a">Vietnam</Text>
                  <Text color="#64748b" fontSize="sm">Leading the recovery (~60% of 2019 levels)</Text>
                </Box>
                <Box p={3} bg="#fff7ed" borderRadius="md" border="1px" borderColor="#fed7aa">
                  <Text fontWeight="semibold" color="#ea580c">Thailand</Text>
                  <Text color="#64748b" fontSize="sm">Lagging slightly behind (~60%), statistically indistinguishable from the group average</Text>
                </Box>
                <Box p={3} bg="#fef2f2" borderRadius="md" border="1px" borderColor="#fecaca">
                  <Text fontWeight="semibold" color="#dc2626">Indonesia</Text>
                  <Text color="#64748b" fontSize="sm">Showing the slowest recovery in this specific Chinese market segment</Text>
                </Box>
              </VStack>
            </Box>

            <Box p={5} bg="#f1f5f9" borderRadius="md" border="1px" borderColor="#cbd5e1">
              <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
                Strategic Implications
              </Text>
              <VStack align="stretch" gap={3}>
                <Text color="#64748b" fontSize="sm">
                  <strong>Competitive Positioning:</strong> Thailand and Indonesia compete directly on price, 
                  making exchange rate management crucial for market share.
                </Text>
                <Text color="#64748b" fontSize="sm">
                  <strong>Market Differentiation:</strong> Vietnam and Malaysia appear to have successfully 
                  differentiated their offerings, reducing price sensitivity.
                </Text>
                <Text color="#64748b" fontSize="sm">
                  <strong>Recovery Strategy:</strong> Thailand's recovery is in line with regional averages, 
                  but the high price elasticity suggests vulnerability to currency appreciation.
                </Text>
              </VStack>
            </Box>

            <Box>
              <Text fontSize="xl" fontWeight="semibold" mb={4}>
                Conclusion
              </Text>
              <Text color="#64748b" mb={4}>
                This econometric analysis confirms that <strong>Thailand's tourism sector is highly sensitive 
                to economic fundamentals</strong>.
              </Text>
              
              <VStack align="stretch" gap={4}>
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={2}>
                    1. Growth Engine
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    Continued growth in China's GDP will naturally drive arrivals, but at a rate less than 1:1 
                    (inelastic income demand).
                  </Text>
                </Box>
                
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={2}>
                    2. Risk Factor
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    The <strong>Real Exchange Rate</strong> is a critical variable. A strengthening Baht poses 
                    a significant risk to competitiveness, especially against price-sensitive competitors like Indonesia.
                  </Text>
                </Box>
                
                <Box>
                  <Text fontWeight="semibold" color="#1e293b" mb={2}>
                    3. Policy Implication
                  </Text>
                  <Text color="#64748b" fontSize="sm">
                    To maintain competitiveness, Thailand must either manage exchange rate volatility or—more 
                    sustainably—move up the value chain to reduce price sensitivity (making demand more inelastic).
                  </Text>
                </Box>
              </VStack>
            </Box>
          </VStack>
        )}
      </Box>
    </Box>
  )
}