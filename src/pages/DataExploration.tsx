/**
 * Data Exploration Page Component
 * 
 * Data exploration page with sub-tabs for Visualizations and Data Notes.
 */

import { useState } from 'react'
import { Box, HStack, Text } from '@chakra-ui/react'
import { ChinaArrivalsChart } from '../components/ChinaArrivalsChart'
import { RecoveryRateChart } from '../components/RecoveryRateChart'
import { DataExplorer } from '../components/DataExplorer'
import { ModelSpecifications } from '../components/ModelSpecifications'

type DataExplorationTab = 'visualizations' | 'notes'

export function DataExploration() {
  const [activeSubTab, setActiveSubTab] = useState<DataExplorationTab>('visualizations')

  return (
    <Box>
      <Box fontSize="3xl" fontWeight="bold" mb={6} color="#1e293b">
        Data Exploration
      </Box>

      {/* Sub-navigation tabs */}
      <HStack gap={2} mb={8} borderBottom="2px" borderColor="#e2e8f0" pb={0}>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'visualizations' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'visualizations' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'visualizations' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('visualizations')}
        >
          Visualizations
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'notes' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'notes' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'notes' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('notes')}
        >
          Data Notes
        </Box>
      </HStack>

      {/* Content area */}
      <Box color="#1e293b" lineHeight="1.8">
        {activeSubTab === 'visualizations' && (
          <Box>
            <ChinaArrivalsChart />
            
            {/* Recovery Rate Chart */}
            <Box mt={16} pt={16} borderTop="3px" borderColor="#e2e8f0">
              <RecoveryRateChart />
            </Box>
          </Box>
        )}
        {activeSubTab === 'notes' && (
          <Box>
            {/* Data Explorer Component */}
            <DataExplorer />

            {/* Model Specifications */}
            <Box mt={16} pt={16} borderTop="3px" borderColor="#e2e8f0">
              <ModelSpecifications />
            </Box>

            {/* Original Data Notes */}
            <Box mt={16} pt={16} borderTop="3px" borderColor="#e2e8f0">
              <Text fontSize="2xl" fontWeight="semibold" mb={4}>
                Data Collection & Processing Notes
              </Text>
            
            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Country Selection
            </Text>
            <Text color="#64748b" mb={4}>
              We selected 13 destination countries based on three key criteria:
            </Text>
            <Box as="ul" pl={6} color="#64748b" mb={4}>
              <Box as="li" mb={2}>Data availability and consistency across the 2005-2024 period</Box>
              <Box as="li" mb={2}>Regional competition with Thailand for Chinese tourists</Box>
              <Box as="li">Significant volume of Chinese outbound tourists to these locations</Box>
            </Box>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Consumer Price Index (CPI)
            </Text>
            <Text color="#64748b" mb={4}>
              We built our index variable for CPI setting the base as 2010 = 100. This standardization allows for 
              consistent comparison across countries and time periods.
            </Text>
            <Text color="#64748b" mb={4}>
              <strong>Cambodia Data Challenge:</strong> The data we collected for CPI was initially in interest rate 
              format and as a percentage. We needed this as an index for our model, so we read the methodology behind 
              how this was done and converted the data accordingly.
            </Text>
            <Text color="#64748b" mb={4}>
              A specific issue arose with Cambodia's 2024 data, which was missing from our primary sources. We found 
              this data on the National Bank of Cambodia's website (https://www.nbc.gov.kh/english/economic_research/monetary_and_financial_statistics_data.php). 
              However, their index used 2006 = 100 as the base year, requiring us to rebase it to align with our 2010 
              standard.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Data Sources
            </Text>
            <Text color="#64748b" mb={4}>
              We utilized multiple sources for certain datasets to ensure completeness and accuracy:
            </Text>
            <Box as="ul" pl={6} color="#64748b" mb={4}>
              <Box as="li" mb={2}>Tourist arrival data from national tourism boards and statistical offices</Box>
              <Box as="li" mb={2}>Exchange rate data from central banks and IMF databases</Box>
              <Box as="li" mb={2}>GDP data from World Bank and national statistical agencies</Box>
              <Box as="li" mb={2}>Safety indices from Vision of Humanity (IEP) Global Peace Index</Box>
              <Box as="li">Visa policy information from official government sources and IATA</Box>
            </Box>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Web Scraping Challenges
            </Text>
            <Text color="#64748b" mb={4}>
              Data collection involved extensive web scraping, particularly from Chinese government sources. We 
              encountered and overcame bot protection mechanisms, requiring sophisticated scraping techniques and 
              respectful rate limiting to ensure data integrity.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Data Transformations
            </Text>
            <Text color="#64748b" mb={4}>
              Several variables underwent logarithmic transformation to:
            </Text>
            <Box as="ul" pl={6} color="#64748b" mb={4}>
              <Box as="li" mb={2}>Allow interpretation of coefficients as percentage changes</Box>
              <Box as="li" mb={2}>Smooth out massive outliers between countries</Box>
              <Box as="li">Ensure linearity in parameters for our regression model</Box>
            </Box>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Panel Structure
            </Text>
            <Text color="#64748b">
              Our final dataset is an unbalanced panel, meaning not all countries have complete data for all years. 
              This is common in tourism research and is appropriately handled by our Fixed Effects estimator, which 
              accounts for missing observations without introducing bias.
            </Text>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  )
}
