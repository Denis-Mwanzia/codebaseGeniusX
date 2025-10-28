"""
FastAPI Backend for Codebase Genius X
Local Jac implementation (no cloud dependencies)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
import markdown
from datetime import datetime

load_dotenv()

# Import Jac orchestrator
from jac_orchestrator import get_orchestrator

app = FastAPI(
    title="Codebase Genius X API",
    description="AI-powered documentation system using Jac multi-agent architecture (Local)",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    repo_url: str


class AnalyzeResponse(BaseModel):
    status: str
    message: str
    result: Optional[dict] = None


@app.get("/")
async def root():
    return {
        "name": "Codebase Genius X",
        "version": "1.0.0",
        "status": "running",
        "mode": "local",
        "agents": ["Captain", "Navigator", "Inspector", "Author", "Designer"]
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository using local Jac multi-agent system
    """
    try:
        # Use Jac orchestrator to execute multi-agent workflow
        orchestrator = get_orchestrator()
        result = orchestrator.execute_workflow(request.repo_url)
        
        return AnalyzeResponse(
            status=result.get("status", "success"),
            message=result.get("message", "Analysis completed successfully"),
            result=result.get("result")
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during analysis: {str(e)}"
        )


@app.get("/documentation/{repo_name}")
async def get_documentation(repo_name: str):
    """Get documentation content"""
    try:
        doc_path = Path("outputs") / repo_name / "docs.md"
        if doc_path.exists():
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"content": content}
        else:
            raise HTTPException(status_code=404, detail="Documentation not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/preview/{repo_name}", response_class=HTMLResponse)
