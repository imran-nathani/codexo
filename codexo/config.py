import toml
from pathlib import Path
from typing import Dict, Any


def load_config(project_path: Path) -> Dict[str, Any]:
    """Load configuration from codexo.config file if it exists."""
    config_path = project_path / 'codexo.config'
    
    if not config_path.exists():
        return {}
    
    try:
        config_data = toml.load(config_path)
        
        # Flatten nested structure for easier access
        flat_config = {}
        
        # Thresholds
        if 'thresholds' in config_data:
            flat_config['loc_threshold'] = config_data['thresholds'].get('loc', 800)
            flat_config['complexity_threshold'] = config_data['thresholds'].get('complexity', 10)
        
        # Files
        if 'files' in config_data:
            flat_config['files'] = config_data['files'].get('include', ['py'])
            flat_config['exclude'] = config_data['files'].get('exclude', [])
        
        # Output
        if 'output' in config_data:
            flat_config['output_format'] = config_data['output'].get('format', 'table')
            flat_config['output_file'] = config_data['output'].get('file')
            flat_config['sort_by'] = config_data['output'].get('sort_by', 'loc')
        
        # Analysis
        if 'analysis' in config_data:
            flat_config['calculate_complexity'] = config_data['analysis'].get('calculate_complexity', False)
            flat_config['include_cyclomatic'] = config_data['analysis'].get('include_cyclomatic', True)
        
        return flat_config
    
    except Exception as e:
        print(f"Warning: Could not load config file: {e}")
        return {}


def create_default_config(project_path: Path) -> None:
    """Create a default codexo.config file in the project."""
    config_path = project_path / 'codexo.config'
    
    default_config = """# CodeX O Configuration File

[thresholds]
loc = 800
complexity = 10

[files]
include = ["py"]
# exclude = ["test_*.py", "*_test.py"]

[output]
format = "table"  # Options: table, json, csv
# file = "codexo-report.txt"
sort_by = "loc"  # Options: loc, complexity, filename

[analysis]
calculate_complexity = true
include_cyclomatic = true
"""
    
    config_path.write_text(default_config)
    print(f"✅ Created default config at: {config_path}")
