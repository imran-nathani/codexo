# CodeX O

**Keep your codebase maintainable and LLM-friendly!**

CodeX O is a command-line tool that analyzes your code for file size and complexity (Big O?), helping developers identify files that need refactoring. Perfect for keeping codebases manageable and optimizing context windows for AI development workflows.

## Features

- **Lines of Code (LOC) Analysis**: Quickly identify large files that might benefit from being split up
- **Complexity Metrics**: Calculate cyclomatic complexity for Python files
- **Configurable Thresholds**: Set your own standards for what's "too big" or "too complex"
- **Multiple Output Formats**: Table, JSON, or CSV output
- **Git-aware**: Automatically respects `.gitignore` patterns
- **CI/CD Ready**: Non-zero exit codes when thresholds are exceeded

## Quick Start

Analyze Python files in the current directory:
```bash
codexo
```

Analyze a specific project with custom thresholds:
```bash
codexo /path/to/project --files=py,js --loc=900
```

Include complexity analysis:
```bash
codexo . --complexity
```

Save report to file:
```bash
codexo . --output=report.txt
```

## 📖 Usage

```
codexo [PATH] [OPTIONS]

Arguments:
  PATH    Path to project directory (default: current directory)

Options:
  --files, -f TEXT          File extensions to analyze (comma-separated)
  --loc, -l INTEGER         Minimum lines of code threshold (default: 800)
  --output, -o PATH         Output file path
  --complexity, -c          Calculate complexity metrics
  --format [table|json|csv] Output format (default: table)
  --sort-by [loc|complexity|filename]  Sort results by (default: loc)
  --help                    Show this message and exit
```

## ⚙️ Configuration File

Create a `codexo.config` file in your project root for persistent settings:

```toml
[thresholds]
loc = 800
complexity = 10

[files]
include = ["py", "js", "ts"]
# exclude = ["test_*.py", "*_test.py"]

[output]
format = "table"  # Options: table, json, csv
# file = "codexo-report.txt"
sort_by = "loc"  # Options: loc, complexity, filename

[analysis]
calculate_complexity = true
include_cyclomatic = true
```

CLI arguments override config file settings.

## Example Output

```
================================================================================
CodeX O Analysis Report
================================================================================

File                                               LOC   Avg Complexity   Max Complexity
------------------------------------------------------------------------------------
src/main.py                                        1250            5.20               15
utils/data_processor.py                             982            4.80               12
api/handlers.py                                     856            3.50                8

------------------------------------------------------------------------------------
Total files analyzed: 3
Total LOC above threshold: 3,088
Average LOC per file: 1,029
Average complexity: 4.50
================================================================================

💡 Tip: Consider breaking down files with high LOC or complexity into smaller modules.
   This keeps your codebase maintainable and LLM context windows small!
```

## Why CodeX O?

### For "Vibe Coders"
Working with AI assistants like Claude or GitHub Copilot? Smaller, focused files mean:
- Better context for LLMs to understand your code
- More accurate AI suggestions
- Faster iteration cycles

### For Team Leads
- Enforce code quality standards across your team
- Identify refactoring opportunities during code reviews
- Track technical debt over time

### For CI/CD Pipelines
```yaml
# Example GitHub Action
- name: Check code complexity
  run: codexo . --loc=800 --complexity
```

CodeX O exits with a non-zero status when files exceed thresholds, making it perfect for automated checks.

## Development

### Project Structure
```
codexo/
├── codexo/
│   ├── __init__.py
│   ├── main.py          # CLI entry point
│   ├── analyzer.py      # Core analysis logic
│   ├── config.py        # Configuration handling
│   └── report.py        # Report generation
├── setup.py
├── README.md
└── LICENSE
```

### Running from Source
```bash
git clone https://github.com/yourusername/codexo.git
cd codexo
pip install -e .
codexo
```

## Roadmap

**Phase 1 (Current):**
- ✅ LOC counting for any file type
- ✅ Python cyclomatic complexity
- ✅ Config file support
- ✅ Multiple output formats

**Phase 2 (Planned):**
- Advanced Big O heuristics for Python
- Function-level complexity breakdown
- HTML reports with visualizations
- Better handling of nested loops

**Phase 3 (Future):**
- JavaScript/TypeScript support
- Additional language analyzers
- Integration with popular IDEs
- Trend tracking over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/) for CLI
- Complexity analysis powered by [Radon](https://radon.readthedocs.io/)
- Inspired by the need to keep codebases manageable in the age of AI-assisted development

## 📧 Contact

Your Name - imran.nathani@gmail.com

Project Link: [https://github.com/imran-nathani/codexo](https://github.com/imran-nathani/codexo)



