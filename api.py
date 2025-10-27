"""
FastAPI Backend for Codebase Genius X
Local Jac implementation (no cloud dependencies)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv

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

