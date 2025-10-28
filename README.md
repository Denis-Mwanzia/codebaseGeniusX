# 🚀 Codebase Genius X: The Intelligent Crew

**AI-Powered Multi-Agent Documentation System Built in Jac Language**

Codebase Genius X automatically analyzes any GitHub repository, maps its structure, understands code relationships, and generates professional Markdown documentation enhanced with Gemini-powered summaries and Mermaid diagrams.

**Repository:** [https://github.com/Denis-Mwanzia/codebaseGeniusX.git](https://github.com/Denis-Mwanzia/codebaseGeniusX.git)

## 🎯 The Intelligent Crew

Meet the agents that make it all happen:

| Agent | Role | Description |
|-------|------|-------------|
| 🧭 **Captain** | Supervisor | Coordinates workflow, manages tasks, aggregates outputs |
| 🗺️ **Navigator** | Repository Mapper | Clones repo, builds file tree, summarizes README |
| 🔍 **Inspector** | Code Analyzer | Parses code, builds Code Context Graph (CCG) |
| ✍️ **Author** | Documentation Writer | Generates structured Markdown docs with Gemini |
| 🎨 **Designer** | Diagram Generator | Creates Mermaid diagrams from CCG |

## 🏗️ Architecture

```
User Input (GitHub URL)
    ↓
🧭 Captain → 🗺️ Navigator → 🔍 Inspector → ✍️ Author → 🎨 Designer
    ↓
Professional Documentation
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- Git (for cloning repositories)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Denis-Mwanzia/codebaseGeniusX.git
cd codebaseGeniusX
```

2. **Install Python dependencies**
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Install Jaseci (Jac Language runtime)**
```bash
pip install jaseci
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

**Get your Gemini API Key:** [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

5. **Setup frontend**
```bash
cd frontend
npm install
cd ..
```

### Running the System

**Backend:**
```bash
python api.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` and enter a GitHub URL!

## 📁 Project Structure

```
codebaseGeniusX/
├── agents/                 # Jac agent walkers
│   ├── navigator.jac       # Repository mapper
│   ├── inspector.jac       # Code analyzer
│   ├── author.jac          # Documentation writer
│   └── designer.jac        # Diagram generator
├── utils/                  # Python utilities
│   ├── gemini_client.py    # Gemini AI integration
│   ├── parser.py           # Multi-language code parser
│   └── file_utils.py       # Git and file operations
├── frontend/              # React application
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   └── main.jsx       # Entry point
│   └── package.json
├── outputs/               # Generated documentation (auto-created)
├── main.jac              # Main captain walker
├── abilities.py          # Jac-Python bridge
├── jac_orchestrator.py   # Workflow orchestrator
├── api.py                # FastAPI backend
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## 🎨 Features

- ✅ **Pure Jac Language** backend with multi-agent architecture
- ✅ **Gemini AI** integration for intelligent documentation
- ✅ **Multi-language Support**: Python, JavaScript, TypeScript, JSX, TSX
- ✅ **Automatic Language Detection**: Identifies primary programming languages
- ✅ **Framework Detection**: Detects React, Vue, Express, FastAPI, and more
- ✅ **Code Context Graph** analysis with entity extraction
- ✅ **React Component Detection**: Automatically identifies and documents components
- ✅ **Mermaid diagrams** for visual documentation
- ✅ **React frontend** with real-time progress tracking
- ✅ **REST API** for easy integration
- ✅ **Automatic Repository Cleanup**: Keeps only generated documentation files
- ✨ **Creative User Experience**: Engaging, story-driven console output and documentation
- 🎭 **Personality-Driven Agents**: Each agent has unique voice and character
- 🎪 **Visual Documentation**: Enhanced with badges, emojis, and storytelling elements

## 📊 Output Example

The system generates four files in `outputs/[repo-name]/`:

- **`docs.md`** - Creative Markdown documentation with:
  - 🎨 Stylish headers with badges and visual elements
  - 🌟 "Project Spotlight" with storytelling approach
  - 🏗️ "Architecture Landscape" with emoji file tree
  - 🔮 "AI-Powered Insights" with smart recommendations
  - 🎭 "The Story Behind The Code" narrative conclusion
  - 🏆 "Hall of Fame" crediting The Intelligent Crew
  
- **`code_graph.json`** - Structured code analysis:
  - Extracted functions, classes, and React components
  - Module relationships and dependencies
  - Language statistics and framework detection
  
- **`file_tree.json`** - Complete repository structure with metadata

- **`diagram.mmd`** - Mermaid diagram showing module relationships

### 🎪 Creative Console Experience

Watch The Intelligent Crew in action with engaging messages:
- 🧭 **Captain**: "All hands on deck! Initiating code exploration mission..."
- 🗺️ **Navigator**: "Charting course to digital treasure..."
- 🔍 **Inspector**: "CSI: Code Scene Investigation in progress..."
- ✍️ **Author**: "Weaving tales of code and glory..."
- 🎨 **Designer**: "Painting digital masterpieces..."
- 🧹 **Janitor**: "Marie Kondo mode activated! Tidying up..."

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Core Logic** | Jac Language (Jaseci) |
| **Multi-Agent** | Walker-based orchestration |
| **AI Model** | Google Gemini Pro |
| **Parsing** | Python AST + Regex patterns |
| **Visualization** | Mermaid diagrams |
| **Backend** | FastAPI (Python) |
| **Frontend** | React 19 + Vite + Tailwind CSS |
| **Version Control** | GitPython |

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

MIT License

## 🙏 Acknowledgments

- Built with [Jac Language](https://jaclang.org)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Inspired by multi-agent AI patterns

## 🏆 Assignment 2

**Course:** Advanced Software Engineering  
**Student:** Denis Mwanzia  
**Repository:** [https://github.com/Denis-Mwanzia/codebaseGeniusX.git](https://github.com/Denis-Mwanzia/codebaseGeniusX.git)

---

**Made with ❤️ by The Intelligent Crew**

