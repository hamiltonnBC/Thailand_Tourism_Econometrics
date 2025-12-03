/**
 * RegressionModelCard Component
 * 
 * Displays a regression model specification with its description and hypothesis tests
 */

import { Box, VStack, HStack, Text, Code } from '@chakra-ui/react'

interface HypothesisTest {
  name: string
  nullHypothesis: string
  result: string
  interpretation: string
  pValue?: string
}

interface RegressionModelCardProps {
  modelName: string
  modelEquation: string
  description: string
  keyFindings: string[]
  hypothesisTests: HypothesisTest[]
}

export function RegressionModelCard({
  modelName,
  modelEquation,
  description,
  keyFindings,
  hypothesisTests
}: RegressionModelCardProps) {
  return (
    <Box
      border="2px"
      borderColor="#cbd5e1"
      borderRadius="lg"
      p={6}
      bg="white"
      _hover={{
        borderColor: '#94a3b8',
        boxShadow: 'md'
      }}
      transition="all 0.3s"
    >
      <VStack align="stretch" gap={5}>
        {/* Model Header */}
        <Box>
          <Text fontSize="xl" fontWeight="bold" color="#1e293b" mb={3}>
            {modelName}
          </Text>
          <Box bg="#f8fafc" p={4} borderRadius="md" border="1px" borderColor="#e2e8f0">
            <Code fontSize="sm" colorScheme="gray" whiteSpace="pre-wrap">
              {modelEquation}
            </Code>
          </Box>
        </Box>

        {/* Description */}
        <Box>
          <Text color="#64748b" lineHeight="1.8">
            {description}
          </Text>
        </Box>

        {/* Key Findings */}
        {keyFindings.length > 0 && (
          <Box>
            <Text fontWeight="semibold" color="#1e293b" mb={2}>
              Key Findings:
            </Text>
            <VStack align="stretch" gap={2}>
              {keyFindings.map((finding, index) => (
                <Text key={index} color="#64748b" fontSize="sm">
                  • {finding}
                </Text>
              ))}
            </VStack>
          </Box>
        )}

        {/* Hypothesis Tests */}
        <Box>
          <Text fontWeight="semibold" color="#1e293b" mb={3}>
            Hypothesis Tests:
          </Text>
          <HStack gap={4} flexWrap="wrap">
            {hypothesisTests.map((test, index) => (
              <HypothesisTestCard key={index} test={test} />
            ))}
          </HStack>
        </Box>
      </VStack>
    </Box>
  )
}

function HypothesisTestCard({ test }: { test: HypothesisTest }) {
  // Determine if test was rejected (success - found an effect) or failed to reject (no effect found)
  // "Reject H₀" = GREEN (we found evidence of an effect - statistical success!)
  // "Fail to reject H₀" = RED (we didn't find evidence of an effect)
  const resultLower = test.result.toLowerCase()
  const isRejected = resultLower.includes('reject h₀') && !resultLower.includes('fail to reject')
  const isFailed = resultLower.includes('fail to reject')
  
  // Set colors based on result
  // GREEN = Successfully rejected null (found an effect)
  // RED = Failed to reject null (no significant effect found)
  const borderColor = isRejected ? '#86efac' : isFailed ? '#fca5a5' : '#e2e8f0'
  const bgColor = isRejected ? '#f0fdf4' : isFailed ? '#fef2f2' : '#f8fafc'
  const glowColor = isRejected ? '0 0 12px rgba(134, 239, 172, 0.6)' : 
                    isFailed ? '0 0 12px rgba(252, 165, 165, 0.6)' : 'none'
  const hoverBorderColor = isRejected ? '#4ade80' : isFailed ? '#f87171' : '#cbd5e1'
  const hoverBgColor = isRejected ? '#dcfce7' : isFailed ? '#fee2e2' : '#f1f5f9'
  
  return (
    <Box
      flex="1"
      minW="250px"
      border="2px"
      borderColor={borderColor}
      borderRadius="md"
      p={4}
      bg={bgColor}
      boxShadow={glowColor}
      _hover={{
        bg: hoverBgColor,
        borderColor: hoverBorderColor,
        boxShadow: isRejected ? '0 0 16px rgba(134, 239, 172, 0.8)' : 
                   isFailed ? '0 0 16px rgba(252, 165, 165, 0.8)' : 'md'
      }}
      transition="all 0.3s"
    >
      <VStack align="stretch" gap={3}>
        <Text fontWeight="bold" fontSize="sm" color="#1e293b">
          {test.name}
        </Text>
        
        <Box>
          <Text fontSize="xs" color="#64748b" fontWeight="semibold" mb={1}>
            H₀:
          </Text>
          <Text fontSize="xs" color="#64748b">
            {test.nullHypothesis}
          </Text>
        </Box>

        {test.pValue && (
          <Box>
            <Text fontSize="xs" color="#64748b" fontWeight="semibold" mb={1}>
              p-value:
            </Text>
            <Text fontSize="xs" fontFamily="mono" color="#1e293b">
              {test.pValue}
            </Text>
          </Box>
        )}

        <Box>
          <Text fontSize="xs" color="#64748b" fontWeight="semibold" mb={1}>
            Result:
          </Text>
          <Text 
            fontSize="xs" 
            fontWeight="semibold"
            color={isRejected ? '#16a34a' : isFailed ? '#dc2626' : '#64748b'}
          >
            {test.result}
          </Text>
        </Box>

        <Box 
          bg="white" 
          p={2} 
          borderRadius="sm" 
          border="1px" 
          borderColor={isRejected ? '#86efac' : isFailed ? '#fca5a5' : '#e2e8f0'}
        >
          <Text fontSize="xs" color="#475569" fontStyle="italic">
            {test.interpretation}
          </Text>
        </Box>
      </VStack>
    </Box>
  )
}
