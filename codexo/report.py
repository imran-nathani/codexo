import json
from typing import List, Dict


def generate_report(results: List[Dict], format: str, sort_by: str) -> str:
    """Generate report in specified format."""
    
    # Sort results
    if sort_by == 'loc':
        results.sort(key=lambda x: x['loc'], reverse=True)
    elif sort_by == 'complexity':
        results.sort(key=lambda x: x.get('complexity', {}).get('max', 0), reverse=True)
    elif sort_by == 'filename':
        results.sort(key=lambda x: x['file'])
    
    if format == 'json':
        return _generate_json_report(results)
    elif format == 'csv':
        return _generate_csv_report(results)
    else:
        return _generate_table_report(results)


def _generate_table_report(results: List[Dict]) -> str:
    """Generate human-readable table report."""
    output = []
    output.append("=" * 80)
    output.append("CodeX O Analysis Report")
    output.append("=" * 80)
    output.append("")
    
    # Determine if we have complexity data
    has_complexity = any('complexity' in r for r in results)
    
    # Header
    if has_complexity:
        output.append(f"{'File':<50} {'LOC':>8} {'Avg Complexity':>15} {'Max Complexity':>15}")
        output.append("-" * 80)
    else:
        output.append(f"{'File':<60} {'LOC':>10}")
        output.append("-" * 80)
    
    # Rows
    for result in results:
        file = result['file']
        loc = result['loc']
        
        if has_complexity and 'complexity' in result:
            avg_complex = result['complexity']['average']
            max_complex = result['complexity']['max']
            output.append(f"{file:<50} {loc:>8} {avg_complex:>15.2f} {max_complex:>15}")
        else:
            output.append(f"{file:<60} {loc:>10}")
    
    output.append("")
    output.append("-" * 80)
    
    # Summary
    total_files = len(results)
    total_loc = sum(r['loc'] for r in results)
    avg_loc = total_loc / total_files if total_files > 0 else 0
    
    output.append(f"Total files analyzed: {total_files}")
    output.append(f"Total LOC above threshold: {total_loc:,}")
    output.append(f"Average LOC per file: {avg_loc:.0f}")
    
    if has_complexity:
        all_complexities = [r['complexity']['average'] for r in results if 'complexity' in r]
        if all_complexities:
            avg_complexity = sum(all_complexities) / len(all_complexities)
            output.append(f"Average complexity: {avg_complexity:.2f}")
    
    output.append("=" * 80)
    output.append("")
    output.append("💡 Tip: Consider breaking down files with high LOC or complexity into smaller modules.")
    output.append("   This keeps your codebase maintainable and LLM context windows manageable!")
    
    return "\n".join(output)


def _generate_json_report(results: List[Dict]) -> str:
    """Generate JSON report."""
    summary = {
        "total_files": len(results),
        "total_loc": sum(r['loc'] for r in results),
        "average_loc": sum(r['loc'] for r in results) / len(results) if results else 0
    }
    
    report = {
        "summary": summary,
        "files": results
    }
    
    return json.dumps(report, indent=2)


def _generate_csv_report(results: List[Dict]) -> str:
    """Generate CSV report."""
    output = []
    
    # Determine if we have complexity data
    has_complexity = any('complexity' in r for r in results)
    
    # Header
    if has_complexity:
        output.append("File,LOC,Avg Complexity,Max Complexity")
    else:
        output.append("File,LOC")
    
    # Rows
    for result in results:
        file = result['file']
        loc = result['loc']
        
        if has_complexity and 'complexity' in result:
            avg_complex = result['complexity']['average']
            max_complex = result['complexity']['max']
            output.append(f'"{file}",{loc},{avg_complex},{max_complex}')
        else:
            output.append(f'"{file}",{loc}')
    
    return "\n".join(output)
