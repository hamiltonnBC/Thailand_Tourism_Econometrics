/**
 * Navigation Component
 * 
 * Left sidebar navigation with tabs for different sections of the econometrics dashboard.
 * Handles active tab state and navigation between sections.
 */

import { Box, VStack } from '@chakra-ui/react'

export type TabId = 'overview' | 'data' | 'model' | 'safety' | 'advanced'

interface NavigationProps {
  activeTab: TabId
  onTabChange: (tab: TabId) => void
}

const tabs: { id: TabId; label: string }[] = [
  { id: 'overview', label: 'Overview' },
  { id: 'data', label: 'Data Exploration' },
  { id: 'model', label: 'Panel Data Analysis' },
  { id: 'safety', label: 'Thailand Safety Regression' },
  { id: 'advanced', label: 'Time Series Analysis' },

]

export function Navigation({ activeTab, onTabChange }: NavigationProps) {
  return (
    <Box
      bg="white"
      borderRight="1px"
      borderColor="#e2e8f0"
      w="250px"
      minH="calc(100vh - 120px)"
      position="fixed"
      left={0}
      top="120px"
      overflowY="auto"
      boxShadow="sm"
    >
      <VStack gap={1} align="stretch" p={4}>
        {tabs.map((tab) => (
          <Box
            key={tab.id}
            px={4}
            py={3}
            cursor="pointer"
            fontWeight={activeTab === tab.id ? 'semibold' : 'medium'}
            fontSize="sm"
            color={activeTab === tab.id ? '#1e293b' : '#64748b'}
            bg={activeTab === tab.id ? '#f1f5f9' : 'transparent'}
            borderRadius="md"
            borderLeft="3px"
            borderColor={activeTab === tab.id ? '#1e293b' : 'transparent'}
            _hover={{
              color: '#1e293b',
              bg: '#f8fafc'
            }}
            transition="all 0.2s"
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </Box>
        ))}
      </VStack>
    </Box>
  )
}
