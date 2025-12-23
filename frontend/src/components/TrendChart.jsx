import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import axios from 'axios'
import './TrendChart.css'

function TrendChart() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    axios
      .get('/api/analytics/trends?days=30')
      .then((res) => {
        const trendData = res.data.data.map(item => ({
          date: new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          complaints: item.complaints
        }))
        setData(trendData)
        setLoading(false)
      })
      .catch((err) => {
        console.error(err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="card">Loading trend data...</div>
  }

  return (
    <div className="card trend-chart">
      <h2>📈 Complaint Trend (30 Days)</h2>
      <p className="card-subtitle">Daily complaint volume over the past month</p>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis dataKey="date" stroke="#6b7280" />
          <YAxis stroke="#6b7280" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: 'none',
              borderRadius: '4px',
              color: '#fff'
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="complaints"
            stroke="#2563eb"
            strokeWidth={2}
            dot={{ fill: '#2563eb', r: 4 }}
            activeDot={{ r: 6 }}
            name="Complaints"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default TrendChart
