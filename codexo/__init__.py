"""
CodeX O - Code Complexity Analyzer

A tool to analyze code complexity and file sizes to keep your codebase
maintainable and LLM-friendly.
"""

__version__ = "0.1.0"
__author__ = "Imran Nathani"

from .main import cli
from .analyzer import FileAnalyzer
from .config import load_config, create_default_config
from .report import generate_report

__all__ = [
    'cli',
    'FileAnalyzer',
    'load_config',
    'create_default_config',
    'generate_report',
]
