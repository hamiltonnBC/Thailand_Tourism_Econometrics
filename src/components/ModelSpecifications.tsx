/**
 * Model Specifications Component
 * 
 * Details possible econometric models and variations for the analysis.
 */

import { Box, Text, VStack } from '@chakra-ui/react'

export function ModelSpecifications() {
  return (
    <VStack align="stretch" gap={6}>
      <Box>
        <Text fontSize="2xl" fontWeight="semibold" mb={4} color="#1e293b">
          Econometric Model Specifications
        </Text>
        <Text color="#64748b" mb={4}>
          Our panel data structure enables multiple modeling approaches. Below are the key specifications 
          we can estimate, each with different assumptions and interpretations.
        </Text>
      </Box>

      {/* Base Model */}
      <Box p={5} borderWidth="2px" borderColor="#3b82f6" borderRadius="md" bg="#eff6ff">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e3a8a">
          1. Fixed Effects (FE) Model — Primary Specification
        </Text>
        <Box as="pre" p={3} bg="white" borderRadius="sm" fontSize="sm" color="#1e293b" mb={3} overflowX="auto">
          ln(arrivals_it) = β₀ + β₁·peace_index_it + β₂·ln(cpi_index_it) + β₃·ln(gdp_china_t) + β₄·ln(exchange_rate_it) + αᵢ + εᵢₜ
        </Box>
        <VStack align="stretch" gap={2} fontSize="sm" color="#1e40af">
          <Text><strong>Where:</strong></Text>
          <Text>• αᵢ = Country fixed effects (controls for time-invariant country characteristics)</Text>
          <Text>• i = country, t = year</Text>
          <Text>• All continuous variables in logs for elasticity interpretation</Text>
        </VStack>
        <Box mt={3} p={3} bg="#dbeafe" borderRadius="sm">
          <Text fontSize="sm" color="#1e40af" lineHeight="1.8">
            <strong>Why FE?</strong> Controls for unobserved heterogeneity (culture, geography, infrastructure) 
            that doesn't change over time. Focuses on within-country variation. Eliminates omitted variable bias 
            from time-invariant factors.
          </Text>
        </Box>
      </Box>

      {/* Alternative Models */}
      <Box p={5} borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" bg="#f8fafc">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
          2. Random Effects (RE) Model — Alternative Specification
        </Text>
        <Box as="pre" p={3} bg="white" borderRadius="sm" fontSize="sm" color="#1e293b" mb={3} overflowX="auto">
          ln(arrivals_it) = β₀ + β₁·peace_index_it + β₂·ln(cpi_index_it) + β₃·ln(gdp_china_t) + β₄·ln(exchange_rate_it) + uᵢ + εᵢₜ
        </Box>
        <Text fontSize="sm" color="#64748b" lineHeight="1.8" mb={2}>
          Where uᵢ ~ N(0, σᵤ²) is a random country-specific effect uncorrelated with regressors.
        </Text>
        <Box p={3} bg="#fef3c7" borderRadius="sm">
          <Text fontSize="sm" color="#78350f" lineHeight="1.8">
            <strong>Trade-off:</strong> More efficient than FE if assumptions hold, but requires strict exogeneity. 
            Use Hausman test to choose between FE and RE. If test rejects (p &lt; 0.05), prefer FE.
          </Text>
        </Box>
      </Box>

      <Box p={5} borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" bg="#f8fafc">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
          3. Two-Way Fixed Effects — Time + Country Controls
        </Text>
        <Box as="pre" p={3} bg="white" borderRadius="sm" fontSize="sm" color="#1e293b" mb={3} overflowX="auto">
          ln(arrivals_it) = β₁·peace_index_it + β₂·ln(cpi_index_it) + β₄·ln(exchange_rate_it) + αᵢ + γₜ + εᵢₜ
        </Box>
        <Text fontSize="sm" color="#64748b" lineHeight="1.8">
          Adds year fixed effects (γₜ) to control for global shocks (financial crises, pandemics, global trends). 
          Note: China GDP drops out due to collinearity with year effects.
        </Text>
      </Box>

      {/* Extensions */}
      <Box p={5} borderWidth="1px" borderColor="#10b981" borderRadius="md" bg="#f0fdf4">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#065f46">
          4. Dynamic Panel Model — Including Lagged Dependent Variable
        </Text>
        <Box as="pre" p={3} bg="white" borderRadius="sm" fontSize="sm" color="#1e293b" mb={3} overflowX="auto">
          ln(arrivals_it) = ρ·ln(arrivals_i,t-1) + β₁·peace_index_it + β₂·ln(cpi_index_it) + ... + αᵢ + εᵢₜ
        </Box>
        <Text fontSize="sm" color="#065f46" lineHeight="1.8">
          Captures persistence in tourism flows (word-of-mouth, repeat visits). Requires GMM estimation 
          (Arellano-Bond) to handle endogeneity of lagged DV. Useful for understanding adjustment dynamics.
        </Text>
      </Box>

      <Box p={5} borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" bg="#f8fafc">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
          5. Interaction Effects — Heterogeneous Responses
        </Text>
        <Box as="pre" p={3} bg="white" borderRadius="sm" fontSize="sm" color="#1e293b" mb={3} overflowX="auto">
          ln(arrivals_it) = ... + β₅·peace_index_it × Region_i + β₆·ln(exchange_rate_it) × Distance_i + ...
        </Box>
        <Text fontSize="sm" color="#64748b" lineHeight="1.8">
          Test if effects vary by region (Southeast Asia vs. others) or distance from China. 
          Allows for heterogeneous treatment effects across country groups.
        </Text>
      </Box>

      {/* Robustness Checks */}
      <Box p={5} borderWidth="1px" borderColor="#f59e0b" borderRadius="md" bg="#fffbeb">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#92400e">
          6. Robustness Checks & Variations
        </Text>
        <VStack align="stretch" gap={3} fontSize="sm" color="#78350f">
          <Box>
            <Text fontWeight="semibold" mb={1}>a) Different Time Periods</Text>
            <Text>• Pre-COVID only (2008-2019): Avoids pandemic disruption</Text>
            <Text>• Full sample (2000-2024): Maximum observations but includes structural break</Text>
            <Text>• Post-2008: Best data quality period</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold" mb={1}>b) Alternative Dependent Variables</Text>
            <Text>• Level (not logged): For countries with zero/missing arrivals</Text>
            <Text>• Growth rates: Δln(arrivals_it) = ln(arrivals_it) - ln(arrivals_i,t-1)</Text>
            <Text>• Market share: arrivals_it / Σⱼ arrivals_jt</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold" mb={1}>c) Clustered Standard Errors</Text>
            <Text>• Cluster by country: Accounts for within-country correlation</Text>
            <Text>• Cluster by year: Accounts for cross-sectional correlation</Text>
            <Text>• Two-way clustering: Most conservative</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold" mb={1}>d) Outlier Treatment</Text>
            <Text>• Winsorize at 1st/99th percentiles</Text>
            <Text>• Exclude COVID years (2020-2021)</Text>
            <Text>• Exclude countries with &gt;30% missing data</Text>
          </Box>
        </VStack>
      </Box>

      {/* Expected Findings */}
      <Box p={5} borderWidth="2px" borderColor="#8b5cf6" borderRadius="md" bg="#faf5ff">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#5b21b6">
          Expected Findings & Hypotheses
        </Text>
        <VStack align="stretch" gap={3} fontSize="sm" color="#6b21a8">
          <Box>
            <Text fontWeight="semibold">H1: Peace Index (β₁ &lt; 0)</Text>
            <Text>Higher peace index (less peaceful) → fewer arrivals. Safety concerns deter tourists.</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold">H2: CPI/Inflation (β₂ &lt; 0)</Text>
            <Text>Higher prices → fewer arrivals. Destination becomes less competitive.</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold">H3: China GDP (β₃ &gt; 0)</Text>
            <Text>Wealthier China → more outbound tourism. Income effect dominates.</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold">H4: Exchange Rate (β₄ ambiguous)</Text>
            <Text>Appreciation of destination currency → more expensive for Chinese tourists → fewer arrivals (β₄ &lt; 0). 
            But could signal economic strength (β₄ &gt; 0). Empirical question.</Text>
          </Box>
          <Box>
            <Text fontWeight="semibold">H5: COVID Structural Break</Text>
            <Text>Expect significant negative shock in 2020-2021, with asymmetric recovery across countries.</Text>
          </Box>
        </VStack>
      </Box>

      {/* Limitations */}
      <Box p={5} borderWidth="1px" borderColor="#ef4444" borderRadius="md" bg="#fef2f2">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#991b1b">
          Limitations & Caveats
        </Text>
        <VStack align="stretch" gap={2} fontSize="sm" color="#7f1d1d" lineHeight="1.8">
          <Text>• <strong>Omitted variables:</strong> Visa policies, marketing spend, flight capacity not included</Text>
          <Text>• <strong>Endogeneity:</strong> Exchange rates may be endogenous to tourism demand</Text>
          <Text>• <strong>Measurement error:</strong> Arrivals data quality varies by country</Text>
          <Text>• <strong>Unbalanced panel:</strong> Missing data reduces sample size and power</Text>
          <Text>• <strong>External validity:</strong> Results specific to Chinese outbound tourism</Text>
        </VStack>
      </Box>
    </VStack>
  )
}
