/**
 * ModelStatistics Component
 * 
 * Displays key statistical information for regression models
 */

import { Box, HStack, VStack, Text } from '@chakra-ui/react'

interface ModelStatisticsProps {
  rSquared: string
  rSquaredWithin: string
  rSquaredBetween: string
  rSquaredOverall: string
  nObservations: number
  entities: number
  timePeriods: number
  fStatistic: string
  fPValue: string
  logLikelihood: string
  poolabilityF: string
  poolabilityP: string
}

export function ModelStatistics({
  rSquared,
  rSquaredWithin,
  rSquaredBetween,
  rSquaredOverall,
  nObservations,
  entities,
  timePeriods,
  fStatistic,
  fPValue,
  logLikelihood,
  poolabilityF,
  poolabilityP
}: ModelStatisticsProps) {
  return (
    <Box 
      bg="#f8fafc" 
      p={5} 
      borderRadius="md" 
      border="1px" 
      borderColor="#e2e8f0"
      mt={4}
    >
      <Text fontSize="md" fontWeight="semibold" mb={4} color="#1e293b">
        Model Statistics
      </Text>
      
      <VStack align="stretch" gap={3}>
        {/* Goodness of Fit */}
        <Box>
          <Text fontSize="sm" fontWeight="semibold" color="#64748b" mb={2}>
            Goodness of Fit
          </Text>
          <HStack gap={6} flexWrap="wrap">
            <Box>
              <Text fontSize="xs" color="#94a3b8">R²</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{rSquared}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">R² (Within)</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{rSquaredWithin}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">R² (Between)</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{rSquaredBetween}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">R² (Overall)</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{rSquaredOverall}</Text>
            </Box>
          </HStack>
        </Box>

        {/* Sample Information */}
        <Box>
          <Text fontSize="sm" fontWeight="semibold" color="#64748b" mb={2}>
            Sample
          </Text>
          <HStack gap={6} flexWrap="wrap">
            <Box>
              <Text fontSize="xs" color="#94a3b8">Observations</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{nObservations}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">Entities</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{entities}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">Time Periods</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{timePeriods}</Text>
            </Box>
          </HStack>
        </Box>

        {/* Model Tests */}
        <Box>
          <Text fontSize="sm" fontWeight="semibold" color="#64748b" mb={2}>
            Model Tests
          </Text>
          <HStack gap={6} flexWrap="wrap">
            <Box>
              <Text fontSize="xs" color="#94a3b8">F-Statistic</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{fStatistic}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">F p-value</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{fPValue}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">Log-Likelihood</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{logLikelihood}</Text>
            </Box>
          </HStack>
        </Box>

        {/* Poolability Test */}
        <Box>
          <Text fontSize="sm" fontWeight="semibold" color="#64748b" mb={2}>
            F-Test for Poolability
          </Text>
          <HStack gap={6} flexWrap="wrap">
            <Box>
              <Text fontSize="xs" color="#94a3b8">F-Statistic</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{poolabilityF}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">p-value</Text>
              <Text fontSize="sm" fontWeight="medium" color="#1e293b">{poolabilityP}</Text>
            </Box>
            <Box>
              <Text fontSize="xs" color="#94a3b8">Result</Text>
              <Text 
                fontSize="sm" 
                fontWeight="medium" 
                color={poolabilityP === '0.0000' ? '#16a34a' : '#dc2626'}
              >
                {poolabilityP === '0.0000' ? 'Fixed Effects Needed' : 'Check Specification'}
              </Text>
            </Box>
          </HStack>
        </Box>
      </VStack>
    </Box>
  )
}
