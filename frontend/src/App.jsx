import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [githubUrl, setGithubUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState([])
  const [documentation, setDocumentation] = useState('')
  const [showFullDoc, setShowFullDoc] = useState(false)
  const [currentRepoName, setCurrentRepoName] = useState('')
  const [agentStates, setAgentStates] = useState({
    navigator: 'pending',
    inspector: 'pending', 
    author: 'pending',
    designer: 'pending'
  })

  const downloadDocumentation = () => {
    if (!documentation) return
    
    const blob = new Blob([documentation], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${result?.repo_name || 'documentation'}.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const updateAgentState = (agentName, state) => {
    setAgentStates(prev => ({
      ...prev,
      [agentName.toLowerCase()]: state
    }))
  }

  const analyzeRepository = async () => {
    if (!githubUrl.trim()) {
      setError('Please enter a GitHub URL')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setProgress([])
    
    // Reset all agents to pending
    setAgentStates({
      navigator: 'pending',
      inspector: 'pending', 
      author: 'pending',
      designer: 'pending'
    })
    
    // Extract repo name from URL for preview (keep full format as used by backend)
    const urlParts = githubUrl.split('/')
    const repoName = urlParts[urlParts.length - 2] + '_' + urlParts[urlParts.length - 1]
    setCurrentRepoName(repoName)

    const agents = [
      { name: 'Navigator', icon: '🗺️', description: 'Cloning and mapping repository', key: 'navigator' },
      { name: 'Inspector', icon: '🔍', description: 'Analyzing code structure', key: 'inspector' },
      { name: 'Author', icon: '✍️', description: 'Writing documentation', key: 'author' },
      { name: 'Designer', icon: '🎨', description: 'Creating diagrams', key: 'designer' }
    ]

    // Initialize progress with all agents in pending state
    setProgress(agents.map(agent => ({ ...agent, status: 'pending' })))

    try {
      // Simulate realistic agent progression: Pending → Initiated → Running → Complete
      for (let i = 0; i < agents.length; i++) {
        const agent = agents[i]
        
        // Set current agent to initiated
        updateAgentState(agent.key, 'initiated')
        setProgress(prev => prev.map((p, idx) => 
          idx === i ? { ...p, status: 'initiated' } : p
        ))
        await new Promise(resolve => setTimeout(resolve, 400))
        
        // Set current agent to running
        updateAgentState(agent.key, 'running')
        setProgress(prev => prev.map((p, idx) => 
          idx === i ? { ...p, status: 'running' } : p
        ))
        
        // Simulate work time (different durations for realism)
        const workDuration = [1200, 1500, 1800, 1000][i] // Navigator, Inspector, Author, Designer
        await new Promise(resolve => setTimeout(resolve, workDuration))
        
        // Set current agent to complete
        updateAgentState(agent.key, 'complete')
        setProgress(prev => prev.map((p, idx) => 
          idx === i ? { ...p, status: 'complete' } : p
        ))
        await new Promise(resolve => setTimeout(resolve, 200))
      }

      // Now make the actual API call
      const response = await axios.post('/api/analyze', {
        repo_url: githubUrl
      })

      if (response.data.status === 'success') {
        setResult(response.data.result)
        
        // Fetch the documentation content
        if (response.data.result?.output_path) {
          try {
            const docResponse = await axios.get(`/api/documentation/${response.data.result.repo_name}`)
            setDocumentation(docResponse.data.content)
          } catch (err) {
            console.error('Error fetching documentation:', err)
          }
        }
      } else {
        throw new Error(response.data.message || 'Analysis failed')
      }
    } catch (err) {
      setError(err.message || 'An error occurred')
      // Set all agents to error state
      Object.keys(agentStates).forEach(key => updateAgentState(key, 'error'))
      setProgress(prev => prev.map(p => ({ ...p, status: 'error' })))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🚀 Codebase Genius X
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            The Intelligent Crew
          </p>
          <p className="text-sm text-gray-500">
            AI-powered documentation system for GitHub repositories
          </p>
        </div>

        {/* Input Section */}
        <div className="max-w-3xl mx-auto mb-8">
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">
              Enter GitHub Repository URL
            </h2>
            
            <div className="flex gap-4">
              <input
                type="text"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                placeholder="https://github.com/user/repo"
                className="flex-1 px-6 py-4 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 text-gray-800"
                disabled={loading}
              />
              <button
                onClick={analyzeRepository}
                disabled={loading}
                className="px-8 py-4 bg-primary text-white rounded-xl font-semibold hover:bg-opacity-90 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all"
              >
                {loading ? 'Analyzing...' : 'Analyze'}
              </button>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Progress Section */}
        {progress.length > 0 && (
          <div className="max-w-3xl mx-auto mb-8">
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-800 mb-6">
                Agent Progress
              </h3>
              <div className="space-y-4">
                {progress.map((agent, index) => (
                  <div 
                    key={index} 
                    className="flex items-center gap-4 transform transition-all duration-500 ease-in-out hover:scale-105 animate-fade-in"
                    style={{ animationDelay: `${index * 200}ms` }}
                  >
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl transition-all duration-300 ${
                      agent.status === 'complete' ? 'bg-green-100 animate-bounce-once' : 
                      agent.status === 'error' ? 'bg-red-100 animate-shake' : 
                      agent.status === 'running' ? 'bg-blue-100 animate-pulse' :
                      agent.status === 'initiated' ? 'bg-yellow-100 animate-bounce-once' :
                      'bg-gray-100'
                    }`}>
                      <span className={`${
                        agent.status === 'complete' ? 'animate-scale-in' : 
                        agent.status === 'error' ? 'animate-shake' : 
                        agent.status === 'running' ? 'animate-spin-slow' :
                        agent.status === 'initiated' ? 'animate-pulse' :
                        ''
                      }`}>
                        {agent.icon}
                      </span>
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold text-gray-800">{agent.name}</div>
                      <div className="text-sm text-gray-600">{agent.description}</div>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-semibold transition-all duration-300 ${
                      agent.status === 'complete' ? 'bg-green-100 text-green-700 animate-pulse-once' : 
                      agent.status === 'error' ? 'bg-red-100 text-red-700 animate-shake' : 
                      agent.status === 'running' ? 'bg-blue-100 text-blue-700 animate-pulse' :
                      agent.status === 'initiated' ? 'bg-yellow-100 text-yellow-700 animate-bounce-once' :
                      'bg-gray-100 text-gray-600'
                    }`}>
                      <span className="flex items-center gap-2">
                        {agent.status === 'complete' ? (
                          <>
                            <span className="animate-bounce">✓</span>
                            <span>Complete</span>
                          </>
                        ) : agent.status === 'error' ? (
                          <>
                            <span className="animate-pulse">✗</span>
                            <span>Error</span>
                          </>
                        ) : agent.status === 'running' ? (
                          <>
                            <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            <span>Running</span>
                          </>
                        ) : agent.status === 'initiated' ? (
                          <>
                            <span className="animate-pulse">🚀</span>
                            <span>Initiated</span>
                          </>
                        ) : (
                          <>
                            <span>⏳</span>
                            <span>Pending</span>
                          </>
                        )}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="max-w-4xl mx-auto animate-fade-in">
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-2xl font-semibold text-gray-800 mb-6 animate-bounce-once">
                <span className="animate-scale-in">Analysis Complete! 🎉</span>
              </h3>
              
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg animate-fade-in" style={{ animationDelay: '0.2s' }}>
                  <div className="text-green-800 font-semibold mb-2">
                    Generated Files:
                  </div>
                  <ul className="text-green-700 space-y-1">
                    <li className="animate-fade-in" style={{ animationDelay: '0.4s' }}>📄 Documentation (Markdown)</li>
                    <li className="animate-fade-in" style={{ animationDelay: '0.6s' }}>📊 Architecture Diagram (Mermaid)</li>
                    <li className="animate-fade-in" style={{ animationDelay: '0.8s' }}>🗂️ Code Structure Graph (JSON)</li>
                    <li className="animate-fade-in" style={{ animationDelay: '1.0s' }}>📁 File Tree (JSON)</li>
                  </ul>
                </div>

                {/* Web Preview */}
                {documentation && (
                  <div className="mt-6 p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border border-purple-200 animate-fade-in" style={{ animationDelay: '1.2s' }}>
                    <h4 className="text-lg font-semibold text-gray-800 mb-4 animate-scale-in" style={{ animationDelay: '1.4s' }}>
                      🌐 Web Preview
                    </h4>
                    <div className="text-center">
                      <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-full text-sm font-semibold inline-block mb-4 animate-pulse-once" style={{ animationDelay: '1.6s' }}>
                        🚀 Live Preview Available
                      </div>
                      <p className="text-gray-700 mb-6">
                        Your documentation has been generated and is ready to view in a beautiful, 
                        interactive web format with professional styling and enhanced readability.
                      </p>
                      <button 
                        onClick={() => window.open(`http://localhost:8000/preview/${currentRepoName}`, '_blank')}
                        className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl font-bold text-lg hover:from-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 shadow-lg animate-bounce-once"
                        style={{ animationDelay: '1.8s' }}
                      >
                        🌐 Open Web Preview
                      </button>
                    </div>
                  </div>
                )}

                <div className="mt-6 flex gap-4">
                  <button 
                    onClick={downloadDocumentation}
                    disabled={!documentation}
                    className="px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-opacity-90 transition-all disabled:bg-gray-300 disabled:cursor-not-allowed animate-fade-in transform hover:scale-105"
                    style={{ animationDelay: '2.0s' }}
                  >
                    📥 Download Documentation
                  </button>
                  <button 
                    onClick={() => setShowFullDoc(true)}
                    className="px-6 py-3 bg-secondary text-white rounded-xl font-semibold hover:bg-opacity-90 transition-all animate-fade-in transform hover:scale-105"
                    style={{ animationDelay: '2.2s' }}
                  >
                    👁️ View Raw Documentation
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Full Documentation Modal */}
        {showFullDoc && documentation && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col">
              <div className="p-6 border-b border-gray-200 flex justify-between items-center">
            <h3 className="text-2xl font-semibold text-gray-800">
              📄 Raw Documentation
            </h3>
                <button
                  onClick={() => setShowFullDoc(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl font-bold"
                >
                  ×
                </button>
              </div>
              <div className="flex-1 overflow-y-auto p-6">
                <div className="prose prose-sm max-w-none">
                  <pre className="whitespace-pre-wrap text-gray-700 font-mono text-sm">
                    {documentation}
                  </pre>
                </div>
              </div>
              <div className="p-6 border-t border-gray-200 flex justify-end gap-4">
                <button
                  onClick={() => downloadDocumentation()}
                  className="px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-opacity-90 transition-all"
                >
                  📥 Download
                </button>
                <button
                  onClick={() => setShowFullDoc(false)}
                  className="px-6 py-3 bg-gray-200 text-gray-800 rounded-xl font-semibold hover:bg-gray-300 transition-all"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

