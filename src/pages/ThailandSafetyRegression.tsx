
import { useState } from 'react'
import { Box, Text, VStack, Heading, Image, HStack, Link } from '@chakra-ui/react'
import { MdCheckCircle } from 'react-icons/md'
import { LandscapeAnalysisTab } from './LandscapeAnalysisTab'

export function ThailandSafetyRegression() {
    const [activeTab, setActiveTab] = useState('safety_perception')

    return (
        <Box>
            <Heading as="h1" size="xl" mb={6} color="#1e293b">
                Thailand Safety Regression
            </Heading>

            <HStack gap={2} mb={8} borderBottom="2px" borderColor="#e2e8f0" pb={0}>
                <Box
                    px={5}
                    py={3}
                    cursor="pointer"
                    fontWeight={activeTab === 'safety_perception' ? 'semibold' : 'medium'}
                    fontSize="sm"
                    color={activeTab === 'safety_perception' ? '#1e293b' : '#64748b'}
                    borderBottom="3px"
                    borderColor={activeTab === 'safety_perception' ? '#1e293b' : 'transparent'}
                    mb="-2px"
                    _hover={{
                        color: '#1e293b',
                        bg: '#f8fafc',
                    }}
                    transition="all 0.2s"
                    onClick={() => setActiveTab('safety_perception')}
                >
                    Safety Perception Analysis
                </Box>
                <Box
                    px={5}
                    py={3}
                    cursor="pointer"
                    fontWeight={activeTab === 'landscape_analysis' ? 'semibold' : 'medium'}
                    fontSize="sm"
                    color={activeTab === 'landscape_analysis' ? '#1e293b' : '#64748b'}
                    borderBottom="3px"
                    borderColor={activeTab === 'landscape_analysis' ? '#1e293b' : 'transparent'}
                    mb="-2px"
                    _hover={{
                        color: '#1e293b',
                        bg: '#f8fafc',
                    }}
                    transition="all 0.2s"
                    onClick={() => setActiveTab('landscape_analysis')}
                >
                    Landscape Analysis
                </Box>
            </HStack>

            <Box>
                {activeTab === 'safety_perception' && (
                    <VStack align="stretch" gap={6} color="#1e293b">

                        <Text>
                            Throughout our literature review, the perceptions of safety in Thailand among Chinese tourists was cited as a key reason for the decline in Chinese tourists to Thailand (Li, X. & Batra, A, 2023; Sinan He, 2024; Boey 2025; Adith Chairattananon, 2025; Bangkok Post, 2025). There is limited available data on this topic. Data scraping of RedNote is virtually impossible. And large scale survey data is hard to come by.
                        </Text>

                        <Box float={{ base: "none", md: "right" }} ml={{ base: 0, md: 6 }} mb={4} mt={2} display="flex" justifyContent="center">
                            <Image
                                src={`${import.meta.env.BASE_URL}images/safety_regression/Image%201.png`}
                                alt="Dragon Trail Report Data"
                                maxW={{ base: "100%", md: "400px" }}
                                borderRadius="md"
                                boxShadow="md"
                            />
                        </Box>

                        <Text>
                            <Link color="blue.500" href="https://dragontrail.com/wp-content/uploads/sites/6/2025/04/Dragon-Trail-Chinese-Traveler-Sentiment-Report-Spring-2025.pdf" target="_blank" rel="noopener noreferrer">
                                Dragon Trail’s April 2025 report
                            </Link>
                            {' '}suggests that 19% of Chinese outbound tourists view Thailand as a safe destination to travel (Page.13).
                        </Text>

                        <Box float={{ base: "none", md: "right" }} ml={{ base: 0, md: 6 }} mb={4} mt={2} display="flex" justifyContent="center">
                            <Image
                                src={`${import.meta.env.BASE_URL}images/safety_regression/Image%202.png`}
                                alt="Regression Analysis Plot"
                                maxW={{ base: "100%", md: "400px" }}
                                borderRadius="md"
                                boxShadow="md"
                            />
                        </Box>

                        <Text>
                            Sabre’s{' '}
                            <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                                report
                            </Link>
                            {' '}on Chinese outbound tourism in 2024 explains that Thailand has fallen from second place to fourth place in the rank of most popular destinations for travellers from mainland China (Sabre, 2024). We decided to test the correlation between perception of the safety of a country and popularity of that country as a tourist destination for Chinese tourists.
                        </Text>

                        <Box borderTop="1px" borderColor="gray.200" my={4} style={{ clear: 'both' }} />



                        <Text>
                            We checked for homoscedasticity and found it using the following Q-Q plot.
                        </Text>


                        <Box float={{ base: "none", md: "right" }} ml={{ base: 0, md: 6 }} mb={4} mt={2} display="flex" justifyContent="center">
                            <Image
                                src={`${import.meta.env.BASE_URL}images/safety_regression/Image%203.png`}
                                alt="Q-Q Plot 1"
                                maxW={{ base: "100%", md: "300px" }}
                                borderRadius="md"
                                boxShadow="md"
                            />
                        </Box>
                        <Text>
                            This is the resulting data. The R<sup>2</sup> value demonstrates that about 15% of the popularity rank is associated with safety perception. Notably, the p-value is not statistically significant. Because of the small sample size, the standard errors increase which impacts our p-value.
                        </Text>
                        <Box float={{ base: "none", md: "right" }} ml={{ base: 0, md: 6 }} mb={4} mt={2} display="flex" justifyContent="left">
                            <Image
                                src={`${import.meta.env.BASE_URL}images/safety_regression/Image%204.png`}
                                alt="Q-Q Plot 2"
                                maxW={{ base: "100%", md: "300px" }}
                                borderRadius="md"
                                boxShadow="md"
                            />
                        </Box>
                        <Text style={{ clear: 'both' }}>
                            While, ultimately, we cannot give statistical evidence for a correlation between the Chinese perception of how safe a country is and the popularity of that destination for Chinese tourists, we cannot suggest that there is no correlation. Certainly, the literature opposes this view.
                        </Text>

                        <Box>
                            <Heading as="h3" size="md" mb={2}>Limitations of this regression:</Heading>
                            <VStack align="start" gap={2}>
                                <HStack>
                                    <Box as={MdCheckCircle} color="green.500" />
                                    <Text>Small sample size.</Text>
                                </HStack>
                                <HStack>
                                    <Box as={MdCheckCircle} color="green.500" />
                                    <Text>The popularity and safety perception data are from 2024 and 2025 respectively. Ideally, they would be from the same time period.</Text>
                                </HStack>
                            </VStack>
                        </Box>

                        <Box borderTop="1px" borderColor="gray.200" my={8} />

                        <Box>
                            <Heading as="h2" size="lg" mb={4}>Bibliography</Heading>
                            <VStack align="stretch" gap={3} fontSize="sm" color="gray.600">
                                <Text>
                                    Sinan He (2024) <i>Survey on Chinese tourists’ perception with the safety of consumption places environment in Bangkok</i>. Masters thesis, Chulalongkorn University. DOI: 10.58837/CHULA.THE.2024.381. <Link color="blue.500" href="https://digital.car.chula.ac.th/chulaetd/12639/" target="_blank" rel="noopener noreferrer">Link</Link>
                                </Text>
                                <Text>
                                    Adith Chairattananon (2025) ‘Safety Concerns Knock Thailand Off Top Spot for Chinese Tourists’. <i>The Nation</i>. Available at: <Link color="blue.500" href="https://www.nationthailand.com/news/tourism/40056015" target="_blank" rel="noopener noreferrer">https://www.nationthailand.com/news/tourism/40056015</Link>
                                </Text>
                                <Text>
                                    Bangkok Post (2025) ‘Chinese flock to Vietnam due to Thailand safety fears’. Available at: <Link color="blue.500" href="https://www.bangkokpost.com/thailand/general/3109744/chinese-flock-to-vietnam-due-to-thailand-safety-fears" target="_blank" rel="noopener noreferrer">https://www.bangkokpost.com/thailand/general/3109744/chinese-flock-to-vietnam-due-to-thailand-safety-fears</Link>
                                </Text>
                                <Text>
                                    Boey, C. (2025) ‘Thailand faces safety concerns from Chinese travellers despite positive trends’. <i>TTG Asia</i>. Available at: <Link color="blue.500" href="https://www.ttgasia.com/2025/05/05/thailand-faces-safety-concerns-from-chinese-travellers-despite-positive-trends/" target="_blank" rel="noopener noreferrer">Link</Link>
                                </Text>
                                <Text>
                                    Li, X. & Batra, A. (2023) ‘A Study on Chinese Tourists’ Perception of Violence and Crime Risk in Thailand’. <i>AU-HIU International Multidisciplinary Journal</i>, 3(2), 49–57. Available at: <Link color="blue.500" href="https://assumptionjournal.au.edu/index.php/auhiu/article/view/7450" target="_blank" rel="noopener noreferrer">Link</Link>
                                </Text>
                                <Text>
                                    Sabre (2024). China Unleashed: Sabre reveals key outbound Chinese travel insights for 2024. Sabre. <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">Link</Link>
                                </Text>
                                <Text>
                                    Tian, T., Meng, J. (2025). Chinese Traveler Sentiment Report: Spring 2025. Retrieved from <Link color="blue.500" href="https://dragontrail.com/wp-content/uploads/sites/6/2025/04/Dragon-Trail-Chinese-Traveler-Sentiment-Report-Spring-2025.pdf" target="_blank" rel="noopener noreferrer">Link</Link>
                                </Text>
                            </VStack>
                        </Box>

                    </VStack>
                )}
                {activeTab === 'landscape_analysis' && (
                    <LandscapeAnalysisTab />
                )}
            </Box>
        </Box>
    )
}
