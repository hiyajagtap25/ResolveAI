import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts'
import './FaultDistribution.css'

const COLORS = ['#2563eb', '#16a34a', '#ea580c', '#dc2626', '#8b5cf6', '#06b6d4', '#f59e0b', '#ec4899']

function FaultDistribution({ data }) {
  if (!data || !data.distribution || data.distribution.length === 0) {
    return <div className="card">No fault data available</div>
  }

  return (
    <div className="card fault-distribution">
      <h2>🔧 Fault Type Distribution</h2>
      <p className="card-subtitle">Total Faults: {data.total_faults}</p>
      
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data.distribution}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ fault_type, percentage }) => `${fault_type}: ${percentage}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="count"
          >
            {data.distribution.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value) => `${value} faults`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>

      <div className="fault-list">
        {data.distribution.map((fault, idx) => (
          <div key={idx} className="fault-item">
            <div className="fault-color" style={{ backgroundColor: COLORS[idx % COLORS.length] }}></div>
            <div className="fault-info">
              <span className="fault-name">{fault.fault_type}</span>
              <span className="fault-count">{fault.count} ({fault.percentage}%)</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default FaultDistribution
