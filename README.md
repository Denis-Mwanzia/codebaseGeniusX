# 🚀 Codebase Genius X: The Intelligent Crew

**AI-Powered Multi-Agent Documentation System Built in Jac Language**

Codebase Genius X automatically analyzes any GitHub repository, maps its structure, understands code relationships, and generates professional Markdown documentation enhanced with Gemini-powered summaries and Mermaid diagrams.

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
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd codebase-genius-x
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
cp env.example .env
# Edit .env and add your GEMINI_API_KEY
```

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
codebase-genius-x/
├── agents/                 # Jac agent files
│   ├── navigator.jac
│   ├── inspector.jac
│   ├── author.jac
│   └── designer.jac
├── utils/                  # Python utilities
│   ├── gemini_client.py
│   ├── parser.py
│   └── file_utils.py
├── frontend/              # React app
├── outputs/               # Generated docs
├── main.jac              # Main orchestrator
├── api.py                # FastAPI backend
└── requirements.txt
```

## 🎨 Features

- ✅ **Pure Jac Language** backend with multi-agent architecture
- ✅ **Gemini AI** integration for intelligent documentation
- ✅ **Code Context Graph** analysis
- ✅ **Mermaid diagrams** for visual documentation
- ✅ **React frontend** with progress tracking
- ✅ **REST API** for easy integration

## 📊 Output Example

The system generates:
- `docs.md` - Comprehensive documentation
- `code_graph.json` - Code structure analysis
- `file_tree.json` - Repository tree
- `diagram.mmd` - Mermaid architecture diagram

## 🧠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Core Logic | Jac Language (Jaseci) |
| AI Model | Gemini 1.5 Flash |
| Parsing | AST + Tree-sitter |
| Visualization | Mermaid |
| Backend | FastAPI |
| Frontend | React + Vite + Tailwind |

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

---

**Made with ❤️ by The Intelligent Crew**

