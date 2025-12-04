/**
 * Recovery Rate Chart Component
 * 
 * Shows the recovery rate of tourist arrivals from China relative to 2019 baseline.
 * Helps identify asymmetric recovery patterns across countries.
 */

import { useState, useEffect, useMemo } from 'react'
import { Box, Text, HStack, VStack, Checkbox } from '@chakra-ui/react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts'

interface DataPoint {
  Country: string
  Year: number
  arrivals_from_china: number
}

interface RecoveryPoint {
  Year: number
  [country: string]: number
}

const RECOVERY_COUNTRIES = [
  'Australia', 'Cambodia', 'Indonesia', 'Japan',
  'Malaysia', 'Maldives', 'Singapore', 'Thailand', 'Viet Nam'
]

const COUNTRY_COLORS: Record<string, string> = {
  'Australia': '#e74c3c',
  'Cambodia': '#3498db',
  'Indonesia': '#2ecc71',
  'Japan': '#f39c12',
  'Malaysia': '#1abc9c',
  'Maldives': '#e67e22',
  'Singapore': '#16a085',
  'Thailand': '#c0392b',
  'Viet Nam': '#27ae60',
}

export function RecoveryRateChart() {
  const [data, setData] = useState<DataPoint[]>([])
  const [selectedCountries, setSelectedCountries] = useState<Set<string>>(new Set(RECOVERY_COUNTRIES))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch(`${import.meta.env.BASE_URL}Primary_Dataset_For_Panel_FINAL.csv`)
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
            
            // Only include recovery countries and years from 2019 onwards
            if (RECOVERY_COUNTRIES.includes(country) && !isNaN(year) && !isNaN(arrivals) && year >= 2019) {
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

  // Calculate recovery rates relative to 2019 baseline
  const recoveryData = useMemo(() => {
    // Get 2019 baseline for each country
    const baseline2019 = new Map<string, number>()
    data.forEach(point => {
      if (point.Year === 2019) {
        baseline2019.set(point.Country, point.arrivals_from_china)
      }
    })

    // Calculate recovery rate for each year
    const yearMap = new Map<number, RecoveryPoint>()
    
    data.forEach(point => {
      const baseline = baseline2019.get(point.Country)
      if (baseline && baseline > 0) {
        if (!yearMap.has(point.Year)) {
          yearMap.set(point.Year, { Year: point.Year })
        }
        // Recovery rate as percentage of 2019 levels
        const recoveryRate = (point.arrivals_from_china / baseline) * 100
        yearMap.get(point.Year)![point.Country] = recoveryRate
      }
    })

    return Array.from(yearMap.values()).sort((a, b) => a.Year - b.Year)
  }, [data])

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
    setSelectedCountries(new Set(RECOVERY_COUNTRIES))
  }

  const deselectAll = () => {
    setSelectedCountries(new Set())
  }

  if (loading) {
    return <Text color="#64748b">Loading data...</Text>
  }

  return (
    <VStack align="stretch" gap={6}>
      <Box>
        <Text fontSize="2xl" fontWeight="semibold" mb={4} color="#1e293b">
          Post-Pandemic Recovery Rate (2019 Baseline = 100%)
        </Text>
        <Text color="#64748b" mb={4}>
          This chart shows how quickly each country is recovering Chinese tourist arrivals relative to their 2019 pre-pandemic levels. 
          Values above 100% indicate the country has exceeded 2019 levels, while values below show incomplete recovery.
        </Text>
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
        
        <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(180px, 1fr))" gap={2}>
          {RECOVERY_COUNTRIES.map(country => (
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
          <LineChart data={recoveryData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
            <XAxis 
              dataKey="Year" 
              stroke="#64748b"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="#64748b"
              style={{ fontSize: '12px' }}
              label={{ value: '% of 2019 Levels', angle: -90, position: 'insideLeft', style: { fontSize: '12px', fill: '#64748b' } }}
              tickFormatter={(value) => `${value}%`}
            />
            {/* Reference line at 100% (2019 baseline) */}
            <ReferenceLine 
              y={100} 
              stroke="#64748b" 
              strokeDasharray="5 5"
              label={{ value: '2019 Baseline', position: 'right', fill: '#64748b', fontSize: 11 }}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'white', 
                border: '1px solid #e2e8f0',
                borderRadius: '6px',
                fontSize: '12px'
              }}
              formatter={(value: any) => `${value.toFixed(1)}%`}
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
                dot={{ r: 4 }}
                connectNulls
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </Box>

      {/* Analysis Box */}
      <Box p={6} bg="#f8fafc" borderRadius="md" borderWidth="1px" borderColor="#e2e8f0">
        <Text fontSize="lg" fontWeight="semibold" mb={3} color="#1e293b">
          Key Insights on Asymmetric Recovery
        </Text>
        <VStack align="stretch" gap={3} color="#64748b" fontSize="sm" lineHeight="1.8">
          <Text>
            <strong style={{ color: '#1e293b' }}>Recovery Patterns:</strong> This visualization reveals significant 
            asymmetry in how different countries are recovering from the COVID-19 pandemic's impact on Chinese tourism. 
            Countries that have exceeded 100% have not only recovered but are attracting more Chinese tourists than 
            in 2019, while those below 100% are still rebuilding.
          </Text>
          <Text>
            <strong style={{ color: '#1e293b' }}>Policy Implications:</strong> The divergence in recovery rates may 
            reflect differences in border reopening policies, visa requirements, marketing efforts, and perceived 
            safety. Countries with faster recovery may have implemented more aggressive tourism promotion strategies 
            or benefited from pent-up demand.
          </Text>
          <Text>
            <strong style={{ color: '#1e293b' }}>Competitive Dynamics:</strong> The asymmetric recovery suggests a 
            potential reshuffling of market share among destination countries. Some destinations may be permanently 
            gaining or losing their position in the Chinese outbound tourism market, which has important implications 
            for long-term tourism planning and investment.
          </Text>
        </VStack>
      </Box>
    </VStack>
  )
}
