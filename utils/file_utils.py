"""
File Utilities for Codebase Genius X
Handles Git operations and file system operations
"""

import git
from pathlib import Path
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse
import os
import json
import re


class FileUtils:
    """Utility functions for file operations"""
    
    def clone_repository(self, github_url: str, output_dir: str = "outputs") -> Optional[str]:
        """Clone a GitHub repository"""
        try:
            parsed = urlparse(github_url)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) < 2:
                raise ValueError(f"Invalid GitHub URL: {github_url}")
            
            repo_name = f"{path_parts[-2]}_{path_parts[-1]}"
            repo_dir = Path(output_dir) / repo_name
            
            # Create output directory
            repo_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if already cloned
            if (repo_dir / '.git').exists():
                print(f"Repository already exists at {repo_dir}")
                return str(repo_dir)
            
            # Clone repository
            print(f"Cloning {github_url} to {repo_dir}")
            git.Repo.clone_from(github_url, str(repo_dir), depth=1)
            
            return str(repo_dir)
        
        except Exception as e:
            print(f"Error cloning repository: {e}")
            return None
    
    def cleanup_repository(self, repo_path: str):
        """Remove cloned repository files, keeping only generated docs"""
        try:
            import shutil
            repo_dir = Path(repo_path)
            if not repo_dir.exists():
                return
            
            print(f"Cleaning up repository at {repo_dir}")
            
            # Files to keep
            keep_files = ['docs.md', 'diagram.mmd', 'code_graph.json', 'file_tree.json']
            
            # Remove everything except keep_files
            for item in repo_dir.iterdir():
                if item.name in keep_files:
                    continue
                
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    # Remove all directories
                    shutil.rmtree(item, ignore_errors=True)
            
            print(f"Repository cleaned up, kept only generated docs")
        
        except Exception as e:
            print(f"Error cleaning up repository: {e}")
    
    def build_file_tree(self, repo_path: str, max_depth: int = 4) -> Dict[str, Any]:
        """Build a tree representation of the repository"""
        repo_path_obj = Path(repo_path)
        
        def walk_directory(path: Path, depth: int = 0) -> List[Dict]:
            if depth > max_depth:
                return []
            
            items = []
            try:
                for item in sorted(path.iterdir()):
                    if item.name.startswith('.') or item.name.startswith('__'):
                        continue
                    
                    if item.is_dir():
                        items.append({
                            'name': item.name,
                            'type': 'directory',
                            'children': walk_directory(item, depth + 1)
                        })
                    elif item.suffix in ['.py', '.js', '.ts', '.tsx', '.jsx', '.jac', '.json', '.md']:
                        items.append({
                            'name': item.name,
                            'type': 'file',
                            'path': str(item.relative_to(repo_path))
                        })
            except PermissionError:
                pass
            
            return items
        
        tree = {
            'name': repo_path_obj.name,
            'type': 'directory',
            'children': walk_directory(repo_path_obj)
        }
        
        # Add framework and language detection
        tree['metadata'] = self._detect_framework_and_language(repo_path_obj)
        
        return tree
    
    def _detect_framework_and_language(self, repo_path: Path) -> Dict[str, Any]:
        """Detect framework and primary language from repository"""
        metadata = {
            'languages': [],
            'framework': None,
            'build_tool': None,
            'runtime': None
        }
        
        # Check package.json for Node.js projects
        package_json = repo_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                all_deps = {**deps, **dev_deps}
                
                # Detect framework
                if 'react' in all_deps:
                    metadata['framework'] = 'React'
                    if 'vite' in all_deps:
                        metadata['build_tool'] = 'Vite'
                    elif 'next' in all_deps:
                        metadata['framework'] = 'Next.js'
                    elif 'create-react-app' in all_deps:
                        metadata['build_tool'] = 'Create React App'
                
                if 'vue' in all_deps:
                    metadata['framework'] = 'Vue.js'
                
                if 'angular' in all_deps:
                    metadata['framework'] = 'Angular'
                
                if 'express' in all_deps:
                    metadata['framework'] = 'Express.js'
                
                if 'nestjs' in all_deps:
                    metadata['framework'] = 'NestJS'
                
                if 'fastapi' in all_deps:
                    metadata['framework'] = 'FastAPI'
                
                # Detect TypeScript
                if 'typescript' in all_deps:
                    metadata['languages'].append('TypeScript')
                else:
                    metadata['languages'].append('JavaScript')
                
                # Detect runtime
                if 'next' in all_deps:
                    metadata['runtime'] = 'Node.js (SSR)'
                else:
                    metadata['runtime'] = 'Node.js'
                    
            except Exception as e:
                print(f"Error reading package.json: {e}")
        
        # Check for Python files
        python_files = list(repo_path.rglob('*.py'))
        if python_files:
            metadata['languages'].append('Python')
            
            # Check for Python frameworks
            if not metadata['framework']:
                requirements = repo_path / 'requirements.txt'
                if requirements.exists():
                    with open(requirements, 'r') as f:
                        content = f.read()
                        if 'fastapi' in content:
                            metadata['framework'] = 'FastAPI'
                        elif 'flask' in content:
                            metadata['framework'] = 'Flask'
                        elif 'django' in content:
                            metadata['framework'] = 'Django'
        
        # Check for Java files
        java_files = list(repo_path.rglob('*.java'))
        if java_files:
            metadata['languages'].append('Java')
        
        # Check for Go files
        go_files = list(repo_path.rglob('*.go'))
        if go_files:
            metadata['languages'].append('Go')
        
        # Check for Rust files
        rust_files = list(repo_path.rglob('*.rs'))
        if rust_files:
            metadata['languages'].append('Rust')
        
        return metadata
    
    def get_readme(self, repo_path: str) -> str:
        """Extract README content"""
        repo_path_obj = Path(repo_path)
        readme_names = ['README.md', 'README.rst', 'README.txt', 'README']
        
        for name in readme_names:
            readme_path = repo_path_obj / name
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"Error reading README: {e}")
        
        return ""
    
    def save_documentation(self, documentation: str, repo_name: str, output_dir: str = "outputs"):
        """Save documentation to file"""
        output_path = Path(output_dir) / repo_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        doc_file = output_path / "docs.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(documentation)
        
        print(f"Documentation saved to {doc_file}")
        return str(doc_file)
    
    def save_file_tree(self, file_tree: Dict[str, Any], repo_name: str, output_dir: str = "outputs"):
        """Save file tree as JSON"""
        output_path = Path(output_dir) / repo_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_tree_json = output_path / "file_tree.json"
        with open(file_tree_json, 'w', encoding='utf-8') as f:
            json.dump(file_tree, f, indent=2)
        
        print(f"File tree saved to {file_tree_json}")
        return str(file_tree_json)
    
    def save_code_graph(self, code_graph: Dict[str, Any], repo_name: str, output_dir: str = "outputs"):
        """Save code graph as JSON"""
        output_path = Path(output_dir) / repo_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        code_graph_json = output_path / "code_graph.json"
        with open(code_graph_json, 'w', encoding='utf-8') as f:
            json.dump(code_graph, f, indent=2)
        
        print(f"Code graph saved to {code_graph_json}")
        return str(code_graph_json)
    
    def save_diagram(self, diagram_content: str, repo_name: str, output_dir: str = "outputs"):
        """Save Mermaid diagram"""
        output_path = Path(output_dir) / repo_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        diagram_file = output_path / "diagram.mmd"
        with open(diagram_file, 'w', encoding='utf-8') as f:
            f.write(diagram_content)
        
        print(f"Diagram saved to {diagram_file}")
        return str(diagram_file)

