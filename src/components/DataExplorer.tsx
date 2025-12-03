/**
 * Data Explorer Component
 * 
 * Interactive component for exploring dataset structure, variables, and completeness.
 */

import { useState } from 'react'
import { Box, Text, HStack, VStack, Tabs } from '@chakra-ui/react'

const VARIABLES = [
  {
    name: 'arrivals_from_china',
    description: 'Number of tourist arrivals from China to the destination country',
    type: 'Continuous',
    role: 'Dependent Variable',
    missing: '5.90%',
    notes: 'Primary outcome variable. Some early years missing for Indonesia, Malaysia.'
  },
  {
    name: 'peace_index',
    description: 'Global Peace Index score (lower = more peaceful)',
    type: 'Continuous',
    role: 'Independent Variable',
    missing: '47.69%',
    notes: 'Available from 2008 onwards. Measures safety and security of destination.'
  },
  {
    name: 'cpi',
    description: 'Consumer Price Index annual change rate (%)',
    type: 'Continuous',
    role: 'Independent Variable',
    missing: '16.67%',
    notes: 'Inflation measure. Some early years missing for several countries.'
  },
  {
    name: 'cpi_index',
    description: 'Consumer Price Index (2010 = 100)',
    type: 'Continuous',
    role: 'Independent Variable',
    missing: '0%',
    notes: 'Standardized price level index. Complete data across all observations.'
  },
  {
    name: 'gdp_china',
    description: "China's GDP in billions USD",
    type: 'Continuous',
    role: 'Independent Variable',
    missing: '0%',
    notes: 'Proxy for Chinese economic conditions and outbound tourism capacity.'
  },
  {
    name: 'exchange_rate',
    description: 'Exchange rate (destination currency per CNY)',
    type: 'Continuous',
    role: 'Independent Variable',
    missing: '16.67%',
    notes: 'Missing for 1995-1999. Affects relative cost of travel.'
  },
  {
    name: 'visa_free',
    description: 'Visa-free entry policy indicator',
    type: 'Binary',
    role: 'Independent Variable (Planned)',
    missing: '100%',
    notes: 'Not yet collected. Would capture policy barriers to entry.'
  },
  {
    name: 'perception_score',
    description: 'Destination perception/attractiveness score',
    type: 'Continuous',
    role: 'Independent Variable (Planned)',
    missing: '100%',
    notes: 'Not yet collected. Would measure destination image.'
  }
]

const YEAR_COVERAGE = [
  { period: '1995-1999', completeness: '42-43%', notes: 'Limited data. Missing exchange rates, peace index, some CPI.' },
  { period: '2000-2007', completeness: '56-60%', notes: 'Improving coverage. Still missing peace index, some arrivals data.' },
  { period: '2008-2019', completeness: '72-74%', notes: 'Best coverage period. Peace index available. Recommended for main analysis.' },
  { period: '2020-2024', completeness: '70-74%', notes: 'Recent data. Some countries still updating 2023-2024 figures.' }
]

