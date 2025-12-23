import './ProductHealth.css'

function ProductHealth({ data }) {
  if (!data || !data.scores || data.scores.length === 0) {
    return <div className="card">No product data available</div>
  }

  const getHealthColor = (score) => {
    if (score >= 80) return '#16a34a'
    if (score >= 60) return '#f59e0b'
    if (score >= 40) return '#ea580c'
    return '#dc2626'
  }

  const getHealthLabel = (score) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    if (score >= 40) return 'Fair'
    return 'Poor'
  }

  return (
    <div className="card product-health">
      <h2>📱 Product Health Scores</h2>
      <p className="card-subtitle">Overall product reliability metrics</p>
      
      <div className="health-list">
        {data.scores.map((product, idx) => (
          <div key={idx} className="health-item">
            <div className="health-header">
              <div className="health-name">
                <span className="health-category">{product.category}</span>
                <span className="health-product">{product.product_name}</span>
              </div>
              <span className="health-complaints">{product.complaint_count}</span>
            </div>
            
            <div className="health-bar-container">
              <div className="health-bar">
                <div
                  className="health-bar-fill"
                  style={{
                    width: `${product.health_score}%`,
                    backgroundColor: getHealthColor(product.health_score)
                  }}
                ></div>
              </div>
              <span className="health-score" style={{ color: getHealthColor(product.health_score) }}>
                {product.health_score}
              </span>
            </div>
            <span className="health-label">{getHealthLabel(product.health_score)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ProductHealth
