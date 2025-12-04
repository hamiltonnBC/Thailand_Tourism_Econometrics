/**
 * MulticollinearityCheck Component
 * 
 * Displays VIF analysis and correlation matrices for multicollinearity diagnostics
 */

import { Box, HStack, Text } from '@chakra-ui/react'

interface VIFData {
  variable: string
  vif: number
}

interface MulticollinearityCheckProps {
  modelName: string
  vifData: VIFData[]
  maxVIF: number
  conditionNumber: number
  highCorrelations: string[]
}

export function MulticollinearityCheck({
  modelName,
  vifData,
  maxVIF,
  conditionNumber,
  highCorrelations
}: MulticollinearityCheckProps) {
  const getVIFColor = (vif: number) => {
    if (vif < 5) return '#16a34a' // green
    if (vif < 10) return '#f59e0b' // orange
    return '#dc2626' // red
  }

  const getVIFStatus = (vif: number) => {
    if (vif < 5) return 'Low'
    if (vif < 10) return 'Moderate'
    return 'High'
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
      <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
        {modelName}
      </Text>

      {/* VIF Table */}
      <Box mb={4}>
        <Text fontSize="sm" fontWeight="semibold" color="#64748b" mb={2}>
          Variance Inflation Factors (VIF)
        </Text>
        <Box 
          bg="white" 
          borderRadius="md" 
          border="1px" 
          borderColor="#e2e8f0"
          overflow="hidden"
        >
          {/* Table Header */}
          <HStack 
            bg="#f1f5f9" 
            p={3} 
            borderBottom="1px" 
            borderColor="#e2e8f0"
            fontWeight="semibold"
            fontSize="sm"
            color="#64748b"
          >
            <Box flex={2}>Variable</Box>
            <Box flex={1} textAlign="right">VIF</Box>
            <Box flex={1} textAlign="right">Status</Box>
          </HStack>

          {/* Table Rows */}
          {vifData.map((item, idx) => (
            <HStack 
              key={idx}
              p={3} 
              borderBottom={idx < vifData.length - 1 ? "1px" : "none"}
              borderColor="#e2e8f0"
              fontSize="sm"
              _hover={{ bg: '#f8fafc' }}
            >
              <Box flex={2} color="#1e293b" fontFamily="monospace">
                {item.variable}
              </Box>
              <Box 
                flex={1} 
                textAlign="right" 
                fontWeight="medium"
                color={getVIFColor(item.vif)}
              >
                {item.vif.toFixed(2)}
              </Box>
              <Box 
                flex={1} 
                textAlign="right"
                fontSize="xs"
                fontWeight="medium"
                color={getVIFColor(item.vif)}
              >
                {getVIFStatus(item.vif)}
              </Box>
            </HStack>
          ))}
        </Box>
      </Box>

      {/* Summary Stats */}
      <HStack gap={6} mb={3} flexWrap="wrap">
        <Box>
          <Text fontSize="xs" color="#94a3b8">Max VIF</Text>
          <Text 
            fontSize="lg" 
            fontWeight="bold" 
            color={getVIFColor(maxVIF)}
          >
            {maxVIF.toFixed(2)}
          </Text>
        </Box>
        <Box>
          <Text fontSize="xs" color="#94a3b8">Condition Number (κ)</Text>
          <Text 
            fontSize="lg" 
            fontWeight="bold" 
            color={conditionNumber < 30 ? '#16a34a' : conditionNumber < 100 ? '#f59e0b' : '#dc2626'}
          >
            {conditionNumber.toFixed(2)}
          </Text>
        </Box>
        <Box>
          <Text fontSize="xs" color="#94a3b8">High Correlations (|r| {'>'} 0.7)</Text>
          <Text fontSize="lg" fontWeight="bold" color="#1e293b">
            {highCorrelations.length}
          </Text>
        </Box>
      </HStack>

      {/* High Correlations */}
      {highCorrelations.length > 0 && (
        <Box>
          <Text fontSize="xs" color="#64748b" mb={1}>
            Variables with high correlation:
          </Text>
          {highCorrelations.map((corr, idx) => (
            <Text key={idx} fontSize="xs" color="#64748b" fontFamily="monospace">
              • {corr}
            </Text>
          ))}
        </Box>
      )}

      {/* Interpretation */}
      <Box mt={3} p={3} bg="white" borderRadius="md" border="1px" borderColor="#e2e8f0">
        <Text fontSize="xs" color="#64748b">
          {maxVIF < 5 && conditionNumber < 30 && (
            <Text as="span" color="#16a34a" fontWeight={600}>
              ✓ Low multicollinearity detected.
            </Text>
          )}
          {maxVIF >= 5 && maxVIF < 10 && (
            <Text as="span" color="#f59e0b" fontWeight={600}>
              ⚠️ Moderate multicollinearity detected.
            </Text>
          )}
          {maxVIF >= 10 && (
            <Text as="span" color="#dc2626" fontWeight={600}>
              ❌ High multicollinearity detected.
            </Text>
          )}
          {' '}
          {maxVIF < 10 
            ? 'All VIF values are below 10, indicating acceptable levels of multicollinearity. Coefficient estimates are reliable.'
            : 'Some variables show high VIF values (>10), suggesting problematic multicollinearity. Consider removing or combining correlated variables.'
          }
        </Text>
      </Box>
    </Box>
  )
}
