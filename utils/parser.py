"""
Code Parser for Codebase Genius X
Handles parsing of Python, JavaScript, TypeScript files using AST and Tree-sitter
"""

import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import re


class CodeParser:
    """Parser for building Code Context Graph"""
    
    def __init__(self):
        self.language_stats = {}
    
    def build_code_context_graph(self, repo_path: str) -> Dict[str, Any]:
        """Build Code Context Graph from repository"""
        graph = {
            "nodes": [],
            "edges": [],
            "modules": {},
            "language_stats": {},
            "dependencies": []
        }
        
        repo_path_obj = Path(repo_path)
        
        # Detect and parse files by language
        self._parse_python_files(repo_path_obj, repo_path, graph)
        self._parse_javascript_files(repo_path_obj, repo_path, graph)
        self._parse_typescript_files(repo_path_obj, repo_path, graph)
        
        # Extract dependencies
        graph['dependencies'] = self._extract_dependencies(repo_path_obj)
        
        # Add language statistics
        graph['language_stats'] = self.language_stats
        
        return graph
    
    def _parse_python_files(self, repo_path_obj: Path, repo_path: str, graph: Dict):
        """Parse Python files"""
        for py_file in repo_path_obj.rglob('*.py'):
            if self._should_skip_file(py_file):
                continue
            
            try:
                module_data = self._parse_python_file(py_file, repo_path_obj)
                if module_data:
                    module_id = module_data['id']
                    graph['modules'][module_id] = module_data
                    graph['nodes'].extend(module_data['classes'])
                    graph['nodes'].extend(module_data['functions'])
                    self.language_stats['Python'] = self.language_stats.get('Python', 0) + 1
            except Exception as e:
                print(f"Error parsing {py_file}: {e}")
                continue
        
    def _parse_javascript_files(self, repo_path_obj: Path, repo_path: str, graph: Dict):
        """Parse JavaScript files"""
        # Parse .js files
        for js_file in repo_path_obj.rglob('*.js'):
            if self._should_skip_file(js_file):
                continue
            
            try:
                module_data = self._parse_javascript_file(js_file, repo_path_obj)
                if module_data:
                    module_id = module_data['id']
                    graph['modules'][module_id] = module_data
                    graph['nodes'].extend(module_data['classes'])
                    graph['nodes'].extend(module_data['functions'])
                    graph['nodes'].extend(module_data.get('components', []))
                    self.language_stats['JavaScript'] = self.language_stats.get('JavaScript', 0) + 1
            except Exception as e:
                print(f"Error parsing {js_file}: {e}")
                continue
        
        # Parse .jsx files
        for jsx_file in repo_path_obj.rglob('*.jsx'):
            if self._should_skip_file(jsx_file):
                continue
            
            try:
                module_data = self._parse_javascript_file(jsx_file, repo_path_obj)
                if module_data:
                    module_id = module_data['id']
                    graph['modules'][module_id] = module_data
                    graph['nodes'].extend(module_data['classes'])
                    graph['nodes'].extend(module_data['functions'])
                    graph['nodes'].extend(module_data.get('components', []))
                    self.language_stats['JavaScript'] = self.language_stats.get('JavaScript', 0) + 1
            except Exception as e:
                print(f"Error parsing {jsx_file}: {e}")
                continue
    
    def _parse_typescript_files(self, repo_path_obj: Path, repo_path: str, graph: Dict):
        """Parse TypeScript files"""
        # Parse .ts files
        for ts_file in repo_path_obj.rglob('*.ts'):
            if self._should_skip_file(ts_file):
                continue
            
            # Skip .d.ts files
            if ts_file.suffixes == ['.d', '.ts']:
                continue
            
            try:
                module_data = self._parse_typescript_file(ts_file, repo_path_obj)
                if module_data:
                    module_id = module_data['id']
                    graph['modules'][module_id] = module_data
                    graph['nodes'].extend(module_data['classes'])
                    graph['nodes'].extend(module_data['functions'])
                    graph['nodes'].extend(module_data.get('components', []))
                    self.language_stats['TypeScript'] = self.language_stats.get('TypeScript', 0) + 1
            except Exception as e:
                print(f"Error parsing {ts_file}: {e}")
                continue
        
        # Parse .tsx files
        for tsx_file in repo_path_obj.rglob('*.tsx'):
            if self._should_skip_file(tsx_file):
                continue
            
            try:
                print(f"🔬 Analyzing React+TypeScript magic in: {tsx_file}")
                module_data = self._parse_typescript_file(tsx_file, repo_path_obj)
                if module_data:
                    components_count = len(module_data.get('components', []))
                    functions_count = len(module_data.get('functions', []))
                    classes_count = len(module_data.get('classes', []))
                    
                    if components_count > 0:
                        print(f"🎭 Discovered {components_count} React components - the stars of the show!")
                    if functions_count > 0:
                        print(f"⚙️ Found {functions_count} functions - the hardworking crew!")
                    if classes_count > 0:
                        print(f"🏛️ Spotted {classes_count} classes - the architectural masterpieces!")
                    module_id = module_data['id']
                    graph['modules'][module_id] = module_data
                    graph['nodes'].extend(module_data['classes'])
                    graph['nodes'].extend(module_data['functions'])
                    graph['nodes'].extend(module_data.get('components', []))
                    self.language_stats['TypeScript'] = self.language_stats.get('TypeScript', 0) + 1
            except Exception as e:
                print(f"Error parsing {tsx_file}: {e}")
                continue
    
    def _parse_python_file(self, file_path: Path, repo_path: Path) -> Dict[str, Any]:
        """Parse a Python file and extract structure"""
        rel_path = str(file_path.relative_to(repo_path))
        module_id = rel_path.replace('/', '_').replace('.py', '')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        
        classes = []
        functions = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'id': f"{module_id}.{node.name}",
                    'type': 'class',
                    'name': node.name,
                    'module': module_id
                })
            elif isinstance(node, ast.FunctionDef):
                functions.append({
                    'id': f"{module_id}.{node.name}",
                    'type': 'function',
                    'name': node.name,
                    'module': module_id
                })
        
        return {
            'id': module_id,
            'path': rel_path,
            'classes': classes,
            'functions': functions
        }
    
    def _parse_javascript_file(self, file_path: Path, repo_path: Path) -> Dict[str, Any]:
        """Parse a JavaScript file and extract structure"""
        rel_path = str(file_path.relative_to(repo_path))
        module_id = rel_path.replace('/', '_').replace('.js', '').replace('.jsx', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        
        functions = []
        classes = []
        components = []
        imports = []
        exports = []
        
        # Extract imports - more comprehensive pattern
        import_pattern = r"import\s+(?:.*?\s+from\s+)?['\"]([^'\"]+)['\"]"
        imports = re.findall(import_pattern, content)
        
        # Extract exports - improved pattern
        export_pattern = r"export\s+(?:default\s+)?(?:class|function|const|let|var|interface|type)\s+(\w+)"
        exports_found = re.findall(export_pattern, content)
        exports.extend(exports_found)
        
        # Extract functions - including async
        func_pattern = r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\("
        functions_found = re.findall(func_pattern, content)
        for func_name in functions_found:
            functions.append({
                'id': f"{module_id}.{func_name}",
                'type': 'function',
                'name': func_name,
                'module': module_id
            })
        
        # Extract arrow functions - improved pattern
        arrow_pattern = r"(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>"
        arrow_functions = re.findall(arrow_pattern, content)
        for func_name in arrow_functions:
            functions.append({
                'id': f"{module_id}.{func_name}",
                'type': 'function',
                'name': func_name,
                'module': module_id
            })
        
        # Extract classes
        class_pattern = r"(?:export\s+)?class\s+(\w+)"
        classes_found = re.findall(class_pattern, content)
        for class_name in classes_found:
            classes.append({
                'id': f"{module_id}.{class_name}",
                'type': 'class',
                'name': class_name,
                'module': module_id
            })
        
        # Extract React components - improved pattern
        # Pattern for: export const ComponentName = ({ ... }) => {
        react_component_pattern = r"(?:export\s+)?(?:const|function)\s+(\w+)\s*[:=].*?=>\s*\{"
        components_found = re.findall(react_component_pattern, content)
        for comp_name in components_found:
            # Only add if it looks like a component (uppercase first letter)
            if comp_name and comp_name[0].isupper():
                components.append({
                    'id': f"{module_id}.{comp_name}",
                    'type': 'component',
                    'name': comp_name,
                    'module': module_id
                })
        
        # Only return if we found something
        if not (functions or classes or components):
            return None
        
        return {
            'id': module_id,
            'path': rel_path,
            'language': 'javascript',
            'classes': classes,
            'functions': functions,
            'components': components,
            'imports': imports,
            'exports': exports
        }
    
    def _parse_typescript_file(self, file_path: Path, repo_path: Path) -> Dict[str, Any]:
        """Parse a TypeScript file and extract structure"""
        rel_path = str(file_path.relative_to(repo_path))
        module_id = rel_path.replace('/', '_').replace('.ts', '').replace('.tsx', '')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None
        
        functions = []
        classes = []
        components = []
        imports = []
        exports = []
        
        # Extract imports - improved pattern
        import_pattern = r"import\s+(?:.*?\s+from\s+)?['\"]([^'\"]+)['\"]"
        imports = re.findall(import_pattern, content)
        
        # Extract exports - improved pattern
        export_pattern = r"export\s+(?:default\s+)?(?:class|function|const|let|var|interface|type)\s+(\w+)"
        exports_found = re.findall(export_pattern, content)
        exports.extend(exports_found)
        
        # Extract functions
        func_pattern = r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*[<\(]"
        functions_found = re.findall(func_pattern, content)
        for func_name in functions_found:
            functions.append({
                'id': f"{module_id}.{func_name}",
                'type': 'function',
                'name': func_name,
                'module': module_id
            })
        
        # Extract arrow functions - improved pattern for TypeScript
        arrow_pattern = r"(?:export\s+)?(?:const|let|var)\s+(\w+)\s*[:=]\s*(?:[^=]*)?=>\s*\{"
        arrow_functions = re.findall(arrow_pattern, content)
        for func_name in arrow_functions:
            functions.append({
                'id': f"{module_id}.{func_name}",
                'type': 'function',
                'name': func_name,
                'module': module_id
            })
        
        # Extract classes
        class_pattern = r"(?:export\s+)?class\s+(\w+)"
        classes_found = re.findall(class_pattern, content)
        for class_name in classes_found:
            classes.append({
                'id': f"{module_id}.{class_name}",
                'type': 'class',
                'name': class_name,
                'module': module_id
            })
        
        # Extract React components - improved pattern for TSX
        # Pattern for: export const ComponentName: React.FC<Props> = ({ ... }) => {
        react_component_pattern1 = r"(?:export\s+)?(?:const|function)\s+(\w+)\s*:\s*React\.FC"
        # Pattern for: export const ComponentName = ({ ... }) => {
        react_component_pattern2 = r"(?:export\s+)?(?:const|function)\s+(\w+)\s*[:=].*?=>\s*\{"
        
        components_found1 = re.findall(react_component_pattern1, content)
        components_found2 = re.findall(react_component_pattern2, content)
        
        all_components = set(components_found1 + components_found2)
        for comp_name in all_components:
            # Only add if it looks like a component (uppercase first letter)
            if comp_name and comp_name[0].isupper():
                components.append({
                    'id': f"{module_id}.{comp_name}",
                    'type': 'component',
                    'name': comp_name,
                    'module': module_id
                })
        
        # Only return if we found something
        if not (functions or classes or components):
            return None
        
        return {
            'id': module_id,
            'path': rel_path,
            'language': 'typescript',
            'classes': classes,
            'functions': functions,
            'components': components,
            'imports': imports,
            'exports': exports
        }
    
    def _extract_dependencies(self, repo_path: Path) -> List[Dict[str, str]]:
        """Extract dependencies from package.json or requirements.txt"""
        dependencies = []
        
        # Check for package.json (Node.js/JavaScript)
        package_json = repo_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Extract dependencies
                deps = data.get('dependencies', {})
                dev_deps = data.get('devDependencies', {})
                
                for name, version in deps.items():
                    dependencies.append({
                        'name': name,
                        'version': version,
                        'type': 'dependency'
                    })
                
                for name, version in dev_deps.items():
                    dependencies.append({
                        'name': name,
                        'version': version,
                        'type': 'devDependency'
                    })
            except Exception as e:
                print(f"Error reading package.json: {e}")
        
        # Check for requirements.txt (Python)
        requirements_txt = repo_path / 'requirements.txt'
        if requirements_txt.exists():
            try:
                with open(requirements_txt, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Parse package name and version
                            if '==' in line:
                                name, version = line.split('==', 1)
                                dependencies.append({
                                    'name': name.strip(),
                                    'version': version.strip(),
                                    'type': 'dependency'
                                })
                            else:
                                dependencies.append({
                                    'name': line,
                                    'version': 'latest',
                                    'type': 'dependency'
                                })
            except Exception as e:
                print(f"Error reading requirements.txt: {e}")
        
        return dependencies
    
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        path_str = str(file_path)
        
        # More specific patterns to avoid false matches
        skip_patterns = [
            '__pycache__',
            '/venv/',
            '/.venv/',
            '/node_modules/',
            '/.git/',
            '/dist/',
            '/build/',
            'node_modules',
        ]
        
        # Check for .git directory (but not .git extension in file names)
        if '/.git/' in path_str or path_str.endswith('/.git'):
            return True
        
        # Check if any pattern matches
        for pattern in skip_patterns:
            if pattern in path_str:
                return True
        
        return False

