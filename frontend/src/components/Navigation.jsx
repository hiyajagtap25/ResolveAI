import './Navigation.css'

function Navigation({ activeTab, setActiveTab }) {
  return (
    <nav className="navigation">
      <div className="nav-header">
        <div className="nav-logo">
          <span className="logo-icon">📊</span>
          <h1>Resolve</h1>
        </div>
        <p className="nav-subtitle">Complaint Intelligence Platform</p>
      </div>
      
      <div className="nav-menu">
        <button
          className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          <span className="nav-icon">📈</span>
          <span>Dashboard</span>
        </button>
      </div>

      <div className="nav-footer">
        <p className="nav-version">v1.0.0</p>
      </div>
    </nav>
  )
}

export default Navigation
