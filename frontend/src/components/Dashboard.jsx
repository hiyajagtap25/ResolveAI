import { useState, useEffect } from 'react'
import axios from 'axios'
import StatCard from './StatCard'
import FaultDistribution from './FaultDistribution'
import ProductHealth from './ProductHealth'
import ResolutionMetrics from './ResolutionMetrics'
import TrendChart from './TrendChart'
import AlertsPanel from './AlertsPanel'
import './Dashboard.css'

function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [summaryStats, setSummaryStats] = useState(null)
  const [error, setError] = useState(null)
  const [refreshing, setRefreshing] = useState(false)

  const fetchData = async () => {
    try {
      setRefreshing(true)
      const [dashboardRes, statsRes] = await Promise.all([
        axios.get('/api/analytics/dashboard'),
        axios.get('/api/stats/summary'),
      ])
      
      setData(dashboardRes.data)
      setSummaryStats(statsRes.data)
      setError(null)
    } catch (err) {
      setError('Failed to load dashboard data')
      console.error(err)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="dashboard-loading">Loading dashboard...</div>
  }

  if (error) {
    return <div className="dashboard-error">{error}</div>
  }

  const avgSatisfaction = summaryStats?.average_satisfaction && summaryStats.average_satisfaction.length > 0
    ? (summaryStats.average_satisfaction.reduce((acc, c) => acc + c.customer_satisfaction, 0) / summaryStats.average_satisfaction.length).toFixed(1)
    : 'N/A'

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>📊 Complaint Intelligence Dashboard</h1>
        <button 
          className={`refresh-btn ${refreshing ? 'refreshing' : ''}`}
          onClick={fetchData}
          disabled={refreshing}
        >
          ↻ Refresh
        </button>
      </div>

      {/* Top Stats */}
      <div className="stats-grid">
        <StatCard
          label="Total Complaints"
          value={summaryStats?.total_complaints || 0}
          trend="+12%"
          color="blue"
        />
        <StatCard
          label="Resolution Rate"
          value={`${summaryStats?.resolution_rate || 0}%`}
          trend="+5%"
          color="green"
        />
        <StatCard
          label="Critical Issues"
          value={summaryStats?.critical_complaints || 0}
          trend="-3%"
          color="red"
        />
        <StatCard
          label="Avg Satisfaction"
          value={avgSatisfaction}
          trend="+8%"
          color="blue"
        />
      </div>

      {/* Main Content Grid */}
      <div className="dashboard-grid">
        {/* Left Column */}
        <div className="dashboard-col-left">
          {data && <FaultDistribution data={data.fault_distribution} />}
          {data && <TrendChart />}
        </div>

        {/* Right Column */}
        <div className="dashboard-col-right">
          {data && <ProductHealth data={data.product_health} />}
          {data && <ResolutionMetrics data={data.resolution_metrics} />}
        </div>
      </div>

      {/* Alerts Section */}
      <div className="dashboard-full-width">
        {data && <AlertsPanel data={data.critical_alerts} />}
      </div>
    </div>
  )
}

export default Dashboard
