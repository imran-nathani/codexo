import os
from pathlib import Path
from typing import List, Dict, Optional
import pathspec
from radon.complexity import cc_visit
from radon.metrics import mi_visit


class FileAnalyzer:
    """Analyzes code files for LOC and complexity metrics."""
    
    def __init__(self, project_path: Path, file_extensions: List[str], 
                 loc_threshold: int, calculate_complexity: bool):
        self.project_path = project_path
        self.file_extensions = file_extensions
        self.loc_threshold = loc_threshold
        self.calculate_complexity = calculate_complexity
        self.gitignore_spec = self._load_gitignore()
        
    def _load_gitignore(self) -> Optional[pathspec.PathSpec]:
        """Load .gitignore patterns if available."""
        gitignore_path = self.project_path / '.gitignore'
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                patterns = f.read().splitlines()
            return pathspec.PathSpec.from_lines('gitwildmatch', patterns)
        return None
    
    def _should_skip(self, path: Path) -> bool:
        """Check if path should be skipped based on common patterns."""
        skip_dirs = {
            '__pycache__', 'node_modules', 'venv', 'env', '.venv',
            '.git', '.idea', '.vscode', 'dist', 'build', '.pytest_cache',
            '.mypy_cache', '.tox', 'htmlcov', '.eggs', '*.egg-info'
        }
        
        # Check if any parent directory matches skip patterns
        for part in path.parts:
            if part in skip_dirs or part.startswith('.') and part not in {'.github', '.gitlab'}:
                return True
        
        # Check gitignore
        if self.gitignore_spec:
            relative_path = path.relative_to(self.project_path)
            if self.gitignore_spec.match_file(str(relative_path)):
                return True
        
        return False
    
    def _count_loc(self, file_path: Path) -> int:
        """Count non-empty, non-comment lines of code."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            loc = 0
            in_multiline_comment = False
            
            for line in lines:
                stripped = line.strip()
                
                # Skip empty lines
                if not stripped:
                    continue
                
                # Handle Python multiline comments/docstrings
                if file_path.suffix == '.py':
                    if '"""' in stripped or "'''" in stripped:
                        if in_multiline_comment:
                            in_multiline_comment = False
                            continue
                        else:
                            in_multiline_comment = True
                            if stripped.count('"""') == 2 or stripped.count("'''") == 2:
                                in_multiline_comment = False
                            continue
                    
                    if in_multiline_comment:
                        continue
                    
                    # Skip single-line comments
                    if stripped.startswith('#'):
                        continue
                
                loc += 1
            
            return loc
        except Exception:
            return 0
    
    def _calculate_complexity(self, file_path: Path) -> Optional[Dict]:
        """Calculate complexity metrics for Python files."""
        if file_path.suffix != '.py':
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                code = f.read()
            
            # Cyclomatic complexity
            complexity_results = cc_visit(code)
            
            if complexity_results:
                avg_complexity = sum(r.complexity for r in complexity_results) / len(complexity_results)
                max_complexity = max(r.complexity for r in complexity_results)
                
                return {
                    'average': round(avg_complexity, 2),
                    'max': max_complexity,
                    'functions': len(complexity_results)
                }
            
            return None
        except Exception:
            return None
    
    def analyze(self) -> List[Dict]:
        """Analyze all files in the project matching criteria."""
        results = []
        
        for root, dirs, files in os.walk(self.project_path):
            root_path = Path(root)
            
            # Skip directories
            if self._should_skip(root_path):
                dirs.clear()  # Don't recurse into this directory
                continue
            
            for file in files:
                file_path = root_path / file
                
                # Check file extension
                if not any(file.endswith(f'.{ext}') for ext in self.file_extensions):
                    continue
                
                # Skip if path should be ignored
                if self._should_skip(file_path):
                    continue
                
                # Count LOC
                loc = self._count_loc(file_path)
                
                # Only include files exceeding threshold
                if loc < self.loc_threshold:
                    continue
                
                result = {
                    'file': str(file_path.relative_to(self.project_path)),
                    'loc': loc
                }
                
                # Add complexity if requested
                if self.calculate_complexity:
                    complexity = self._calculate_complexity(file_path)
                    if complexity:
                        result['complexity'] = complexity
                
                results.append(result)
        
        return results
