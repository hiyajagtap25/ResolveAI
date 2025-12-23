import './ResolutionMetrics.css'

function ResolutionMetrics({ data }) {
  if (!data) {
    return <div className="card">No resolution data available</div>
  }

  return (
    <div className="card resolution-metrics">
      <h2>⏱️ Resolution Metrics</h2>
      <p className="card-subtitle">Complaint resolution performance</p>
      
      <div className="metrics-grid">
        <div className="metric-box">
          <span className="metric-label">Total Resolved</span>
          <span className="metric-value">{data.total_resolved}</span>
        </div>
        
        <div className="metric-box">
          <span className="metric-label">Average Time</span>
          <span className="metric-value">{data.avg_resolution_days} days</span>
        </div>
        
        <div className="metric-box">
          <span className="metric-label">Median Time</span>
          <span className="metric-value">{data.median_resolution_days} days</span>
        </div>
        
        <div className="metric-box">
          <span className="metric-label">Fastest</span>
          <span className="metric-value">{data.min_resolution_days} days</span>
        </div>
        
        <div className="metric-box">
          <span className="metric-label">Slowest</span>
          <span className="metric-value">{data.max_resolution_days} days</span>
        </div>
      </div>
    </div>
  )
}

export default ResolutionMetrics
