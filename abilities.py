"""
Jac Abilities Module
Bridges Jac walkers with Python functionality

This module provides the bridge between Jac walkers (agents) and Python utility
classes. Each function here can be called from Jac code via the 'can' ability system.

Author: The Intelligent Crew
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json

# Import existing utilities
from utils.file_utils import FileUtils
from utils.parser import CodeParser
from utils.gemini_client import GeminiClient

# Initialize utilities as singletons
file_utils = FileUtils()
parser = CodeParser()
gemini = GeminiClient()


def git_clone_repo(github_url: str) -> Optional[str]:
    """
    Clone a GitHub repository to local storage.
    
    This function is called by the Navigator agent to fetch the repository
    that will be analyzed. The repository is cloned to the outputs/ directory.
    
    Args:
        github_url (str): Full GitHub repository URL (e.g., 
                         "https://github.com/user/repo.git")
    
    Returns:
        Optional[str]: Path to cloned repository directory, or None on error
    
    Called by: Navigator agent
    """
    return file_utils.clone_repository(github_url)


def build_file_tree(repo_path: str) -> Dict[str, Any]:
    """
    Build a hierarchical file tree structure of the repository.
    
    This function traverses the repository directory and creates a nested
    tree structure showing all files and folders. Also performs framework
    and language detection.
    
    Args:
        repo_path (str): Path to the cloned repository
    
    Returns:
        Dict[str, Any]: Tree structure with 'name', 'type', 'children', 
                       and 'metadata' fields
    
    Called by: Navigator agent
    """
    return file_utils.build_file_tree(repo_path)


def summarize_readme(repo_path: str) -> str:
    """
    Summarize the repository's README file using Gemini AI.
    
    Extracts the README content, sends it to Gemini for summarization,
    and returns a concise summary of the project.
    
    Args:
        repo_path (str): Path to the cloned repository
    
    Returns:
        str: AI-generated summary of the README content
    
    Called by: Navigator agent
    """
    readme_content = file_utils.get_readme(repo_path)
    return gemini.summarize_readme(readme_content)


def parse_code_structure(repo_path: str) -> Dict[str, Any]:
    """
    Parse code structure (alias for build_code_context_graph).
    
    This is a convenience alias that calls build_code_context_graph.
    Maintained for backward compatibility with Jac agent code.
    
    Args:
        repo_path (str): Path to the cloned repository
    
    Returns:
        Dict[str, Any]: Code Context Graph structure
    
    Called by: Inspector agent
    """
    return parser.build_code_context_graph(repo_path)


def build_code_context_graph(repo_path: str) -> Dict[str, Any]:
    """
    Build the Code Context Graph (CCG) from repository files.
    
    This is the core analysis function. It parses all code files in the
    repository, extracts functions, classes, components, and relationships,
    and builds a comprehensive graph structure representing the codebase.
    
    Args:
        repo_path (str): Path to the cloned repository
    
    Returns:
        Dict[str, Any]: Code Context Graph with nodes (functions, classes),
                       edges (relationships), modules, and statistics
    
    Called by: Inspector agent
    """
    return parser.build_code_context_graph(repo_path)


def generate_markdown_docs(context: Dict[str, Any]) -> str:
    """
    Generate comprehensive Markdown documentation using Gemini AI.
    
    Takes the complete analysis context (file tree, code graph, README summary)
    and uses Gemini to generate professional documentation in Markdown format.
    
    Args:
        context (Dict[str, Any]): Dictionary containing:
            - 'code_graph': The Code Context Graph
            - 'file_tree': The repository file tree
            - 'readme_summary': Summary of the README
            - 'repo_url': GitHub repository URL
    
    Returns:
        str: Complete Markdown documentation
    
    Called by: Author agent
    """
    context['repo_url'] = context.get('repo_url', '')
    return gemini.generate_documentation(context)


def generate_mermaid_diagram(code_graph: Dict[str, Any]) -> str:
    """
    Generate a Mermaid diagram from the Code Context Graph.
    
    Converts the code graph structure into a Mermaid diagram syntax
    that can be rendered in documentation. Shows module relationships
    and structure.
    
    Args:
        code_graph (Dict[str, Any]): The Code Context Graph
    
    Returns:
        str: Mermaid diagram syntax code
    
    Called by: Designer agent
    """
    file_tree = code_graph.get('file_tree', {})
    return gemini.generate_diagram(code_graph, file_tree)


def embed_diagram_in_docs(documentation: str, mermaid_diagram: str) -> str:
    """
    Embed Mermaid diagram into documentation.
    
    This function would normally parse and insert the diagram at the
    appropriate section. Currently, diagrams are embedded during
    generation, so this is a pass-through.
    
    Args:
        documentation (str): The generated documentation
        mermaid_diagram (str): The Mermaid diagram code
    
    Returns:
        str: Documentation with embedded diagram
    
    Called by: Designer agent
    """
    # Diagrams are already embedded during generation
    return documentation


def extract_repo_name(code_graph: Dict[str, Any]) -> str:
    """
    Extract repository name from the code graph metadata.
    
    Args:
        code_graph (Dict[str, Any]): The Code Context Graph containing file_tree
    
    Returns:
        str: Repository name or 'Unknown' if not found
    
    Called by: Designer agent
    """
    file_tree = code_graph.get('file_tree', {})
    return file_tree.get('name', 'Unknown')


def save_documentation(documentation: str, repo_name: str) -> str:
    """
    Save the generated documentation to a file.
    
    Writes the documentation Markdown to the outputs directory,
    organized by repository name.
    
    Args:
        documentation (str): The complete Markdown documentation
        repo_name (str): Name of the repository
    
    Returns:
        str: Path to the saved documentation file
    
    Called by: Designer agent
    """
    return file_utils.save_documentation(documentation, repo_name)


