"""
Jac Orchestrator
Executes Jac walkers and integrates with Python backend
"""

import os
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# Try to import jaclang for Jaseci 2.0.0
try:
    from jaclang import JacMachine
    from jaclang.runtimelib.machine import JacMachineImpl
    JAC_AVAILABLE = True
    print("✓ Jaseci 2.0.0 (jaclang) available - using Jac runtime")
except ImportError:
    JAC_AVAILABLE = False
    print("Warning: Jaseci not available, falling back to Python implementation")

from abilities import (
    git_clone_repo, build_file_tree, summarize_readme,
    parse_code_structure, build_code_context_graph,
    generate_markdown_docs, generate_mermaid_diagram,
    embed_diagram_in_docs, extract_repo_name, save_documentation
)
from utils.file_utils import FileUtils
from utils.parser import CodeParser
from utils.gemini_client import GeminiClient


class JacOrchestrator:
    """Orchestrates the multi-agent workflow"""
    
    def __init__(self):
        self.file_utils = FileUtils()
        self.parser = CodeParser()
        self.gemini = GeminiClient()
        self.abilities_registered = False
        
    def register_abilities(self):
        """Register abilities with Jaseci (placeholder for future implementation)"""
        # TODO: Implement for Jaseci 2.0.0 when API is clarified  
        return False
    
    def execute_workflow(self, github_url: str) -> Dict[str, Any]:
        """
        Execute the multi-agent workflow
        Falls back to Python implementation if Jac not available
        """
        # For now, always use Python implementation
        # Jaseci 2.0.0 has significantly different API and syntax
        # TODO: Update to use new JacMachine API when syntax is clarified
        print("🐍 Using Python implementation (Jaseci 2.0.0 API integration pending)")
        return self._execute_python_workflow(github_url)
    
    def _execute_python_workflow(self, github_url: str) -> Dict[str, Any]:
        """
        Python implementation of the workflow
        This is what currently works
        """
        print("🧭 Captain: Starting mission (Python mode)")
        
        # Step 1: Clone repository
        print("🗺️ Navigator: Cloning repository...")
        repo_path = self.file_utils.clone_repository(github_url)
        if not repo_path:
            raise Exception("Failed to clone repository")
        
        # Step 2: Build file tree
        print("🗺️ Navigator: Building file tree...")
        file_tree = self.file_utils.build_file_tree(repo_path)
        
        # Step 3: Summarize README
        print("🗺️ Navigator: Summarizing README...")
        readme_content = self.file_utils.get_readme(repo_path)
        readme_summary = self.gemini.summarize_readme(readme_content)
        
        # Step 4: Build code graph
        print("🔍 Inspector: Analyzing code structure...")
        code_graph = self.parser.build_code_context_graph(repo_path)
        
        # Step 5: Generate documentation
        print("✍️ Author: Writing documentation...")
        context = {
            'code_graph': code_graph,
            'file_tree': file_tree,
            'readme_summary': readme_summary,
            'repo_url': github_url
        }
        documentation = self.gemini.generate_documentation(context)
        
        # Step 6: Generate diagram
        print("🎨 Designer: Creating diagrams...")
        diagram = self.gemini.generate_diagram(code_graph, file_tree)
        
        # Step 7: Save all files
        print("🎨 Designer: Saving files...")
        repo_name = os.path.basename(repo_path)
        doc_path = self.file_utils.save_documentation(documentation, repo_name)
        file_tree_path = self.file_utils.save_file_tree(file_tree, repo_name)
        code_graph_path = self.file_utils.save_code_graph(code_graph, repo_name)
        diagram_path = self.file_utils.save_diagram(diagram, repo_name)
        
        # Step 8: Cleanup cloned repository
        print("🧹 Cleaning up cloned repository...")
        self.file_utils.cleanup_repository(repo_path)
        
        print("✅ Mission complete!")
        
        return {
            "status": "success",
            "message": "Analysis completed successfully",
            "result": {
                "repo_name": repo_name,
                "output_path": doc_path,
                "file_tree": file_tree,
                "code_graph": code_graph,
                "files": {
                    "documentation": doc_path,
                    "file_tree": file_tree_path,
                    "code_graph": code_graph_path,
                    "diagram": diagram_path
                }
            }
        }


# Global orchestrator instance
_orchestrator = None

def get_orchestrator() -> JacOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = JacOrchestrator()
        _orchestrator.register_abilities()
    return _orchestrator