export function DataExplorer() {
  const [activeTab, setActiveTab] = useState<'variables' | 'years' | 'countries'>('variables')

  return (
    <VStack align="stretch" gap={6}>
      <Box>
        <Text fontSize="2xl" fontWeight="semibold" mb={4} color="#1e293b">
          Dataset Structure & Coverage
        </Text>
        <Text color="#64748b" mb={4}>
          Explore the variables, time coverage, and data completeness of our panel dataset.
        </Text>
      </Box>

      {/* Tabs */}
      <Tabs.Root value={activeTab} onValueChange={(e) => setActiveTab(e.value as any)}>
        <Tabs.List gap={2}>
          <Tabs.Trigger value="variables">Variables</Tabs.Trigger>
          <Tabs.Trigger value="years">Year Coverage</Tabs.Trigger>
          <Tabs.Trigger value="countries">Countries</Tabs.Trigger>
        </Tabs.List>

        {/* Variables Tab */}
        <Tabs.Content value="variables">
          <VStack align="stretch" gap={4} mt={4}>
            {VARIABLES.map((variable, idx) => (
              <Box
                key={idx}
                p={4}
                borderWidth="1px"
                borderColor="#e2e8f0"
                borderRadius="md"
                bg={variable.missing === '100%' ? '#fff5f5' : '#f8fafc'}
              >
                <HStack justify="space-between" mb={2}>
                  <Text fontWeight="semibold" color="#1e293b" fontSize="md">
                    {variable.name}
                  </Text>
                  <HStack gap={3}>
                    <Box px={2} py={1} bg="#e0f2fe" borderRadius="sm">
                      <Text fontSize="xs" color="#0369a1">{variable.type}</Text>
                    </Box>
                    <Box px={2} py={1} bg={variable.missing === '0%' ? '#dcfce7' : variable.missing === '100%' ? '#fee2e2' : '#fef3c7'} borderRadius="sm">
                      <Text fontSize="xs" color={variable.missing === '0%' ? '#15803d' : variable.missing === '100%' ? '#991b1b' : '#92400e'}>
                        {variable.missing} missing
                      </Text>
                    </Box>
                  </HStack>
                </HStack>
                <Text fontSize="sm" color="#64748b" mb={2}>
                  {variable.description}
                </Text>
                <HStack gap={4} fontSize="xs" color="#64748b">
                  <Text><strong>Role:</strong> {variable.role}</Text>
                </HStack>
                <Text fontSize="xs" color="#64748b" mt={2} fontStyle="italic">
                  {variable.notes}
                </Text>
              </Box>
            ))}
          </VStack>
        </Tabs.Content>

        {/* Year Coverage Tab */}
        <Tabs.Content value="years">
          <VStack align="stretch" gap={4} mt={4}>
            <Box p={4} bg="#f0f9ff" borderWidth="1px" borderColor="#bae6fd" borderRadius="md">
              <Text fontSize="sm" color="#0c4a6e" lineHeight="1.8">
                <strong>Dataset Span:</strong> 1995-2024 (30 years) | <strong>Total Observations:</strong> 390 | <strong>Countries:</strong> 13
              </Text>
            </Box>

            {YEAR_COVERAGE.map((period, idx) => (
              <Box key={idx} p={4} borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" bg="#f8fafc">
                <HStack justify="space-between" mb={2}>
                  <Text fontWeight="semibold" color="#1e293b">{period.period}</Text>
                  <Box px={3} py={1} bg="#dbeafe" borderRadius="sm">
                    <Text fontSize="sm" color="#1e40af">{period.completeness} complete</Text>
                  </Box>
                </HStack>
                <Text fontSize="sm" color="#64748b">{period.notes}</Text>
              </Box>
            ))}


          </VStack>
        </Tabs.Content>

        {/* Countries Tab */}
        <Tabs.Content value="countries">
          <VStack align="stretch" gap={3} mt={4}>
            {[
              { name: 'Australia', completeness: '67.50%', notes: 'Complete arrivals data. Missing early exchange rates.' },
              { name: 'Cambodia', completeness: '64.17%', notes: 'Some CPI gaps. Good arrivals coverage.' },
              { name: 'Indonesia', completeness: '65.83%', notes: 'Missing arrivals 1995-1998.' },
              { name: 'Japan', completeness: '67.50%', notes: 'Excellent data quality throughout.' },
              { name: 'Korea, Republic of', completeness: '67.08%', notes: 'Missing 2024 arrivals data.' },
              { name: 'Malaysia', completeness: '59.58%', notes: 'Missing arrivals 1995-2007. Use caution for early period.' },
              { name: 'Maldives', completeness: '60.42%', notes: 'No peace index data. Small market size.' },
              { name: 'Philippines', completeness: '60.00%', notes: 'Significant CPI gaps. Missing recent arrivals.' },
              { name: 'Singapore', completeness: '62.92%', notes: 'Some early CPI missing. Otherwise strong.' },
              { name: 'Thailand', completeness: '60.83%', notes: 'CPI gaps in early years. Key destination.' },
              { name: 'United Kingdom', completeness: '66.25%', notes: 'Missing 2020, 2023-2024 arrivals.' },
              { name: 'United States of America', completeness: '67.50%', notes: 'Strong data coverage throughout.' },
              { name: 'Viet Nam', completeness: '64.17%', notes: 'Early CPI gaps. Good recent coverage.' }
            ].map((country, idx) => (
              <Box key={idx} p={3} borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" bg="#f8fafc">
                <HStack justify="space-between">
                  <Text fontWeight="medium" color="#1e293b" fontSize="sm">{country.name}</Text>
                  <Text fontSize="xs" color="#64748b">{country.completeness}</Text>
                </HStack>
                <Text fontSize="xs" color="#64748b" mt={1}>{country.notes}</Text>
              </Box>
            ))}
          </VStack>
        </Tabs.Content>
      </Tabs.Root>
    </VStack>
  )
}
