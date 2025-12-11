import { Box, Text, VStack, Heading, Image, Link } from '@chakra-ui/react'

export function LandscapeAnalysisTab() {
    return (
        <VStack align="stretch" gap={6} color="#1e293b">
            <Heading as="h2" size="lg">Country comparison landscape analysis & variable identification</Heading>

            <Text>
                Thailand is competing with other countries for Chinese tourists, making these countries substitute goods for a trip to Thailand. Substitute goods are a key element of the demand function. By investigating these countries, we can identify the reasoning behind relatively reduced demand for Thailand by Chinese tourists since 2023.
            </Text>

            <Text>
                <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                    Sabre
                </Link>
                {' '}has released the thirty most popular destinations for outbound travellers from China in 2023 and 2024 ({' '}
                <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                    Sabre, 2024
                </Link>
                ). The 29 other countries in this list are Thailand’s competitors. By analysing the countries on this list, we can see what the differentiating factors may be. Thailand fell from second place in 2023 to fourth in 2024.{' '}
                <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                    Sabre
                </Link>
                {' '}(2024) states that: ‘Travel originating from mainland China has increased by close to 400% overall globally for 2024.’ We can see from the below infographic ({' '}
                <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                    Sabre, 2024
                </Link>
                ) that Chinese tourists to Thailand were actually up 339%. This is still less than the 400% we would expect.
            </Text>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%201.png`}
                    alt="Sabre Infographic"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text>
                Many countries experienced higher than this 400%: including Korea, Japan, Hong Kong, Australia, Singapore, Malaysia, Indonesia, Macao, the UK, Laos, Russia, New Zealand, India, Kazakhstan and Bangladesh ({' '}
                <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                    Sabre, 2024
                </Link>
                ).
            </Text>

            <Text>
                This regression compares Thailand in 2024 to these other countries using a series of metrics. It is a cross-sectional study. The dependent variable is the rank for the most popular destinations for travellers from mainland China for 2024. ‘1’ signifies the most popular destination for Chinese tourists.
            </Text>

            <Text>
                Factors that may influence Chinese tourists to choose other countries over Thailand were identified through a literature review. Relevant data sets were then sourced to analyse these factors.
            </Text>

            <Text fontStyle="italic">
                Note: This regression is for countries in an annual period. Thus, seasonal changes have not been adjusted for.
            </Text>

            <Heading as="h3" size="md" mt={4}>Visa policy</Heading>

            <Text>
                <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">
                    Sabre
                </Link>
                {' '}(2024) gives us some insight into why the growth in Chinese tourism to Singapore may be influenced by visa policy. “China recently signed a mutual agreement on 30-day visa-free travel with Singapore, which became effective from February 9th, allowing entry for business, travel, leisure, and sightseeing. Thailand and China agreed to a similar arrangement, effective March 1st to replace a temporary visa suspension which ended in February. Thailand immediately felt the benefit of the arrangement in 2023 but has dropped a little in the rankings as more agreements come in place, giving travellers more choice.”
            </Text>

            <Text>
                This{' '}
                <Link color="blue.500" href="http://mi.mbd.baidu.com/r/1NvzVTtPV04?f=cp&rs=602329212&ruk=UokDaz1ihng_T1Wi4rwOMw&u=1b626b39ac8294e4" target="_blank" rel="noopener noreferrer">
                    data
                </Link>
                {' '}is collected from May 2025 ({' '}
                <Link color="blue.500" href="http://mi.mbd.baidu.com/r/1NvzVTtPV04?f=cp&rs=602329212&ruk=UokDaz1ihng_T1Wi4rwOMw&u=1b626b39ac8294e4" target="_blank" rel="noopener noreferrer">
                    Shandong Zhongpiao Aviation Service, 2025
                </Link>
                ). Although this is later than our other data, it is the closest proxy variable we have to visa rules as of 2024, given that policy is reasonably stable over time. For this we have used a dummy variable where 2 = visa free, 1 = visa on arrival, 0 = transit exemption or visa required. Ordinal dummy variables are difficult to work with. However, given there are three elements, it is logical to order them this way. This variable setup problematically assumes an equal difference between no visa arrangement, a visa on arrival and no visa needed. It is feasible that a visa on arrival may be much closer or further to not needing a visa compared to having no visa arrangement. Our categorisation does not account for this limitation.
            </Text>

            <Text>
                Furthermore, some countries offer visa-free travel to Chinese tourists for 30 days, whereas some offer them for 60 or 90 days. This difference was not accounted for. Chinese tourists stay an average of 8 days ({' '}
                <Link color="blue.500" href="https://www.visa.co.th/en_TH/about-visa/newsroom/press-releases/thailand-tourism-to-be-boosted-by-repeat-travellers-visa-study.html" target="_blank" rel="noopener noreferrer">
                    Visa
                </Link>
                , 2023). We can, therefore, assume that visa free travel for 30 days or 60 days is unlikely to make an impact on the travel patterns of outbound Chinese tourists.
            </Text>

            <Heading as="h3" size="md" mt={4}>Cultural experiences</Heading>

            <Text>
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                {' '}(2014) focused on Chinese tourists visiting a specific region of Australia, but also drew on previous studies about Chinese tourists visiting the USA and Canada providing many variable suggestions with theoretical backing stemming from these papers. It emphasises how Chinese tourists value their destination’s culture. In the literature review of this paper ({' '}
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                , 2014, Pg.45), immersion in culture was a key factor identified by Chinese tourists. Interestingly, they investigate the impact of this factor on the travel decisions of different types of Chinese travellers. For example, Chinese travellers with less travel experience were more likely to go to neighbouring countries, due to the culture being more familiar ({' '}
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                , 2014, Pg.47). Thus, Thailand may be able to appeal to Chinese travellers with less experience by promoting Thai culture so that it is more familiar to Chinese citizens. This paper also found that ‘as people accumulate travel experience, the motivation of seeking cultural experiences becomes stronger’ ({' '}
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                , 2014, Pg.48). Thus, investing in rich cultural experience infrastructure may appeal to Chinese tourists with extensive travel experience.
            </Text>

            <Text>
                Identifying a proxy variable for cultural experiences is challenging. US News ({' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings" target="_blank" rel="noopener noreferrer">
                    US News, 2024
                </Link>
                {' '}A) creates{' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings" target="_blank" rel="noopener noreferrer">
                    country rankings
                </Link>
                {' '}based on a large global survey. A limitation of these variables is the fact that survey methodology is used. Thus, people self-select as participants. Over half of those surveyed were college-educated and read/watch the news at least four days a week ({' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/articles/methodology" target="_blank" rel="noopener noreferrer">
                    US News, 2024 B
                </Link>
                ). These are subjective questions so demographics matter as they influence perception. However, due to the inherent subjectivity of cultural experiences and the absence of more suitable data sets, we have decided to test using these proxy variables.
            </Text>

            <Text>
                The Heritage Index was found to more closely adhere to the findings of the literature review than the Cultural Influence Index. The Heritage Index is made up of the following components: culturally accessible, has a rich history, has great food, many cultural attractions and many geographical attractions.
            </Text>

            <Text>
                The following data sets from their survey were identified as suitable proxy variables for this analysis:{' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/culturally-accessible" target="_blank" rel="noopener noreferrer">
                    culturally accessible
                </Link>
                {' '}and{' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/many-cultural-attractions" target="_blank" rel="noopener noreferrer">
                    many cultural attractions
                </Link>
                . These serve as proxy variables for cultural experiences.
            </Text>

            <Text>
                According to{' '}
                <Link color="blue.500" href="https://www.academia.edu/85749472/International_Tourists_Travel_Motivation_By_Push_Pull_Factors_And_The_Decision_Making_For_Selecting_Thailand_As_Destination_Choice" target="_blank" rel="noopener noreferrer">
                    Yiamjanya and Wongleedee
                </Link>
                {' '}(2014), Thai food is the main pull factor for tourists to Thailand. US News has a{' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/great-food" target="_blank" rel="noopener noreferrer">
                    food index
                </Link>
                {' '}which sets a subjective ranking for which countries have the best food. Notably, this survey was global. Chinese tastes may differ. There are many individual opinions of what may be the most appealing cuisine to Chinese people, however, there is no large-scale data. Thus, the closest data we have is that of general world preferences for cuisines, which US News provides.
            </Text>

            <Text>
                <Link color="blue.500" href="https://www.researchgate.net/publication/341327179_COVID-19_potential_effects_on_Chinese_citizens'_lifestyle_and_travel" target="_blank" rel="noopener noreferrer">
                    Wen et al.
                </Link>
                {' '}(2020) measured increased desire for nature-based tourism in the post-pandemic era. While nature is not quantifiable at a country level, we have identified ‘
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/many-geographic-attractions" target="_blank" rel="noopener noreferrer">
                    many geographical attractions
                </Link>
                ’ (US News, 2024 C). We could also use the ‘
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/scenic" target="_blank" rel="noopener noreferrer">
                    scenic
                </Link>
                ’ index but this introduces high multicollinearity so we removed it from the regression during the refining stage.
            </Text>

            <Text>
                While the initial iteration of our regression did include these indexes as separate variables so that their individual impact could be measured, the perception indexes were ultimately found to be highly collinear so the composite index was used.
            </Text>

            <Heading as="h3" size="md" mt={4}>Safety & Relaxation</Heading>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%206.png`}
                    alt="Safety and Relaxation"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text>
                Safety is a prerequisite for relaxation.{' '}
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                {' '}(2014) explains that relaxing is a key motivation for travelling. Furthermore, 64% of those surveyed for the Dragon Trail report ({' '}
                <Link color="blue.500" href="https://dragontrail.com/wp-content/uploads/sites/6/2025/04/Dragon-Trail-Chinese-Traveler-Sentiment-Report-Spring-2025.pdf" target="_blank" rel="noopener noreferrer">
                    Tian et al, 2025
                </Link>
                , Page.10) said relaxation was their main purpose for travelling abroad. Perceptions of safety improved for almost every destination included the Dragon Trail report, except Thailand. Perceptions of the safety of Thailand decreased ({' '}
                <Link color="blue.500" href="https://dragontrail.com/wp-content/uploads/sites/6/2025/04/Dragon-Trail-Chinese-Traveler-Sentiment-Report-Spring-2025.pdf" target="_blank" rel="noopener noreferrer">
                    Tian et al, 2025
                </Link>
                ). This may contribute to the relative decrease in Chinese tourists to Thailand.
            </Text>

            <Text>
                Since the Covid-19 pandemic, Chinese tourists have been increasingly concerned about safety overseas due to a rise in discrimination ({' '}
                <Link color="blue.500" href="https://www.researchgate.net/publication/341327179_COVID-19_potential_effects_on_Chinese_citizens'_lifestyle_and_travel" target="_blank" rel="noopener noreferrer">
                    Wen et al.
                </Link>
                , 2020). 41% of Chinese travellers are most concerned about safety when booking a trip, more than any other factor ({' '}
                <Link color="blue.500" href="https://dragontrail.com/wp-content/uploads/sites/6/2025/04/Dragon-Trail-Chinese-Traveler-Sentiment-Report-Spring-2025.pdf" target="_blank" rel="noopener noreferrer">
                    Tian et al,
                </Link>
                Page. 18).
            </Text>

            <Text>
                The global peace index is a measure which compares countries on how safe they are ({' '}
                <Link color="blue.500" href="https://www.visionofhumanity.org/wp-content/uploads/2023/06/GPI-2023-Web.pdf" target="_blank" rel="noopener noreferrer">
                    IPE, 2023
                </Link>
                ). The data is collected and weighted by a team of experts. It accounts for factors such as the homicide rate, incarceration rate, violent crime, weapons exports, etc. While each of these factors individually may not impact tourism directly, the combination of them directly impacts the global perception of the safety of each country. Chinese tourists respond to perceived safety, often shaped by media and online narratives.
            </Text>

            <Heading as="h3" size="md" mt={4}>Wellness</Heading>

            <Text>
                <Link color="blue.500" href="https://www.researchgate.net/publication/341327179_COVID-19_potential_effects_on_Chinese_citizens'_lifestyle_and_travel" target="_blank" rel="noopener noreferrer">
                    Wen et al.
                </Link>
                {' '}(2020) also noted an increased emphasis on travel in pursuit of wellness activities. The Global Wellness Institute ({' '}
                <Link color="blue.500" href="https://globalwellnessinstitute.org/wp-content/uploads/2025/02/2025_GWI-Country-Rankings_022125.pdf" target="_blank" rel="noopener noreferrer">
                    GWI, 2025
                </Link>
                ) has data on the size of the wellness industry in countries. It is measured by spending in billions of US dollars. One key limitation of this study is that it is not indexed for purchasing power. To illustrate the effects of this, imagine investing the same amount of money in the wellness industry in the UK and in Malaysia. The resulting quality of products and services will differ hugely. Thus, it is not a perfect measure.
            </Text>

            <Text>
                Therefore, we indexed the Wellness Industry for{' '}
                <Link color="blue.500" href="https://www.worlddata.info/cost-of-living.php?full" target="_blank" rel="noopener noreferrer">
                    cost of living
                </Link>
                {' '}in order to better approximate the quality of the resulting services after the initial investment in the industry.
            </Text>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%208.png`}
                    alt="Wellness Industry"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Heading as="h2" size="lg" mt={8}>Identified but excluded variables, with justifications</Heading>

            <Heading as="h4" size="sm" mt={4}>Friendliness</Heading>

            <Text>
                A quarter of Chinese tourists to Thailand in 2023 intended to revisit in the next 12 months ({' '}
                <Link color="blue.500" href="https://www.visa.co.th/en_TH/about-visa/newsroom/press-releases/thailand-tourism-to-be-boosted-by-repeat-travellers-visa-study.html" target="_blank" rel="noopener noreferrer">
                    Visa
                </Link>
                , 2023). This repeat tourism, therefore, has a huge impact on the number of Chinese tourists in Thailand every year. Tourist satisfaction leads directly to repeat visits. Behind only the attributes (landscape, amenities, attractions) of a place, the second most important determinant of tourist satisfaction is “friendliness of local people” ({' '}
                <Link color="blue.500" href="https://www.researchgate.net/publication/350489492_Determinants_of_Tourist_Satisfaction_and_Dissatisfaction_on_Tourism_Village" target="_blank" rel="noopener noreferrer">
                    Sari, 2021
                </Link>
                ).
            </Text>

            <Text>
                Thailand capitalised on its reputation for friendliness in the 1960s, launching its first economic development plan. In this, it adopted a tourism marketing strategy whereby it used the slogan ‘Siam, the Land of Smiles’ ({' '}
                <Link color="blue.500" href="https://www.nationthailand.com/life/art-culture/40053526" target="_blank" rel="noopener noreferrer">
                    Adair, 2025
                </Link>
                ). Friendliness may capture intangible soft-power aspects that influence Chinese satisfaction. While friendliness is highly subjective, US News has a ranking for it ({' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/friendly" target="_blank" rel="noopener noreferrer">
                    US News, 2024 C
                </Link>
                ). Unfortunately, this variable is highly collinear with the Heritage Index. Running the same regression with the Heritage Index swapped out for the Friendliness Index found that the Heritage Index created a higher R<sup>2</sup> value and a lower P-Value. For this reason, the Heritage Index was found to be a more suitable variable to measure.
            </Text>


            <Heading as="h4" size="sm" mt={4}>Purchasing power</Heading>

            <Text>
                Of course, in order to travel to Thailand, Chinese people must have the financial means to do so. World Data has a cost of living index based on the OECD data, IMF data, World bank data and European Commission ({' '}
                <Link color="blue.500" href="https://www.worlddata.info/cost-of-living.php?full" target="_blank" rel="noopener noreferrer">
                    worlddata.info, 2025
                </Link>
                ). It adjusts for income in the country but we have not done this because we assume the income across Chinese tourists and not citizens of that country. Thus, we initially created a variable: cost of living. This measure is intended for residents so it uses a ‘normal basket of goods’, rather than a tourist. Tourists consume different goods. However, the hotel and restaurant price index ({' '}
                <Link color="blue.500" href="https://www.theglobaleconomy.com/rankings/hotel_and_restaurant_prices_wb/" target="_blank" rel="noopener noreferrer">
                    The Global Economy, 2021
                </Link>
                ). The most recent available data is 2021. Other, more recent, data exists but it is focused on cities rather than national data ({' '}
                <Link color="blue.500" href="https://www.freetour.com/blog/average-hotel-room-prices-around-the-world" target="_blank" rel="noopener noreferrer">
                    Dubakova, 2025
                </Link>
                ;{' '}
                <Link color="blue.500" href="https://www.expedia.com/newsroom/hotels-com-2025-hotel-price-index/" target="_blank" rel="noopener noreferrer">
                    Newsroom, 2025
                </Link>
                ). Ultimately, this variable was excluded due to a lack of an appropriate proxy variable.
            </Text>

            <Heading as="h4" size="sm" mt={4}>Transportation costs</Heading>

            <Text>
                The law of demand tells us that, for normal goods, demand increases as price decreases. Thus, to investigate the change in demand, we must look at the price of a trip to Thailand.
            </Text>

            <Text>
                <Link color="blue.500" href="https://www.academia.edu/4234649/Who_visits_Thailand_and_Why_WBRC_Bangkok_Webb_and_Chotithamwattana_2" target="_blank" rel="noopener noreferrer">
                    Webb and Chotithamwattana
                </Link>
                {' '}(2011) uses econometric forecasting models to decompose the tourist visitation patterns for Thailand for the years of 1995-2011. It uses transport costs to Thailand as a variable. This makes intuitive sense as a consumer under the law of demand. This is a complex factor given that it depends where in China they are flying from, and where in the target country they are flying to. Thus, absent this information, we were unable to find sufficient data to include in our model.
            </Text>

            <Heading as="h4" size="sm" mt={4}>Prestige</Heading>

            <Text>
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                {' '}(2014) conducts a literature review which concludes that prestige is an important factor for Chinese tourists in deciding where to visit. However, the research conducted by the paper shows (through table 3) that prestige was relatively unimportant to survey respondents. Given the lack of consensus, we decided to include this in our regression to test for significance. US News has an index which functions as proxy variables for this:{' '}
                <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/prestigious" target="_blank" rel="noopener noreferrer">
                    prestige
                </Link>
                . However, these perception indexes turned out to be highly collinear, so this variable was ultimately excluded from the final regression.
            </Text>

            <Heading as="h4" size="sm" mt={4}>Shopping</Heading>

            <Text>
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                {' '}(2014) and{' '}
                <Link color="blue.500" href="https://www.researchgate.net/publication/283179233_Factors_Influencing_International_Visitors_to_Revisit_Bangkok_Thailand" target="_blank" rel="noopener noreferrer">
                    Thiumsak and Ruangkanjanases
                </Link>
                {' '}(2016) identified shopping as a key reason for travelling among Chinese citizens.{' '}
                <Link color="blue.500" href="https://www.sciencedirect.com/science/article/pii/S1447677014000072" target="_blank" rel="noopener noreferrer">
                    Zhang et al.
                </Link>
                {' '}(2014) identifies both inexpensive shopping and shopping malls as variables. It thus recommends ‘shopping markets should remain unique as this would emphasize Thailand’s unique selling proposition’ and attract more Chinese tourists.
            </Text>

            <Text>
                <Link color="blue.500" href="https://ceoworld.biz/2025/05/12/revealed-the-worlds-best-cities-for-shopping-2025/" target="_blank" rel="noopener noreferrer">
                    CEOWorld
                </Link>
                {' '}surveyed “1,200 global experts” on which cities are the best for shopping ({' '}
                <Link color="blue.500" href="https://ceoworld.biz/2025/05/12/revealed-the-worlds-best-cities-for-shopping-2025/" target="_blank" rel="noopener noreferrer">
                    Wilson, 2025
                </Link>
                ). They ranked them based on the following factors: “(1) Variety: major shopping centers, designers, quantity of upscale shops, shopping malls, boutique retailers, number of available brands, and a little-known antiques shop; (2) Friendliness: city beauty, quality of window displays, shop decor, staff friendliness, city dining experience, and accommodation options; (3) Value for money: bargain opportunities like sale seasons and average prices.”
            </Text>

            <Text>
                Given how limited the data is and the nature of the data as city rather than country meant that we could not include it in our final regression analysis without sacrificing both accuracy and degrees of freedom.
            </Text>


            <Heading as="h3" size="md" mt={4}>Limitation</Heading>
            <VStack align="start" pl={4}>
                <Text>1. This regression does not take into consideration post Covid lags in recovery. This is addressed in the other model within this project.</Text>
                <Text>2. The sample size is extremely small.</Text>
            </VStack>

            <Box borderTop="1px" borderColor="gray.200" my={4} />

            <Heading as="h2" size="lg" mt={8}>Creating the function</Heading>
            <Text fontWeight="bold">T = f(V, H, P, W)</Text>
            <Text>T = Rank for number of Chinese tourists to this country in 2024</Text>
            <Text>V = Visa needs (2 = visa free, 1 = visa on arrival, 0 = transit exemption or visa required)</Text>
            <Text>H = Culturally accessible & has a rich history & has great food & has many cultural attractions & has many geographical attractions</Text>
            <Text>P = Safety and Relaxation</Text>
            <Text>W = Wellness industry</Text>

            <Heading as="h3" size="md" mt={4}>Final data sources</Heading>

            <Box overflowX="auto">
                <Box as="table" width="100%" style={{ borderCollapse: 'collapse' }}>
                    <Box as="thead" bg="gray.50">
                        <Box as="tr">
                            <Box as="th" p={2} borderBottom="1px" borderColor="gray.200" textAlign="left">Variable</Box>
                            <Box as="th" p={2} borderBottom="1px" borderColor="gray.200" textAlign="left">Link to source</Box>
                            <Box as="th" p={2} borderBottom="1px" borderColor="gray.200" textAlign="left">Year of data</Box>
                            <Box as="th" p={2} borderBottom="1px" borderColor="gray.200" textAlign="left">Organisation</Box>
                            <Box as="th" p={2} borderBottom="1px" borderColor="gray.200" textAlign="left">Methodology</Box>
                        </Box>
                    </Box>
                    <Box as="tbody">
                        <Box as="tr">
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Rank for popularity</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">Sabre Report</Link></Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">2024</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Sabre</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Unclear</Box>
                        </Box>
                        <Box as="tr">
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Heritage rank</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/heritage" target="_blank" rel="noopener noreferrer">US News Heritage</Link></Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">2024</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">US News</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://www.usnews.com/news/best-countries/articles/methodology" target="_blank" rel="noopener noreferrer">Methodology</Link></Box>
                        </Box>
                        <Box as="tr">
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Safety and Relaxation</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://www.economicsandpeace.org/wp-content/uploads/2024/06/GPI-2024-web.pdf" target="_blank" rel="noopener noreferrer">GPI Report</Link></Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">2024</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Institute for Economics and Peace</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://globalwellnessinstitute.org/wp-content/uploads/2025/02/2025_GWI-Country-Rankings_022125.pdf" target="_blank" rel="noopener noreferrer">GWI Methodology</Link></Box>
                        </Box>
                        <Box as="tr">
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Wellness industry</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://globalwellnessinstitute.org/wp-content/uploads/2025/02/2025_GWI-Country-Rankings_022125.pdf" target="_blank" rel="noopener noreferrer">GWI Report</Link></Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">2023</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Global Wellness Institute</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Page 11 of GWI Report</Box>
                        </Box>
                        <Box as="tr">
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">Cost of living</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://www.worlddata.info/cost-of-living.php?full" target="_blank" rel="noopener noreferrer">World Data</Link></Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">2024</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100">World Data</Box>
                            <Box as="td" p={2} borderBottom="1px" borderColor="gray.100"><Link color="blue.500" href="https://www.worlddata.info/cost-of-living.php?full" target="_blank" rel="noopener noreferrer">Methodology</Link></Box>
                        </Box>
                    </Box>
                </Box>
            </Box>

            <Box display="flex" justifyContent="center" mt={4}>
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%2012.png`}
                    alt="Data Sources"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Heading as="h3" size="md" mt={4}>Areas for further research</Heading>

            <Text>
                Throughout this project, we noted an absence of vital data to accurately complete this regression. Further research is suggested for the following areas in order to properly estimate the reasoning for a decrease in Chinese tourists to Thailand in 2025:
            </Text>

            <VStack align="start" pl={4}>
                <Text>1. Chinese perceptions of cultural experiences in countries around the world.</Text>
                <Text>2. Chinese perceptions of food in countries around the world.</Text>
                <Text>3. Chinese perceptions of the safety of countries around the world.</Text>
                <Text>4. Chinese perceptions of the friendliness of countries around the world.</Text>
                <Text>5. Hotel price index at a country level.</Text>
                <Text>6. Restaurant price index at a country level.</Text>
            </VStack>

            <Box borderTop="1px" borderColor="gray.200" my={4} />

            <Heading as="h2" size="lg" mt={8}>Refining the regression</Heading>

            <Text>
                The data was cleaned by checking for outliers, filling in any black cells, correcting for any errors in inputting, etc.
            </Text>

            <Text>
                This data was then run through Excel. There were many iterations of this regression. Checking VIF figures and Q-Q plots showed us whether the regression was valid by ensuring our underlying assumptions were correct. One such iteration of the regression is visible below. Notably, the R<sup>2</sup> figure is much higher than our final regression. This is because the high multicollinearity present in this regression has inflated the R<sup>2</sup> value.
            </Text>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%209.png`}
                    alt="Regression Iteration"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Box borderTop="1px" borderColor="gray.200" my={4} />

            <Heading as="h2" size="lg" mt={8}>The final regression</Heading>

            <Text>
                In running a linear regression, we assume that no variables are collinear. To check for multicollinearity, we tested for the Variable Inflation Factor (VIF) of each of the variables. A figure of 1 is considered perfectly independent, and a figure of 5 is considered problematically collinear.
            </Text>

            <Text fontWeight="bold">Safety VIF</Text>
            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%2010.png`}
                    alt="Safety VIF"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text fontWeight="bold">Visa VIF</Text>
            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%2011.png`}
                    alt="Visa VIF"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text fontWeight="bold">Wellness VIF</Text>
            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%205.png`}
                    alt="Wellness VIF"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text fontWeight="bold">Heritage VIF</Text>
            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%207.png`}
                    alt="Heritage VIF"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text>
                Taking the R<sup>2</sup> values from each of these regressions, we can create the following table. We can then use the VIF formula which is VIF= 1/(1-R<sup>2</sup>).
            </Text>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%203.png`}
                    alt="VIF Formula"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text>
                These VIF results are all very low so we can confirm that we have no multicollinearity in our model.
            </Text>

            <Text>
                The normality of the regression residuals is critical. We tested this by creating a Q-Q chart in Excel. In row A, we had the residuals ordered from smallest to largest. In row B, we had the formula =(ROW(A1)-0.5)/25 and in row C we had =NORM.S.INV(B1). This created a Q-Q chart. A 45 degree line shows normally distributed residuals.
            </Text>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%202.png`}
                    alt="Q-Q Chart"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text>
                We have noticed no issues in the regression. Thus, we are satisfied with the model selection.
            </Text>

            <Box borderTop="1px" borderColor="gray.200" my={4} />

            <Heading as="h2" size="lg" mt={8}>Conclusion</Heading>

            <Text>
                Our final regression results were the following:
            </Text>

            <Box display="flex" justifyContent="center">
                <Image
                    src={`${import.meta.env.BASE_URL}images/main_ols_regression/Image%204.png`}
                    alt="Final Regression Results"
                    maxW="600px"
                    borderRadius="md"
                    boxShadow="md"
                />
            </Box>

            <Text>
                We note that approximately 30% of the change in rank is correlated to the heritage ranking, peace index, visa status and adjusted wellness industry. Notably, none of the p-values are statistically significant. Because of the small sample size, the standard errors increase which impacts our p-value. From this, we can say that we did not find evidence for an effect of any variable under the sample, model, proxy variables and assumptions we used. If we were to use the true variables instead of the proxy variables, we would have a much more accurate statistical analysis. Thus, further research is advisable.
            </Text>

            <Text>
                Further statistical analysis is required to investigate the relationship between the independent and dependent variables identified in this study.
            </Text>

            <Box borderTop="1px" borderColor="gray.200" my={4} />

            <Heading as="h2" size="lg" mt={8}>Bibliography</Heading>

            <Text fontSize="sm" color="gray.600">
                Adair, S (2025). <Text as="span" fontStyle="italic">Postwar Charm to PR Strategy: Why Thailand is Known as the Land of Smiles.</Text> [online] Available at: <Link color="blue.500" href="https://www.nationthailand.com/life/art-culture/40053526" target="_blank" rel="noopener noreferrer">https://www.nationthailand.com/life/art-culture/40053526</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Dubakova, A (2025). <Text as="span" fontStyle="italic">Average hotel room prices around the world.</Text> [online] Available at: <Link color="blue.500" href="https://www.freetour.com/blog/average-hotel-room-prices-around-the-world" target="_blank" rel="noopener noreferrer">https://www.freetour.com/blog/average-hotel-room-prices-around-the-world</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                GWI (2025). <Text as="span" fontStyle="italic">The Global Wellness Economy: Country Rankings.</Text> [online] Available at: <Link color="blue.500" href="https://globalwellnessinstitute.org/wp-content/uploads/2025/02/2025_GWI-Country-Rankings_022125.pdf" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                nationthailand (July 7th, 2025). <Text as="span" fontStyle="italic">Chinese Tourist Numbers to Thailand Plummet 34%, Industry Awaits Recovery.</Text> [online] nationthailand. Available at: <Link color="blue.500" href="https://www.nationthailand.com/news/tourism/40052231" target="_blank" rel="noopener noreferrer">https://www.nationthailand.com/news/tourism/40052231</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                nationthailand (July 9th, 2025). <Text as="span" fontStyle="italic">Thailand’s tourism struggles as Chinese visitors decline, experts urge focus on new opportunities.</Text> [online] nationthailand. Available at: <Link color="blue.500" href="https://www.nationthailand.com/news/tourism/40052350" target="_blank" rel="noopener noreferrer">https://www.nationthailand.com/news/tourism/40052350</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Newsroom (2025). <Text as="span" fontStyle="italic">Hotel Price Index 2025.</Text> [online] Available at: <Link color="blue.500" href="https://www.expedia.com/newsroom/hotels-com-2025-hotel-price-index/" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                IPE (2023). <Text as="span" fontStyle="italic">Global Peace Index 2023.</Text> [online]. Available at: <Link color="blue.500" href="https://www.visionofhumanity.org/wp-content/uploads/2023/06/GPI-2023-Web.pdf" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Sabre (2023). <Text as="span" fontStyle="italic">Reopening China: Sabre data indicates significant outbound travel rebound despite high air fares, as China begins to re-open to the world.</Text> [online] Sabre Asia Pacific. Available at: <Link color="blue.500" href="https://www.sabre.com/locations/apac/reopening-china-sabre-data-indicates-significant-outbound-travel-rebound-despite-high-air-fares-as-china-begins-to-re-open-to-the-world/" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Sabre (2024). <Text as="span" fontStyle="italic">China Unleashed: Sabre reveals key outbound Chinese travel insights for 2024.</Text> Sabre. <Link color="blue.500" href="https://www.sabre.com/insights/china-unleashed-sabre-reveals-key-outbound-chinese-travel-insights-for-2024/" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Sari, P.I., Lestari, Y.D. (2021). <Text as="span" fontStyle="italic">Determinants of Tourist Satisfaction and Dissatisfaction on Tourism Village.</Text> urnal Pendidikan Ekonomi Dan Bisnis (JPEB) 9(1):09-24.
            </Text>

            <Text fontSize="sm" color="gray.600">
                Shandong Zhongpiao Aviation Service (2025). <Text as="span" fontStyle="italic">2025 List of Visa Free Countries for Chinese Passports.</Text> [online]
            </Text>

            <Text fontSize="sm" color="gray.600">
                The Global Economy (2021). <Text as="span" fontStyle="italic">Hotel and restaurant prices - Country rankings.</Text> [online]. Available at: <Link color="blue.500" href="https://www.theglobaleconomy.com/rankings/hotel_and_restaurant_prices_wb/" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Tian, T., Meng, J. (2025). <Text as="span" fontStyle="italic">Chinese Traveler Sentiment Report: Spring 2025.</Text> Retrieved from <Link color="blue.500" href="https://dragontrail.com/wp-content/uploads/sites/6/2025/04/Dragon-Trail-Chinese-Traveler-Sentiment-Report-Spring-2025.pdf" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                US News (2024) A. <Text as="span" fontStyle="italic">US News Best Countries.</Text> [online] Available at: <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                US News (2024) B. <Text as="span" fontStyle="italic">Methodology: How the 2024 Best Countries were Ranked.</Text> [online] Available at: <Link color="blue.500" href="https://www.usnews.com/news/best-countries/articles/methodology" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                US News (2024) C. <Text as="span" fontStyle="italic">These are the Friendliest Countries.</Text> [online]. Available at: <Link color="blue.500" href="https://www.usnews.com/news/best-countries/rankings/friendly" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Visa (2023). <Text as="span" fontStyle="italic">Thailand tourism to be boosted by ‘repeat travellers’’ - Visa study.</Text> [online] Available at: <Link color="blue.500" href="https://www.visa.co.th/en_TH/about-visa/newsroom/press-releases/thailand-tourism-to-be-boosted-by-repeat-travellers-visa-study.html" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Webb, A. J. (2013, August 13). <Text as="span" fontStyle="italic">Who visits Thailand and Why WBRC Bangkok Webb and Chotithamwattana 2.</Text> Academia.edu. <Link color="blue.500" href="https://www.academia.edu/4234649/Who_visits_Thailand_and_Why_WBRC_Bangkok_Webb_and_Chotithamwattana_2" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Wen, Jun & Kozak, Metin & Yang, Shaohua & Liu, Fang. (2020). <Text as="span" fontStyle="italic">COVID-19: potential effects on Chinese citizens’ lifestyle and travel.</Text> Tourism Review. ahead-of-print. 10.1108/TR-03-2020-0110.
            </Text>

            <Text fontSize="sm" color="gray.600">
                Wilson, D. (2025). <Text as="span" fontStyle="italic">Revealed: The World’s Best Cities for Shopping 2025.</Text> [online]. Available at: <Link color="blue.500" href="https://ceoworld.biz/2025/05/12/revealed-the-worlds-best-cities-for-shopping-2025/" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                worlddata.info. (2025). <Text as="span" fontStyle="italic">Comparison of worldwide cost of living.</Text> [online] Available at: <Link color="blue.500" href="https://www.worlddata.info/cost-of-living.php?full" target="_blank" rel="noopener noreferrer">Link</Link>
            </Text>

            <Text fontSize="sm" color="gray.600">
                Zhang, Yahua & Peng, Yiqian. (2014). <Text as="span" fontStyle="italic">Understanding travel motivations of Chinese tourists visiting Cairns, Australia.</Text> Journal of Hospitality and Tourism Management. 21. 44–53. 10.1016/j.jhtm.2014.07.001.
            </Text>

        </VStack>
    )
}
