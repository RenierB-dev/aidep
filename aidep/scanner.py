"""
Scanner module to read and parse Python dependency files.
Supports requirements.txt and pyproject.toml
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from packaging.version import parse as parse_version
from packaging.specifiers import SpecifierSet


class DependencyScanner:
    """Scans Python projects for dependencies."""
    
    AI_FRAMEWORKS = [
        "langchain",
        "langchain-core",
        "langchain-community",
        "langchain-openai",
        "llama-index",
        "llama-index-core",
        "openai",
        "anthropic",
        "crewai",
        "crewai-tools",
        "autogen",
        "langflow",
        "transformers",
        "torch",
        "tensorflow",
        "pydantic",
        "sqlalchemy",
    ]
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        
    def find_requirements_file(self) -> Optional[Path]:
        """Find requirements.txt or pyproject.toml in project."""
        req_files = [
            "requirements.txt",
            "requirements-dev.txt",
            "requirements/base.txt",
            "pyproject.toml",
        ]
        
        for req_file in req_files:
            file_path = self.project_path / req_file
            if file_path.exists():
                return file_path
        
        return None
    
    def parse_requirements_txt(self, file_path: Path) -> Dict[str, str]:
        """Parse requirements.txt file."""
        dependencies = {}
        
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                    
                # Skip -e editable installs and git URLs
                if line.startswith('-e') or line.startswith('git+'):
                    continue
                
                # Parse package name and version
                parsed = self._parse_requirement_line(line)
                if parsed:
                    name, version = parsed
                    dependencies[name.lower()] = version
        
        return dependencies
    
    def _parse_requirement_line(self, line: str) -> Optional[Tuple[str, str]]:
        """Parse a single requirement line."""
        # Remove inline comments
        line = line.split('#')[0].strip()
        
        # Match patterns like: package==1.0.0, package>=1.0.0, package<2.0.0
        match = re.match(r'^([a-zA-Z0-9\-_]+)([>=<~!]+.*)?$', line)
        
        if match:
            package_name = match.group(1)
            version_spec = match.group(2) if match.group(2) else ""
            return (package_name, version_spec.strip())
        
        return None
    
    def parse_pyproject_toml(self, file_path: Path) -> Dict[str, str]:
        """Parse pyproject.toml file."""
        dependencies = {}
        
        try:
            import tomllib
        except ImportError:
            import tomli as tomllib
        
        try:
            with open(file_path, 'rb') as f:
                data = tomllib.load(f)
            
            # Try different locations for dependencies
            dep_locations = [
                ('project', 'dependencies'),
                ('tool', 'poetry', 'dependencies'),
                ('tool', 'pdm', 'dependencies'),
            ]
            
            for location in dep_locations:
                deps = data
                for key in location:
                    deps = deps.get(key, {})
                    if not deps:
                        break
                
                if isinstance(deps, list):
                    # Poetry/PDM format: list of strings
                    for dep in deps:
                        if isinstance(dep, str):
                            parsed = self._parse_requirement_line(dep)
                            if parsed:
                                name, version = parsed
                                dependencies[name.lower()] = version
                
                elif isinstance(deps, dict):
                    # Alternative format: dict of name: version
                    for name, version in deps.items():
                        if name.lower() == 'python':
                            continue
                        if isinstance(version, str):
                            dependencies[name.lower()] = version
                        elif isinstance(version, dict):
                            version_str = version.get('version', '')
                            dependencies[name.lower()] = version_str
        
        except Exception:
            pass
        
        return dependencies
    
    def scan_project(self) -> Dict[str, str]:
        """Scan project for dependencies."""
        req_file = self.find_requirements_file()
        
        if not req_file:
            return {}
        
        if req_file.name == 'pyproject.toml':
            return self.parse_pyproject_toml(req_file)
        else:
            return self.parse_requirements_txt(req_file)
    
    def filter_ai_frameworks(self, dependencies: Dict[str, str]) -> Dict[str, str]:
        """Filter to only AI framework dependencies."""
        return {
            name: version
            for name, version in dependencies.items()
            if any(framework in name.lower() for framework in self.AI_FRAMEWORKS)
        }
    
    def check_version_in_range(self, version: str, spec: str) -> bool:
        """Check if a version satisfies a specifier."""
        try:
            if not spec or spec == "*":
                return True
            
            specifier_set = SpecifierSet(spec)
            return version in specifier_set
        except Exception:
            return False
