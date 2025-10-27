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

  const analyzeRepository = async () => {
    if (!githubUrl.trim()) {
      setError('Please enter a GitHub URL')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)
    setProgress([])

    const agents = [
      { name: 'Navigator', icon: '🗺️', description: 'Cloning and mapping repository' },
      { name: 'Inspector', icon: '🔍', description: 'Analyzing code structure' },
      { name: 'Author', icon: '✍️', description: 'Writing documentation' },
      { name: 'Designer', icon: '🎨', description: 'Creating diagrams' }
    ]

    try {
      // Simulate progress
      for (const agent of agents) {
        setProgress(prev => [...prev, { ...agent, status: 'running' }])
        await new Promise(resolve => setTimeout(resolve, 500))
      }

      const response = await axios.post('/api/analyze', {
        repo_url: githubUrl
      })

      if (response.data.status === 'success') {
        setResult(response.data.result)
        setProgress(prev => prev.map(p => ({ ...p, status: 'complete' })))
        
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
                  <div key={index} className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${
                      agent.status === 'complete' ? 'bg-green-100' : 
                      agent.status === 'error' ? 'bg-red-100' : 'bg-blue-100'
                    }`}>
                      {agent.icon}
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold text-gray-800">{agent.name}</div>
                      <div className="text-sm text-gray-600">{agent.description}</div>
                    </div>
                    <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      agent.status === 'complete' ? 'bg-green-100 text-green-700' : 
                      agent.status === 'error' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                    }`}>
                      {agent.status === 'complete' ? '✓ Complete' : 
                       agent.status === 'error' ? '✗ Error' : '⟳ Running'}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-2xl font-semibold text-gray-800 mb-6">
                Analysis Complete! 🎉
              </h3>
              
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <div className="text-green-800 font-semibold mb-2">
                    Generated Files:
                  </div>
                  <ul className="text-green-700 space-y-1">
                    <li>📄 Documentation (Markdown)</li>
                    <li>📊 Architecture Diagram (Mermaid)</li>
                    <li>🗂️ Code Structure Graph (JSON)</li>
                    <li>📁 File Tree (JSON)</li>
                  </ul>
                </div>

                {/* Documentation Preview */}
                {documentation && (
                  <div className="mt-6 p-6 bg-gray-50 rounded-xl border border-gray-200">
                    <h4 className="text-lg font-semibold text-gray-800 mb-4">
                      📄 Documentation Preview
                    </h4>
                    <div className="max-h-96 overflow-y-auto prose prose-sm max-w-none">
                      <pre className="whitespace-pre-wrap text-gray-700 font-mono text-sm">
                        {documentation.substring(0, 1000)}{documentation.length > 1000 ? '...' : ''}
                      </pre>
                    </div>
                  </div>
                )}

                <div className="mt-6 flex gap-4">
                  <button 
                    onClick={downloadDocumentation}
                    disabled={!documentation}
                    className="px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-opacity-90 transition-all disabled:bg-gray-300 disabled:cursor-not-allowed"
                  >
                    📥 Download Documentation
                  </button>
                  <button 
                    onClick={() => setShowFullDoc(true)}
                    className="px-6 py-3 bg-secondary text-white rounded-xl font-semibold hover:bg-opacity-90 transition-all"
                  >
                    👁️ View Full Documentation
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
                  📄 Full Documentation
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

