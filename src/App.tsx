/**
 * App Component
 * 
 * Main application component that manages the overall layout and tab navigation.
 * Renders the header, navigation, and content based on the active tab.
 */

import { useState } from 'react'
import { Box, Container } from '@chakra-ui/react'
import { Header } from './components/Header'
import { Navigation, type TabId } from './components/Navigation'
import { Overview } from './pages/Overview'
import { DataExploration } from './pages/DataExploration'
import { Model } from './pages/Model'

function App() {
  const [activeTab, setActiveTab] = useState<TabId>('overview')

  return (
    <Box minH="100vh" bg="#f8fafc">
      <Header />
      
      <Box display="flex">
        <Navigation activeTab={activeTab} onTabChange={setActiveTab} />
        
        <Box ml="250px" flex={1} p={12}>
          <Container maxW="container.xl">
            <Box 
              bg="white" 
              borderRadius="lg" 
              boxShadow="sm"
              border="1px"
              borderColor="#e2e8f0"
              p={10}
              minH="600px"
            >
              {activeTab === 'overview' && <Overview />}
              {activeTab === 'data' && <DataExploration />}
              {activeTab === 'model' && <Model />}
              {activeTab === 'results' && (
                <Box>
                  <Box fontSize="3xl" fontWeight="bold" mb={4} color="#1e293b">
                    Results
                  </Box>
                  <Box color="#64748b" fontSize="md">Results content coming soon...</Box>
                </Box>
              )}
              {activeTab === 'conclusions' && (
                <Box>
                  <Box fontSize="3xl" fontWeight="bold" mb={4} color="#1e293b">
                    Conclusions
                  </Box>
                  <Box color="#64748b" fontSize="md">Conclusions content coming soon...</Box>
                </Box>
              )}
              {activeTab === 'team' && (
                <Box>
                  <Box fontSize="3xl" fontWeight="bold" mb={4} color="#1e293b">
                    Team
                  </Box>
                  <Box color="#64748b" fontSize="md">Team content coming soon...</Box>
                </Box>
              )}
              {activeTab === 'references' && (
                <Box>
                  <Box fontSize="3xl" fontWeight="bold" mb={4} color="#1e293b">
                    References
                  </Box>
                  <Box color="#64748b" fontSize="md">References content coming soon...</Box>
                </Box>
              )}
            </Box>
          </Container>
        </Box>
      </Box>
    </Box>
  )
}

export default App
