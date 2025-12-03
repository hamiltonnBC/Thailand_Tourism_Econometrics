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

export function ChinaArrivalsChart() {
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
        yearMap.get(point.Year)![point.Country] = point.arrivals_from_china
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
          Tourist Arrivals from China by Destination Country
        </Text>
        <Text color="#64748b" mb={4}>
          This interactive chart shows the number of Chinese tourists arriving at different destination countries over time.
          Select or deselect countries to customize the view.
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
              tickFormatter={(value) => {
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
              formatter={(value: any) => value.toLocaleString()}
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
