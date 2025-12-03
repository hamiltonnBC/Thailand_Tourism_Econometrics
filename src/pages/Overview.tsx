/**
 * Overview Page Component
 * 
 * Main overview page with sub-tabs for Synopsis and Our Journey.
 */

import { useState } from 'react'
import { Box, HStack, Text } from '@chakra-ui/react'

type OverviewTab = 'synopsis' | 'journey' | 'literature'

export function Overview() {
  const [activeSubTab, setActiveSubTab] = useState<OverviewTab>('synopsis')

  return (
    <Box>
      <Box fontSize="3xl" fontWeight="bold" mb={6} color="#1e293b">
        Overview
      </Box>

      {/* Sub-navigation tabs */}
      <HStack gap={2} mb={8} borderBottom="2px" borderColor="#e2e8f0" pb={0}>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'synopsis' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'synopsis' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'synopsis' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('synopsis')}
        >
          Synopsis
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'journey' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'journey' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'journey' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('journey')}
        >
          Our Journey
        </Box>
        <Box
          px={5}
          py={3}
          cursor="pointer"
          fontWeight={activeSubTab === 'literature' ? 'semibold' : 'medium'}
          fontSize="sm"
          color={activeSubTab === 'literature' ? '#1e293b' : '#64748b'}
          borderBottom="3px"
          borderColor={activeSubTab === 'literature' ? '#1e293b' : 'transparent'}
          mb="-2px"
          _hover={{
            color: '#1e293b',
            bg: '#f8fafc',
          }}
          transition="all 0.2s"
          onClick={() => setActiveSubTab('literature')}
        >
          Literature Review
        </Box>
      </HStack>

      {/* Content area */}
      <Box color="#1e293b" lineHeight="1.8">
        {activeSubTab === 'synopsis' && (
          <Box>
            <Text fontSize="2xl" fontWeight="semibold" mb={4}>
              Project Synopsis
            </Text>
            <Text color="#64748b" mb={4}>
              This project investigates the asymmetric recovery of Chinese tourism to Thailand following the COVID-19 
              pandemic. While Chinese outbound tourism has rebounded globally, Thailand has experienced a notably slower 
              recovery compared to regional competitors, creating what we term the "Thailand Penalty."
            </Text>
            <Text color="#64748b" mb={4}>
              Using panel data analysis covering 13 destinations from 2005-2024, we employ a Fixed Effects model to 
              quantify this phenomenon while controlling for China's economic slowdown and other confounding factors. 
              Our gravity-style specification isolates destination-specific effects, allowing us to measure the precise 
              magnitude of Thailand's underperformance.
            </Text>
            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Research Questions
            </Text>
            <Box as="ul" pl={6} color="#64748b" mb={4}>
              <Box as="li" mb={2}>
                What is the magnitude of the asymmetric recovery rate between Thailand and its regional competitors?
              </Box>
              <Box as="li" mb={2}>
                What are the empirical determinants of Chinese outbound tourism demand post-pandemic?
              </Box>
              <Box as="li">
                Can we quantify a specific "Thailand Penalty" while controlling for China's economic conditions?
              </Box>
            </Box>
            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Key Findings
            </Text>
            <Text color="#64748b" mb={4}>
              Our analysis reveals statistically significant differences in recovery rates, with Thailand experiencing 
              a measurable penalty relative to competitors. The model controls for visa policies, exchange rates, safety 
              indices, and price levels, isolating the Thailand-specific effect from broader economic trends.
            </Text>
            <Text color="#64748b">
              This research fills a critical gap in the literature by providing quantitative evidence for what has 
              previously been documented only through qualitative surveys and anecdotal comparisons.
            </Text>
          </Box>
        )}
        {activeSubTab === 'journey' && (
          <Box>
            <Text fontSize="2xl" fontWeight="semibold" mb={4}>
              Our Research Journey
            </Text>
            <Text color="#64748b" mb={4}>
              We started out brainstorming what we wanted to analyze in tourism. This was a tumultuous process, as when 
              we started looking into literature, it became very apparent that tourism econometrics is quite a field. As 
              we grew in our understanding of econometric theory, it became easier for us to identify what we could and 
              could not accomplish for this final project.
            </Text>
            
            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Identifying the Gap
            </Text>
            <Text color="#64748b" mb={4}>
              We found a large number of articles written about the lack of rebounding tourism to Thailand from Chinese 
              tourists. As we looked into this, there was a lot written about how significant this difference was, 
              potential reasons why, and potential solutions. We felt though, that it wasn't quantified in the literature 
              nearly well enough, and that there was a lack of evidence with methodological backing for reasons that were 
              listed.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Learning and Exploration
            </Text>
            <Text color="#64748b" mb={4}>
              Our first goal was to get a full picture of what has been done so far. As we did so, we identified a variety 
              of different ways that tourism econometrics has been used in the past for different purposes. We felt that we 
              for sure wanted to run a linear regression, and get hands-on practice with OLS, the standard tests that we 
              learned about in class, and the surrounding skills we gain from this project.
            </Text>
            <Text color="#64748b" mb={4}>
              We wanted to branch further than this though, and to really research other econometric theory. We learned 
              about gradient boosting trees, abnormality testing, time series analysis, panel data analysis, and 
              specifically gravity models used in the context of tourism.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Technical Skills Development
            </Text>
            <Text color="#64748b" mb={4}>
              We also wanted to practice our programming skills, as this felt like a good opportunity to really dive deep 
              and attempt to develop multiple points of value. We web scraped data heavily, we wrestled with Chinese 
              government bot protection, and explored training models for sentiment analysis.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Project Goals
            </Text>
            <Text color="#64748b" mb={3}>
              Given our unique goals, we decided to run multiple different models to identify multiple different aspects 
              of this story we wanted to tell. Our specific objectives included:
            </Text>
            <Box as="ul" pl={6} color="#64748b" mb={4}>
              <Box as="li" mb={2}>Linear regression with OLS estimation</Box>
              <Box as="li" mb={2}>Testing for and addressing heteroskedasticity</Box>
              <Box as="li" mb={2}>Identifying and handling autocorrelation</Box>
              <Box as="li" mb={2}>Testing for multicollinearity</Box>
              <Box as="li" mb={2}>Practicing hypothesis testing (t-tests and F-tests)</Box>
              <Box as="li" mb={2}>Understanding degrees of freedom and sample size requirements</Box>
              <Box as="li" mb={2}>Web scraping and data collection</Box>
              <Box as="li" mb={2}>Data visualization and storytelling</Box>
              <Box as="li">Web development for presenting our findings</Box>
            </Box>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Collaboration and Organization
            </Text>
            <Text color="#64748b">
              We had several meetings with our group, and created a shared Google Drive for collaboration. A Git 
              repository was established to store all relevant code (outside of MATLAB code), ensuring version control 
              and reproducibility of our analysis.
            </Text>
          </Box>
        )}
        {activeSubTab === 'literature' && (
          <Box>
            <Text fontSize="2xl" fontWeight="semibold" mb={4}>
              Literature Review
            </Text>
            
            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              The Asymmetric Recovery Phenomenon
            </Text>
            <Text color="#64748b" mb={4}>
              The post-pandemic recovery of global tourism is easily characterized by confusion, with Southeast Asia 
              experiencing a particularly uneven rebound. While aggregate international arrivals to the region have 
              approached 2019 levels, the recovery of the Chinese outbound tourism market has been asymmetrical. 
              Specifically, Chinese tourism to Thailand is recovering at a much slower rate than it is to other countries.
            </Text>
            <Text color="#64748b" mb={4}>
              Our project looks at quantifying this difference, and using econometric theory that we have learned in this 
              class to determine the effects that select variables have had to cause this difference.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Documented Evidence
            </Text>
            <Text color="#64748b" mb={4}>
              Existing literature has described this phenomenon already. In a report from Sabre Market Intelligence (MIDT), 
              'Travel originating from mainland China has increased by close to 400% overall globally for 2024.' Thailand 
              fell from second place in 2023 to fourth in 2024.
            </Text>
            <Text color="#64748b" mb={4}>
              In determining a methodologically sound way to determine the answers to our questions, we looked at the 
              growing changes in Chinese outbound tourism, along with literature that details the cultural reasonings 
              behind it.
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              The Role of Social Media
            </Text>
            <Text color="#64748b" mb={4}>
              One of the major factors that we have seen detailed in the literature as a change in Chinese tourist behavior, 
              is the increasing importance of social media and the internet. In a micro-econometric study, researchers 
              utilized Structural Equation Modeling (SEM) on a sample of 490 independent Chinese tourists to demonstrate 
              that Perceived Value (PV) and Perceived Cost (PC) are the primary mediators of travel intention.
            </Text>
            <Text color="#64748b" mb={4}>
              Their findings explicitly link Social Media exposure (via WeChat and Douyin) to destination choice, arguing 
              that digital platforms significantly enhance perceived value while simultaneously reducing perceived costs 
              (Fu, Li, and Li 2025).
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              The "Second Wave" of Chinese Tourists
            </Text>
            <Text color="#64748b" mb={4}>
              Perhaps most importantly, we sought out literature on what is changing with Chinese Tourists. In "How tourism 
              markets change: insights from Chinese outbound group and independent travellers," we find several notable 
              conclusions. The market has seen a significant structural change, moving away from a dominance of traditional 
              package group tours toward a preference for independent travel (Huang et al., 2024).
            </Text>
            <Text color="#64748b" mb={4}>
              The authors essentially indicate that there is a "Second Wave" of Chinese outbound tourists, that are younger, 
              more technologically savvy, and have different priorities. This further evidences the importance of social 
              media as a factor influencing tourism.
            </Text>
            <Text color="#64748b" mb={4}>
              The authors also note that for both groups of Chinese outbound tourists—the traditional and this new group—safety 
              is a paramount consideration (Huang et al., 2024).
            </Text>

            <Text fontSize="xl" fontWeight="semibold" mb={3} mt={6}>
              Key Takeaways
            </Text>
            <Box as="ul" pl={6} color="#64748b">
              <Box as="li" mb={2}>
                Chinese outbound tourism has increased 400% globally in 2024, but Thailand's ranking has dropped
              </Box>
              <Box as="li" mb={2}>
                Social media platforms (WeChat, Douyin) significantly influence destination choice and perceived value
              </Box>
              <Box as="li" mb={2}>
                A structural shift from group tours to independent travel is reshaping the market
              </Box>
              <Box as="li" mb={2}>
                Younger, tech-savvy tourists represent a "Second Wave" with different priorities
              </Box>
              <Box as="li">
                Safety remains a paramount concern across all Chinese tourist demographics
              </Box>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  )
}
