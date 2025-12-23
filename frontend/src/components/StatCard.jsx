import './StatCard.css'

function StatCard({ label, value, trend, color }) {
  const colorClass = color || 'blue'
  
  return (
    <div className={`stat-card stat-card-${colorClass}`}>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-trend">{trend}</div>
    </div>
  )
}

export default StatCard
