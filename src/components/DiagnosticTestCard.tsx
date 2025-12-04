/**
 * DiagnosticTestCard Component
 * 
 * Displays results from heteroskedasticity and autocorrelation tests
 */

import { Box, HStack, VStack, Text } from '@chakra-ui/react'

interface DiagnosticTestCardProps {
  modelName: string
  waldStatistic: number
  waldDF: number
  waldPValue: number
  waldResult: string
  wooldridgeF: number
  wooldridgePValue: number
  wooldridgeResult: string
}

export function DiagnosticTestCard({
  modelName,
  waldStatistic,
  waldDF,
  waldPValue,
  waldResult,
  wooldridgeF,
  wooldridgePValue,
  wooldridgeResult
}: DiagnosticTestCardProps) {
  const getStatusColor = (result: string) => {
    if (result.includes('Fail to reject')) return '#16a34a' // green - good
    return '#dc2626' // red - issue detected
  }

  const getStatusIcon = (result: string) => {
    if (result.includes('Fail to reject')) return '✓'
    return '⚠️'
  }

  return (
    <Box 
      bg="#f8fafc" 
      p={5} 
      borderRadius="md" 
      border="1px" 
      borderColor="#e2e8f0"
      mb={4}
    >
      <Text fontSize="lg" fontWeight="semibold" mb={4} color="#1e293b">
        {modelName}
      </Text>

      <VStack align="stretch" gap={4}>
        {/* Modified Wald Test */}
        <Box>
          <HStack justify="space-between" mb={2}>
            <Text fontSize="sm" fontWeight="semibold" color="#64748b">
              Modified Wald Test (Heteroskedasticity)
            </Text>
            <Text 
              fontSize="sm" 
              fontWeight="bold" 
              color={getStatusColor(waldResult)}
            >
              {getStatusIcon(waldResult)} {waldResult}
            </Text>
          </HStack>
          
          <Box 
            bg="white" 
            p={3} 
            borderRadius="md" 
            border="1px" 
            borderColor="#e2e8f0"
          >
            <HStack gap={6} flexWrap="wrap">
              <Box>
                <Text fontSize="xs" color="#94a3b8">Test Statistic</Text>
                <Text fontSize="sm" fontWeight="medium" color="#1e293b" fontFamily="monospace">
                  χ²({waldDF}) = {waldStatistic.toFixed(2)}
                </Text>
              </Box>
              <Box>
                <Text fontSize="xs" color="#94a3b8">P-value</Text>
                <Text 
                  fontSize="sm" 
                  fontWeight="medium" 
                  color={waldPValue < 0.05 ? '#dc2626' : '#16a34a'}
                  fontFamily="monospace"
                >
                  {waldPValue < 0.001 ? '< 0.001' : waldPValue.toFixed(4)}
                </Text>
              </Box>
            </HStack>
            
            <Text fontSize="xs" color="#64748b" mt={2}>
              {waldPValue < 0.05 
                ? 'Evidence of heteroskedasticity detected. Error variance differs significantly across countries.'
                : 'No strong evidence of heteroskedasticity. Error variance is relatively constant across countries.'
              }
            </Text>
          </Box>
        </Box>

        {/* Wooldridge Test */}
        <Box>
          <HStack justify="space-between" mb={2}>
            <Text fontSize="sm" fontWeight="semibold" color="#64748b">
              Wooldridge Test (Autocorrelation)
            </Text>
            <Text 
              fontSize="sm" 
              fontWeight="bold" 
              color={getStatusColor(wooldridgeResult)}
            >
              {getStatusIcon(wooldridgeResult)} {wooldridgeResult}
            </Text>
          </HStack>
          
          <Box 
            bg="white" 
            p={3} 
            borderRadius="md" 
            border="1px" 
            borderColor="#e2e8f0"
          >
            <HStack gap={6} flexWrap="wrap">
              <Box>
                <Text fontSize="xs" color="#94a3b8">F-Statistic</Text>
                <Text fontSize="sm" fontWeight="medium" color="#1e293b" fontFamily="monospace">
                  F = {wooldridgeF.toFixed(2)}
                </Text>
              </Box>
              <Box>
                <Text fontSize="xs" color="#94a3b8">P-value</Text>
                <Text 
                  fontSize="sm" 
                  fontWeight="medium" 
                  color={wooldridgePValue < 0.05 ? '#dc2626' : '#16a34a'}
                  fontFamily="monospace"
                >
                  {wooldridgePValue < 0.001 ? '< 0.001' : wooldridgePValue.toFixed(4)}
                </Text>
              </Box>
            </HStack>
            
            <Text fontSize="xs" color="#64748b" mt={2}>
              {wooldridgePValue < 0.05 
                ? 'Evidence of first-order autocorrelation detected. Errors are correlated over time within countries.'
                : 'No strong evidence of autocorrelation. Errors appear independent over time.'
              }
            </Text>
          </Box>
        </Box>
      </VStack>
    </Box>
  )
}