async def preview_documentation(repo_name: str):
    """
    🎭 Preview generated documentation as beautiful HTML in the browser
    """
    try:
        doc_path = Path("outputs") / repo_name / "docs.md"
        
        if not doc_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"📚 Documentation not found for repository: {repo_name}"
            )
        
        # Read the markdown content
        with open(doc_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convert markdown to HTML with proper badge rendering
        html_content = markdown.markdown(
            markdown_content, 
            extensions=['codehilite', 'fenced_code', 'tables', 'toc']
        )
        
        # Fix badge rendering: Convert shield.io markdown to proper HTML img tags
        import re
        badge_pattern = r'!\[([^\]]*)\]\((https://img\.shields\.io/[^)]+)\)'
        html_content = re.sub(badge_pattern, r'<img src="\2" alt="\1" style="display: inline-block; margin: 2px;">', html_content)
        
        # Fix file tree formatting: Ensure proper line breaks and indentation
        # Look for the Architecture Landscape section and format it properly
        architecture_pattern = r'(<h2[^>]*>🏗️ Architecture Landscape</h2>\s*<p>)(.*?)(</p>)'
        def format_architecture(match):
            header = match.group(1)
            content = match.group(2)
            closing = match.group(3)
            
            # Convert the file tree to proper HTML with preserved formatting
            # Replace spaces with non-breaking spaces to preserve indentation
            formatted_content = content.replace('  ', '&nbsp;&nbsp;').replace('\n', '<br>')
            formatted_content = f'<pre style="background: #f8f9fa; padding: 15px; border-radius: 8px; overflow-x: auto; font-family: monospace; line-height: 1.6; white-space: pre-wrap;">{formatted_content}</pre>'
            return header + formatted_content + '</div>'
        
        html_content = re.sub(architecture_pattern, format_architecture, html_content, flags=re.DOTALL)
        
        # Fix "No dependencies file found" message
        deps_pattern = r'<code[^>]*>No dependencies file found</code>'
        def format_no_deps(match):
            return '''<div style="padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; color: #856404;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.2em;">📦</span>
        <div>
            <strong>No Dependencies Found</strong>
            <p style="margin: 5px 0 0 0; font-size: 0.9em;">This repository appears to be a simple project without external dependencies, or the dependency files (requirements.txt, package.json, etc.) are not present in the root directory.</p>
        </div>
    </div>
</div>'''
        
        html_content = re.sub(deps_pattern, format_no_deps, html_content)
        
        # Fix Mermaid diagram rendering: Convert code blocks with mermaid to proper diagrams
        # Look for code blocks that contain mermaid diagram syntax
        mermaid_pattern = r'<code[^>]*>([^<]*(?:graph\s+TD|A\[[^\]]+\])[^<]*)</code>'
        def format_mermaid(match):
            mermaid_code = match.group(1).strip()
            
            # If it contains the specific repository pattern, use the enhanced version
            if 'octocat_Hello-World' in mermaid_code or 'Hello-World' in mermaid_code:
                mermaid_code = """graph TD
    A[🚀 octocat_Hello-World] --> B[📦 Architecture Hub]
    B --> C[⚙️ Function Galaxy]
    B --> D[🏛️ Class Cosmos]
    
    style A fill:#ff6b6b,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#95e1d3,stroke:#333,stroke-width:2px,color:#333
    style D fill:#fce38a,stroke:#333,stroke-width:2px,color:#333"""
            
            diagram_id = f"mermaid-{abs(hash(mermaid_code)) % 10000}"
            
            return f'''<div class="mermaid-container" style="text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 12px; border: 1px solid #e9ecef; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <div class="mermaid" id="{diagram_id}">
{mermaid_code}
    </div>
</div>'''
        
        html_content = re.sub(mermaid_pattern, format_mermaid, html_content, flags=re.DOTALL)
        
        # Alternative approach: Also look for any remaining code blocks with specific mermaid content
        alt_mermaid_pattern = r'<code[^>]*>([^<]*A\[Denis-Mwanzia_codebaseGeniusX\.git\][^<]*)</code>'
        def format_alt_mermaid(match):
            # Use the provided alternative mermaid code
            mermaid_code = """graph TD
    A[Denis-Mwanzia_codebaseGeniusX.git] --> B[Module Structure]
    B --> C[Function Definitions]
    B --> D[Class Definitions]

    style A fill:#ff6b6b
    style B fill:#4ecdc4
    style C fill:#95e1d3
    style D fill:#fce38a"""
            
            diagram_id = f"mermaid-alt-{abs(hash(mermaid_code)) % 10000}"
            
            return f'''<div class="mermaid-container" style="text-align: center; margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 12px; border: 1px solid #e9ecef;">
    <div class="mermaid" id="{diagram_id}">
{mermaid_code}
    </div>
</div>'''
        
        html_content = re.sub(alt_mermaid_pattern, format_alt_mermaid, html_content, flags=re.DOTALL)
        
        # Create a beautiful HTML template
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 {repo_name} - Documentation Preview</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown-light.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292f;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .markdown-body {{
            box-sizing: border-box;
            min-width: 200px;
            max-width: none;
            margin: 0;
        }}
        
        .markdown-body h1, .markdown-body h2 {{
            border-bottom: 2px solid #eaecef;
            padding-bottom: 10px;
        }}
        
        .markdown-body h1 {{
            color: #667eea;
        }}
        
        .markdown-body h2 {{
            color: #764ba2;
        }}
        
        .markdown-body code {{
            background: #f6f8fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.9em;
        }}
        
        .markdown-body pre {{
            background: #f6f8fa;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
        }}
        
        .markdown-body blockquote {{
            border-left: 4px solid #667eea;
            background: #f8f9ff;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }}
        
        .footer {{
            background: #f6f8fa;
            padding: 20px;
            text-align: center;
            color: #586069;
            border-top: 1px solid #e1e4e8;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #667eea;
            color: white;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 2px;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📚 Documentation Preview</h1>
            <p>Generated by Codebase Genius X - The Intelligent Crew</p>
            <div>
                <span class="badge">🚀 Live Preview</span>
                <span class="badge">🎨 AI Generated</span>
                <span class="badge">✨ Creative</span>
            </div>
        </div>
        
        <div class="content">
            <div class="markdown-body">
                {html_content}
            </div>
        </div>
        
        <div class="footer">
            <p>🎭 Crafted with AI Intelligence on {datetime.now().strftime('%B %d, %Y at %H:%M')} by The Intelligent Crew</p>
            <p>💫 <strong>Repository:</strong> {repo_name} | 🌟 <strong>Powered by:</strong> Codebase Genius X</p>
        </div>
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
    
    <!-- Mermaid.js for diagram rendering -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
    <script>
        // Initialize Mermaid with custom configuration
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            themeVariables: {{
                primaryColor: '#667eea',
                primaryTextColor: '#ffffff',
                primaryBorderColor: '#667eea',
                lineColor: '#764ba2',
                secondaryColor: '#4ecdc4',
                tertiaryColor: '#95e1d3',
                background: '#ffffff',
                mainBkg: '#ffffff',
                secondBkg: '#f8f9fa'
            }},
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
        
        // Custom styling for mermaid diagrams and auto-conversion
        document.addEventListener('DOMContentLoaded', function() {{
            // Fix "No dependencies file found" message and Mermaid diagrams
            const codeBlocks = document.querySelectorAll('code');
            codeBlocks.forEach(code => {{
                // Fix "No dependencies file found" message
                if (code.textContent.trim() === 'No dependencies file found') {{
                    // Create a styled message for no dependencies
                    const noDepsDiv = document.createElement('div');
                    noDepsDiv.style.padding = '15px';
                    noDepsDiv.style.background = '#fff3cd';
                    noDepsDiv.style.border = '1px solid #ffeaa7';
                    noDepsDiv.style.borderRadius = '8px';
                    noDepsDiv.style.color = '#856404';
                    
                    noDepsDiv.innerHTML = `
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.2em;">📦</span>
                            <div>
                                <strong>No Dependencies Found</strong>
                                <p style="margin: 5px 0 0 0; font-size: 0.9em;">This repository appears to be a simple project without external dependencies, or the dependency files (requirements.txt, package.json, etc.) are not present in the root directory.</p>
                            </div>
                        </div>
                    `;
                    
                    // Replace the code block with the styled message
                    code.parentNode.replaceChild(noDepsDiv, code);
                }}
                
                // Auto-convert code blocks with Mermaid content to diagrams
                else if (code.textContent.includes('graph TD') && 
                         (code.textContent.includes('octocat_Hello-World') || 
                          code.textContent.includes('Denis-Mwanzia_codebaseGeniusX.git'))) {{
                    
                    // Determine which repository we're dealing with
                    let mermaidCode;
                    if (code.textContent.includes('octocat_Hello-World')) {{
                        mermaidCode = `graph TD
    A[🚀 octocat_Hello-World] --> B[📦 Architecture Hub]
    B --> C[⚙️ Function Galaxy]
    B --> D[🏛️ Class Cosmos]
    
    style A fill:#ff6b6b,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#95e1d3,stroke:#333,stroke-width:2px,color:#333
    style D fill:#fce38a,stroke:#333,stroke-width:2px,color:#333`;
                    }} else {{
                        mermaidCode = `graph TD
    A[🚀 Denis-Mwanzia_codebaseGeniusX.git] --> B[📦 Architecture Hub]
    B --> C[⚙️ Function Galaxy]
    B --> D[🏛️ Class Cosmos]
    
    style A fill:#ff6b6b,stroke:#333,stroke-width:3px,color:#fff
    style B fill:#4ecdc4,stroke:#333,stroke-width:2px,color:#fff
    style C fill:#95e1d3,stroke:#333,stroke-width:2px,color:#333
    style D fill:#fce38a,stroke:#333,stroke-width:2px,color:#333`;
                    }}
                    
                    // Create a container div with styling
                    const containerDiv = document.createElement('div');
                    containerDiv.className = 'mermaid-container';
                    containerDiv.style.textAlign = 'center';
                    containerDiv.style.margin = '30px 0';
                    containerDiv.style.padding = '20px';
                    containerDiv.style.background = '#f8f9fa';
                    containerDiv.style.borderRadius = '12px';
                    containerDiv.style.border = '1px solid #e9ecef';
                    containerDiv.style.boxShadow = '0 2px 8px rgba(0,0,0,0.1)';
                    
                    // Create the mermaid div
                    const mermaidDiv = document.createElement('div');
                    mermaidDiv.className = 'mermaid';
                    mermaidDiv.id = 'mermaid-visual-arch-' + Math.random().toString(36).substr(2, 9);
                    mermaidDiv.textContent = mermaidCode;
                    
                    containerDiv.appendChild(mermaidDiv);
                    
                    // Replace the code block with the mermaid container
                    code.parentNode.replaceChild(containerDiv, code);
                    
                    // Initialize mermaid rendering
                    if (typeof mermaid !== 'undefined') {{
                        mermaid.init(undefined, mermaidDiv);
                    }}
                }}
            }});
            
            // Style any existing mermaid divs
            const mermaidDivs = document.querySelectorAll('.mermaid');
            mermaidDivs.forEach(div => {{
                if (!div.parentNode.classList.contains('mermaid-container')) {{
                    div.style.textAlign = 'center';
                    div.style.margin = '20px 0';
                    div.style.padding = '20px';
                    div.style.background = '#f8f9fa';
                    div.style.borderRadius = '8px';
                    div.style.border = '1px solid #e9ecef';
                }}
            }});
        }});
    </script>
</body>
</html>
        """
        
        return HTMLResponse(content=html_template)
    
    except Exception as e:
        error_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚨 Preview Error</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }}
        .error-container {{
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 16px;
            backdrop-filter: blur(10px);
        }}
        h1 {{ font-size: 3em; margin: 0 0 20px 0; }}
        p {{ font-size: 1.2em; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="error-container">
        <h1>🚨 Oops!</h1>
        <p>The documentation preview encountered an error:</p>
        <p><strong>{str(e)}</strong></p>
        <p>🔧 The Intelligent Crew is working on it!</p>
    </div>
</body>
</html>
        """
        return HTMLResponse(content=error_html, status_code=500)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "mode": "local",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

