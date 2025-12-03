/**
 * Model Page Component
 * 
 * The Model page with sub-tabs for Methodology, Specification, and Constraints & Tests.
 */

import { useState } from 'react'
import { Box, HStack, Text, Code, VStack } from '@chakra-ui/react'

type ModelTab = 'methodology' | 'specification' | 'constraints'

export function Model() {
  const [activeSubTab, setActiveSubTab] = useState<ModelTab>('methodology')

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
          fontWeight={activeSubTab === 'methodology' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'methodology' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'methodology' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('methodology')}
        >
          Methodology
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
          Model Specification
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'constraints' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'constraints' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'constraints' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('constraints')}
        >
          Constraints & Tests
        </Box>
      </HStack>

      {/* Content area */}
      <Box color="#1e293b" lineHeight="1.8">
        {activeSubTab === 'methodology' && (
          <VStack align="stretch" gap={6}>
            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Research Approach
              </Text>
              <Text color="#64748b" mb={4}>
                To empirically investigate the determinants of Chinese outbound tourism and quantify the asymmetric 
                recovery rates between Thailand and its regional competitors, we constructed an unbalanced panel dataset 
                covering the period 2005–2024.
              </Text>
              <Text color="#64748b" mb={4}>
                Existing econometric literature using panel data on Southeast Asian tourism has predominantly focused on 
                the 'Tourism-Led Growth Hypothesis' (TLGH). For instance, Yunitaningtyas et al. (2019) employed panel 
                data analysis across ASEAN member countries to demonstrate that tourism receipts are a statistically 
                significant driver of national economic development and GDP growth.
              </Text>
              <Text color="#64748b">
                However, there remains a critical gap in understanding post-pandemic determinants of international demand, 
                and there is a lack of quantified rationale for the observed drop in Chinese tourism to Thailand.
              </Text>
            </Box>

            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Our Contribution
              </Text>
              <Text color="#64748b" mb={4}>
                While the decline in Chinese tourism is well-documented, current literature relies on qualitative surveys 
                and year-over-year comparisons. Our study uses a <strong>Panel Data Fixed Effects approach</strong> to 
                isolate the specific magnitude of the differences from Chinese tourism to Thailand vs. other destinations, 
                while controlling for the confounding variable of China's economic slowdown.
              </Text>
              <Text color="#64748b">
                We estimate the specific 'Thailand Penalty' relative to regional competitors, along with other high tourism 
                locations. We chose the locations based on data availability, regional competition, and the number of Chinese 
                outbound tourists to these locations.
              </Text>
            </Box>

            <Box>
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Model Selection
              </Text>
              <Text color="#64748b" mb={4}>
                We utilize a <strong>Gravity-style specification</strong>. While traditional gravity models rely on distance, 
                our use of Country Fixed Effects controls for time-invariant geographic costs (Morley, Rosselló, & 
                Santana-Gallego, 2014).
              </Text>
              <Text color="#64748b" mb={4}>
                The selection of the Fixed Effects (FE) estimator is supported by empirical precedents in ASEAN tourism 
                literature. Yunitaningtyas et al. (2019) demonstrated through the Chow and Hausman tests that the Fixed 
                Effects model is superior to Random Effects for this region. They argue that ASEAN countries exhibit 
                significant unobserved heterogeneity that must be controlled for via individual intercepts.
              </Text>
              <Text color="#64748b">
                Following this methodological standard, we apply the Hausman test to confirm the appropriateness of FE 
                for our demand model.
              </Text>
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

        {activeSubTab === 'constraints' && (
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
      </Box>
    </Box>
  )
}
