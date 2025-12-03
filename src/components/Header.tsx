/**
 * Header Component
 * 
 * Main header displaying the project title.
 * Sits above the navigation tabs.
 */

import { Box, Container, Heading, Text } from '@chakra-ui/react'

export function Header() {
  return (
    <Box 
      bg="#1e293b" 
      color="white" 
      py={10}
      borderBottom="1px"
      borderColor="#334155"
    >
      <Container maxW="container.xl">
        <Heading 
          size="2xl" 
          fontWeight="bold"
          letterSpacing="tight"
          mb={2}
        >
            Econometrics at Mahidol University
        </Heading>
        <Text 
          fontSize="lg" 
          color="#cbd5e1"
        >
          Thailand Tourism Analysis
        </Text>
      </Container>
    </Box>
  )
}
