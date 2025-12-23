import { useState, useEffect } from 'react'
import axios from 'axios'
import Dashboard from './components/Dashboard'
import Navigation from './components/Navigation'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('dashboard')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Check backend health
    axios
      .get('/api/health')
      .then(() => setLoading(false))
      .catch((err) => {
        setError('Backend connection failed')
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="app-loading">
        <div className="spinner"></div>
        <p>Loading Resolve...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="app-error">
        <h1>⚠️ Connection Error</h1>
        <p>{error}</p>
        <p>Make sure the FastAPI backend is running on http://localhost:8000</p>
      </div>
    )
  }

  return (
    <div className="app">
      <Navigation activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="app-main">
        {activeTab === 'dashboard' && <Dashboard />}
      </main>
    </div>
  )
}

export default App
