/**
 * China Arrivals Chart Component
 * 
 * Interactive line chart showing arrivals from China by country over time.
 * Users can select which countries to display.
 */

import { useState, useEffect, useMemo } from 'react'
import { Box, Text, HStack, VStack, Checkbox, Slider } from '@chakra-ui/react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface DataPoint {
  Country: string
  Year: number
  arrivals_from_china: number
}

const COUNTRY_COLORS: Record<string, string> = {
  'Australia': '#e74c3c',
  'Cambodia': '#3498db',
  'Indonesia': '#2ecc71',
  'Japan': '#f39c12',
  'Korea, Republic of': '#9b59b6',
  'Malaysia': '#1abc9c',
  'Maldives': '#e67e22',
  'Philippines': '#34495e',
  'Singapore': '#16a085',
  'Thailand': '#c0392b',
  'United Kingdom': '#8e44ad',
  'United States of America': '#2980b9',
  'Viet Nam': '#27ae60',
}

interface ArrivalsChartProps {
  title: string
  description: string
  useLog?: boolean
  yAxisLabel?: string
}

function ArrivalsChart({ title, description, useLog = false, yAxisLabel }: ArrivalsChartProps) {
  const [data, setData] = useState<DataPoint[]>([])
  const [selectedCountries, setSelectedCountries] = useState<Set<string>>(new Set(Object.keys(COUNTRY_COLORS)))
  const [loading, setLoading] = useState(true)
  const [yearRange, setYearRange] = useState<[number, number]>([1995, 2024])

  // Get min and max years from data
  const { minYear, maxYear } = useMemo(() => {
    if (data.length === 0) return { minYear: 1995, maxYear: 2024 }
    const years = data.map(d => d.Year)
    return {
      minYear: Math.min(...years),
      maxYear: Math.max(...years)
    }
  }, [data])

  useEffect(() => {
    fetch('/Primary_Dataset_For_Panel_FINAL.csv')
      .then(response => response.text())
      .then(csvText => {
        const lines = csvText.split('\n')
        
        const parsed: DataPoint[] = []
        for (let i = 1; i < lines.length; i++) {
          const values = lines[i].split(',')
          if (values.length >= 3 && values[0] && values[1] && values[2]) {
            const country = values[0].trim()
            const year = parseInt(values[1].trim())
            const arrivals = parseFloat(values[2].trim())
            
            if (!isNaN(year) && !isNaN(arrivals)) {
              parsed.push({ Country: country, Year: year, arrivals_from_china: arrivals })
            }
          }
        }
        
        setData(parsed)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error loading data:', error)
        setLoading(false)
      })
  }, [])

  // Update year range when data loads
  useEffect(() => {
    if (data.length > 0) {
      setYearRange([minYear, maxYear])
    }
  }, [minYear, maxYear, data.length])

  const toggleCountry = (country: string) => {
    const newSelected = new Set(selectedCountries)
    if (newSelected.has(country)) {
      newSelected.delete(country)
    } else {
      newSelected.add(country)
    }
    setSelectedCountries(newSelected)
  }

  const selectAll = () => {
    setSelectedCountries(new Set(Object.keys(COUNTRY_COLORS)))
  }

  const deselectAll = () => {
    setSelectedCountries(new Set())
  }

  // Transform data for Recharts
  const chartData = () => {
    const yearMap = new Map<number, any>()
    
    data.forEach(point => {
      // Filter by selected countries and year range
      if (selectedCountries.has(point.Country) && 
          point.Year >= yearRange[0] && 
          point.Year <= yearRange[1]) {
        if (!yearMap.has(point.Year)) {
          yearMap.set(point.Year, { Year: point.Year })
        }
        // Apply log transformation if requested
        const value = useLog && point.arrivals_from_china > 0 
          ? Math.log(point.arrivals_from_china) 
          : point.arrivals_from_china
        yearMap.get(point.Year)![point.Country] = value
      }
    })
    
    return Array.from(yearMap.values()).sort((a, b) => a.Year - b.Year)
  }

  if (loading) {
    return <Text color="#64748b">Loading data...</Text>
  }

  return (
    <VStack align="stretch" gap={6}>
      <Box>
        <Text fontSize="2xl" fontWeight="semibold" mb={4} color="#1e293b">
          {title}
        </Text>
        <Text color="#64748b" mb={4}>
          {description}
        </Text>
      </Box>

      {/* Year Range Selection */}
      <Box borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" p={4} bg="#f8fafc">
        <HStack mb={4} justify="space-between">
          <Text fontWeight="semibold" color="#1e293b">Select Year Range:</Text>
          <HStack gap={4}>
            <Text fontSize="sm" color="#64748b">
              {yearRange[0]} - {yearRange[1]}
            </Text>
            <Text 
              color="#3498db" 
              cursor="pointer" 
              fontSize="sm"
              _hover={{ textDecoration: 'underline' }}
              onClick={() => setYearRange([minYear, maxYear])}
            >
              Reset
            </Text>
          </HStack>
        </HStack>
        
        <Slider.Root
          min={minYear}
          max={maxYear}
          value={yearRange}
          onValueChange={(e) => setYearRange(e.value as [number, number])}
          minStepsBetweenThumbs={1}
        >
          <Slider.Control>
            <Slider.Track>
              <Slider.Range />
            </Slider.Track>
            <Slider.Thumb index={0} />
            <Slider.Thumb index={1} />
          </Slider.Control>
          <Slider.MarkerGroup>
            <Slider.Marker value={minYear}>
              <Text fontSize="xs" color="#64748b">{minYear}</Text>
            </Slider.Marker>
            <Slider.Marker value={maxYear}>
              <Text fontSize="xs" color="#64748b">{maxYear}</Text>
            </Slider.Marker>
          </Slider.MarkerGroup>
        </Slider.Root>
      </Box>

      {/* Country Selection */}
      <Box borderWidth="1px" borderColor="#e2e8f0" borderRadius="md" p={4} bg="#f8fafc">
        <HStack mb={3} gap={4}>
          <Text fontWeight="semibold" color="#1e293b">Select Countries:</Text>
          <Text 
            color="#3498db" 
            cursor="pointer" 
            fontSize="sm"
            _hover={{ textDecoration: 'underline' }}
            onClick={selectAll}
          >
            Select All
          </Text>
          <Text 
            color="#3498db" 
            cursor="pointer" 
            fontSize="sm"
            _hover={{ textDecoration: 'underline' }}
            onClick={deselectAll}
          >
            Deselect All
          </Text>
        </HStack>
        
        <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(200px, 1fr))" gap={2}>
          {Object.keys(COUNTRY_COLORS).map(country => (
            <Checkbox.Root
              key={country}
              checked={selectedCountries.has(country)}
              onCheckedChange={() => toggleCountry(country)}
            >
              <Checkbox.HiddenInput />
              <Checkbox.Control />
              <Checkbox.Label>
                <HStack gap={2}>
                  <Box w="12px" h="12px" bg={COUNTRY_COLORS[country]} borderRadius="sm" />
                  <Text fontSize="sm" color="#1e293b">{country}</Text>
                </HStack>
              </Checkbox.Label>
            </Checkbox.Root>
          ))}
        </Box>
      </Box>

      {/* Chart */}
      <Box h="500px" w="100%">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData()} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="Year" 
              stroke="#64748b"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="#64748b"
              style={{ fontSize: '12px' }}
              label={yAxisLabel ? { value: yAxisLabel, angle: -90, position: 'insideLeft', style: { fontSize: '12px', fill: '#64748b' } } : undefined}
              tickFormatter={(value) => {
                if (useLog) {
                  return value.toFixed(1)
                }
                if (value >= 1000000) return `${(value / 1000000).toFixed(1)}M`
                if (value >= 1000) return `${(value / 1000).toFixed(0)}K`
                return value.toString()
              }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'white', 
                border: '1px solid #e2e8f0',
                borderRadius: '6px',
                fontSize: '12px'
              }}
              formatter={(value: any) => {
                if (useLog) {
                  return `ln(${Math.exp(value).toLocaleString(undefined, { maximumFractionDigits: 0 })}) = ${value.toFixed(2)}`
                }
                return value.toLocaleString()
              }}
            />
            <Legend 
              wrapperStyle={{ fontSize: '12px' }}
            />
            {Array.from(selectedCountries).map(country => (
              <Line
                key={country}
                type="monotone"
                dataKey={country}
                stroke={COUNTRY_COLORS[country]}
                strokeWidth={2}
                dot={false}
                connectNulls
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </Box>
    </VStack>
  )
}


// Main export component with both linear and log charts
export function ChinaArrivalsChart() {
  return (
    <VStack align="stretch" gap={12}>
      {/* Linear Scale Chart */}
      <ArrivalsChart
        title="Tourist Arrivals from China by Destination Country"
        description="This interactive chart shows the number of Chinese tourists arriving at different destination countries over time. Select or deselect countries to customize the view."
      />

      {/* Logarithmic Scale Chart */}
      <Box borderTop="2px" borderColor="#e2e8f0" pt={12}>
        <ArrivalsChart
          title="Tourist Arrivals from China (Logarithmic Scale)"
          description="The same data displayed on a logarithmic scale. This transformation is commonly used in econometric models to interpret coefficients as percentage changes and to handle the wide range of values across countries."
          useLog={true}
          yAxisLabel="ln(Arrivals)"
        />
        
        {/* Justification */}
        <Box mt={6} p={6} bg="#f8fafc" borderRadius="md" borderWidth="1px" borderColor="#e2e8f0">
          <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
            Why Use Logarithmic Transformation?
          </Text>
          <VStack align="stretch" gap={3} color="#64748b" fontSize="sm" lineHeight="1.8">
            <Text>
              <strong style={{ color: '#1e293b' }}>1. Percentage Interpretation:</strong> When we log-transform the dependent variable (arrivals), 
              the regression coefficients can be interpreted as percentage changes rather than absolute changes. For example, 
              a coefficient of 0.05 means a 5% increase in arrivals, which is more meaningful when comparing countries 
              with vastly different tourism volumes.
            </Text>
            <Text>
              <strong style={{ color: '#1e293b' }}>2. Handling Scale Differences:</strong> Our data spans several orders of magnitude—from 
              thousands of arrivals (Maldives in early years) to millions (Thailand, Japan). The logarithmic transformation 
              compresses this range, preventing countries with larger absolute numbers from dominating the regression and 
              allowing us to model proportional relationships.
            </Text>
            <Text>
              <strong style={{ color: '#1e293b' }}>3. Linearity in Parameters:</strong> Many economic relationships are multiplicative 
              rather than additive. Taking logs converts multiplicative relationships into additive ones, which satisfies 
              the linearity assumption required for OLS regression. This is particularly important for modeling growth rates 
              and elasticities.
            </Text>
            <Text>
              <strong style={{ color: '#1e293b' }}>4. Reducing Heteroskedasticity:</strong> Tourism data often exhibits increasing 
              variance as the mean increases (larger countries have more volatile absolute changes). Log transformation 
              stabilizes the variance across observations, improving the efficiency of our estimators and the validity 
              of our standard errors.
            </Text>
            <Text>
              <strong style={{ color: '#1e293b' }}>5. Smoothing Outliers:</strong> The log transformation reduces the influence 
              of extreme values without removing them, making our model more robust to unusual observations while still 
              capturing the underlying trends.
            </Text>
          </VStack>
        </Box>
      </Box>
    </VStack>
  )
}
