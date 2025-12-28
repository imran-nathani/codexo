import click
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from .analyzer import FileAnalyzer
from .config import load_config
from .report import generate_report


@click.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--files', '-f', default=None, help='Comma-separated file extensions (e.g., py,js,ts)')
@click.option('--loc', '-l', type=int, default=None, help='Minimum lines of code threshold')
@click.option('--output', '-o', type=click.Path(), default=None, help='Output file path')
@click.option('--complexity', '-c', is_flag=True, help='Calculate complexity metrics')
@click.option('--format', type=click.Choice(['table', 'json', 'csv']), default='table', help='Output format')
@click.option('--sort-by', type=click.Choice(['loc', 'complexity', 'filename']), default='loc', help='Sort results by')
def cli(path: str, files: Optional[str], loc: Optional[int], output: Optional[str], 
        complexity: bool, format: str, sort_by: str):
    """
    CodeX O - Analyze code complexity and file sizes to keep your codebase maintainable.
    
    Examples:
        codexo
        codexo /path/to/project --files=py,js --loc=900
        codexo . --complexity --output=report.txt
    """
    project_path = Path(path).resolve()
    
    # Load config file if exists
    config = load_config(project_path)
    
    # CLI args override config
    file_extensions = files.split(',') if files else config.get('files', ['py'])
    loc_threshold = loc if loc is not None else config.get('loc_threshold', 800)
    calculate_complexity = complexity or config.get('calculate_complexity', False)
    output_format = format if format != 'table' else config.get('output_format', 'table')
    sort_by_field = sort_by if sort_by != 'loc' else config.get('sort_by', 'loc')
    
    click.echo(f"🔍 Analyzing project: {project_path}")
    click.echo(f"📊 File types: {', '.join(file_extensions)}")
    click.echo(f"📏 LOC threshold: {loc_threshold}")
    if calculate_complexity:
        click.echo(f"🧮 Complexity analysis: enabled")
    click.echo()
    
    # Analyze files
    analyzer = FileAnalyzer(project_path, file_extensions, loc_threshold, calculate_complexity)
    results = analyzer.analyze()
    
    if not results:
        click.echo("✅ No files exceed the thresholds. Great job keeping your code maintainable!")
        return
    
    # Generate report
    report = generate_report(results, output_format, sort_by_field)
    
    # Output
    if output:
        output_path = Path(output)
        output_path.write_text(report)
        click.echo(f"📝 Report saved to: {output_path}")
    else:
        click.echo(report)
    
    # Exit with error code if files exceed threshold (useful for CI/CD)
    if results:
        sys.exit(1)


if __name__ == '__main__':
    cli()
