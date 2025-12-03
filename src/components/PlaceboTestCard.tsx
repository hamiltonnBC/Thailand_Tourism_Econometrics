/**
 * PlaceboTestCard Component
 * 
 * Displays spatial placebo test results for each country
 */

import { Box, VStack, HStack, Text, SimpleGrid } from '@chakra-ui/react'

interface PlaceboTest {
  country: string
  coefficient: number | string
  pValue: string
  tStat: string
  isSignificant: boolean
  isThailand?: boolean
}

interface PlaceboTestCardProps {
  title: string
  description: string
  tests: PlaceboTest[]
  interpretation: string
}

export function PlaceboTestCard({
  title,
  description,
  tests,
  interpretation
}: PlaceboTestCardProps) {
  return (
    <Box
      border="2px"
      borderColor="#cbd5e1"
      borderRadius="lg"
      p={6}
      bg="white"
    >
      <VStack align="stretch" gap={5}>
        {/* Header */}
        <Box>
          <Text fontSize="xl" fontWeight="bold" color="#1e293b" mb={3}>
            {title}
          </Text>
          <Text color="#64748b" lineHeight="1.8" mb={4}>
            {description}
          </Text>
        </Box>

        {/* Test Results Grid */}
        <Box>
          <Text fontWeight="semibold" color="#1e293b" mb={3}>
            Placebo Test Results:
          </Text>
          <SimpleGrid columns={{ base: 1, md: 2, lg: 3, xl: 4 }} gap={4}>
            {tests.map((test, index) => (
              <PlaceboCountryCard key={index} test={test} />
            ))}
          </SimpleGrid>
        </Box>

        {/* Interpretation */}
        <Box 
          bg="#f0f9ff" 
          border="1px" 
          borderColor="#3b82f6" 
          borderRadius="md" 
          p={4}
        >
          <Text fontWeight="semibold" color="#1e40af" mb={2} fontSize="sm">
            📊 Interpretation:
          </Text>
          <Text color="#1e40af" fontSize="sm" lineHeight="1.6">
            {interpretation}
          </Text>
        </Box>
      </VStack>
    </Box>
  )
}

function PlaceboCountryCard({ test }: { test: PlaceboTest }) {
  // Determine colors based on significance and whether it's Thailand
  const isThailand = test.isThailand || false
  const isSignificant = test.isSignificant
  
  // Color logic:
  // Thailand + Significant = Blue (this is our main result)
  // Other country + Significant = Red (problematic - shouldn't be significant)
  // Other country + Not Significant = Green (good - as expected)
  let borderColor = '#e2e8f0'
  let bgColor = '#f8fafc'
  let glowColor = 'none'
  let statusColor = '#64748b'
  let statusText = 'Not Significant'
  
  if (isThailand) {
    // Thailand - should be significant (blue)
    borderColor = isSignificant ? '#60a5fa' : '#fca5a5'
    bgColor = isSignificant ? '#eff6ff' : '#fef2f2'
    glowColor = isSignificant ? '0 0 12px rgba(96, 165, 250, 0.6)' : '0 0 12px rgba(252, 165, 165, 0.6)'
    statusColor = isSignificant ? '#1d4ed8' : '#dc2626'
    statusText = isSignificant ? '✓ Significant (Expected)' : '✗ Not Significant (Unexpected)'
  } else {
    // Other countries - should NOT be significant
    if (isSignificant) {
      // RED - problematic
      borderColor = '#fca5a5'
      bgColor = '#fef2f2'
      glowColor = '0 0 12px rgba(252, 165, 165, 0.6)'
      statusColor = '#dc2626'
      statusText = '✗ Significant (Problem!)'
    } else {
      // GREEN - good
      borderColor = '#86efac'
      bgColor = '#f0fdf4'
      glowColor = '0 0 12px rgba(134, 239, 172, 0.6)'
      statusColor = '#16a34a'
      statusText = '✓ Not Significant (Good)'
    }
  }
  
  return (
    <Box
      border="2px"
      borderColor={borderColor}
      borderRadius="md"
      p={4}
      bg={bgColor}
      boxShadow={glowColor}
      _hover={{
        transform: 'translateY(-2px)',
        boxShadow: `${glowColor}, 0 4px 6px rgba(0,0,0,0.1)`
      }}
      transition="all 0.3s"
    >
      <VStack align="stretch" gap={3}>
        <Text 
          fontWeight="bold" 
          fontSize="md" 
          color="#1e293b"
          textAlign="center"
        >
          {test.country}
          {isThailand && ' 🇹🇭'}
        </Text>
        
        <Box bg="white" p={2} borderRadius="sm" border="1px" borderColor="#e2e8f0">
          <VStack align="stretch" gap={1}>
            <HStack justify="space-between">
              <Text fontSize="xs" color="#64748b">Coefficient:</Text>
              <Text fontSize="xs" fontFamily="mono" fontWeight="semibold" color="#1e293b">
                {typeof test.coefficient === 'number' ? test.coefficient.toFixed(4) : test.coefficient}
              </Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontSize="xs" color="#64748b">t-stat:</Text>
              <Text fontSize="xs" fontFamily="mono" color="#1e293b">
                {test.tStat}
              </Text>
            </HStack>
            <HStack justify="space-between">
              <Text fontSize="xs" color="#64748b">p-value:</Text>
              <Text fontSize="xs" fontFamily="mono" color="#1e293b">
                {test.pValue}
              </Text>
            </HStack>
          </VStack>
        </Box>

        <Box 
          bg={isThailand ? (isSignificant ? '#dbeafe' : '#fee2e2') : (isSignificant ? '#fee2e2' : '#dcfce7')}
          p={2} 
          borderRadius="sm"
          textAlign="center"
        >
          <Text fontSize="xs" fontWeight="bold" color={statusColor}>
            {statusText}
          </Text>
        </Box>
      </VStack>
    </Box>
  )
}
