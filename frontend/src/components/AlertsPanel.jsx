import './AlertsPanel.css'

function AlertsPanel({ data }) {
  if (!data) {
    return <div className="card">No alerts data available</div>
  }

  const hasAlerts = (data.critical_products && data.critical_products.length > 0) ||
                    (data.unresolved_fault_types && data.unresolved_fault_types.length > 0)

  if (!hasAlerts) {
    return (
      <div className="card alerts-panel">
        <h2>🚨 Critical Alerts</h2>
        <div className="alerts-empty">
          <p>✓ No critical alerts at this time</p>
        </div>
      </div>
    )
  }

  return (
    <div className="card alerts-panel">
      <h2>🚨 Critical Alerts</h2>
      
      <div className="alerts-grid">
        {data.critical_products && data.critical_products.length > 0 && (
          <div className="alert-section">
            <h3>⚠️ Critical Product Issues</h3>
            <div className="alert-items">
              {data.critical_products.map((item, idx) => (
                <div key={idx} className="alert-item alert-item-critical">
                  <div className="alert-icon">📱</div>
                  <div className="alert-content">
                    <span className="alert-title">{item.product}</span>
                    <span className="alert-details">{item.critical_count} critical complaints</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
        
        {data.unresolved_fault_types && data.unresolved_fault_types.length > 0 && (
          <div className="alert-section">
            <h3>⏳ High Unresolved Issues</h3>
            <div className="alert-items">
              {data.unresolved_fault_types.map((item, idx) => (
                <div key={idx} className="alert-item alert-item-warning">
                  <div className="alert-icon">🔧</div>
                  <div className="alert-content">
                    <span className="alert-title">{item.fault_type}</span>
                    <span className="alert-details">{item.unresolved_count} unresolved</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default AlertsPanel
