"""
CLI interface for aidep.
Main commands: check, suggest, validate, doctor, explain, config
"""

import sys
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from pathlib import Path

from .scanner import DependencyScanner
from .checker import ConflictChecker
from .conflicts import COMPATIBILITY_MATRIX, CONFLICTS

console = Console()


@click.group()
@click.version_option(version="0.2.0")
def main():
    """
    🔧 aidep - AI Dependency Doctor

    Detect and fix AI framework dependency conflicts in seconds.
    """
    pass


@main.command()
@click.option('--path', default='.', help='Project path to scan')
@click.option('--verbose', is_flag=True, help='Show detailed output')
def check(path, verbose):
    """
    🔍 Scan your project for AI framework conflicts.
    
    Example: aidep check
    """
    console.print("\n[bold cyan]🔍 Scanning project for AI framework conflicts...[/bold cyan]\n")
    
    scanner = DependencyScanner(path)
    
    # Find and parse requirements
    req_file = scanner.find_requirements_file()
    
    if not req_file:
        console.print("[bold red]❌ No requirements file found![/bold red]")
        console.print("\nLooking for: requirements.txt, pyproject.toml")
        console.print("\nCreate a requirements.txt with your dependencies first.")
        return
    
    console.print(f"[green]✓[/green] Found: {req_file.name}")
    
    # Scan dependencies
    dependencies = scanner.scan_project()
    
    if not dependencies:
        console.print("[yellow]⚠️  No dependencies found in file[/yellow]")
        return
    
    # Filter to AI frameworks
    ai_deps = scanner.filter_ai_frameworks(dependencies)
    
    if not ai_deps:
        console.print("[green]✓ No AI framework dependencies detected[/green]")
        console.print("\nThis tool focuses on: LangChain, LlamaIndex, OpenAI, CrewAI, etc.")
        return
    
    console.print(f"\n[cyan]Found {len(ai_deps)} AI framework dependencies:[/cyan]\n")
    
    # Show dependencies table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Package", style="cyan")
    table.add_column("Version Spec", style="green")
    
    for pkg, ver in ai_deps.items():
        table.add_row(pkg, ver if ver else "*")
    
    console.print(table)
    
    # Check for conflicts
    console.print("\n[bold cyan]🔍 Checking for known conflicts...[/bold cyan]\n")
    
    checker = ConflictChecker(ai_deps)
    conflicts = checker.check_all()
    
    if not conflicts:
        console.print(Panel(
            "[bold green]✅ No known conflicts detected![/bold green]\n\n"
            "Your AI framework dependencies look compatible.\n"
            "Note: This checks against known issues. Always test in a clean environment.",
            title="Results",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]⚠️  Found {len(conflicts)} potential conflict(s)![/bold red]",
            title="Conflicts Detected",
            border_style="red"
        ))
        
        # Show each conflict
        for i, conflict in enumerate(conflicts, 1):
            console.print(f"\n[bold red]Conflict #{i}:[/bold red]")
            console.print(f"[yellow]Severity:[/yellow] {conflict['severity'].upper()}")
            console.print(f"\n{conflict['description']}\n")
            
            # Show affected packages
            console.print("[cyan]Affected packages in your project:[/cyan]")
            for pkg, ver in conflict['affected_packages'].items():
                console.print(f"  • {pkg}: {ver}")
            
            # Show fix
            console.print(f"\n[bold green]💡 Suggested fix:[/bold green]")
            console.print(Panel(conflict['fix'], border_style="green"))

            # Show helpful tip if available
            if 'helpful_tip' in conflict:
                console.print(f"\n[cyan]{conflict['helpful_tip']}[/cyan]")
        
        # Summary
        console.print("\n[bold cyan]📝 Next Steps:[/bold cyan]")
        console.print("1. Review the conflicts above")
        console.print("2. Choose a fix strategy (pinned versions or upgrade all)")
        console.print("3. Update your requirements.txt")
        console.print("4. Test in a clean virtual environment")
        console.print("\n💡 Tip: Use 'aidep suggest <package>' for more options\n")


@main.command()
@click.argument('package')
def suggest(package):
    """
    💡 Get compatible version suggestions for a package.
    
    Example: aidep suggest langchain
    """
    package_lower = package.lower()
    
    console.print(f"\n[bold cyan]💡 Version suggestions for: {package}[/bold cyan]\n")
    
    if package_lower not in COMPATIBILITY_MATRIX:
        console.print(f"[yellow]No specific compatibility data for '{package}'[/yellow]")
        console.print("\nSupported packages:")
        for pkg in COMPATIBILITY_MATRIX.keys():
            console.print(f"  • {pkg}")
        console.print("\n💡 Try: aidep check (to scan your project)")
        return
    
    matrix = COMPATIBILITY_MATRIX[package_lower]
    
    console.print(f"[bold]Compatible version combinations for {package}:[/bold]\n")
    
    for version_range, compatible in matrix.items():
        console.print(f"[green]If using {package} {version_range}:[/green]")
        
        if isinstance(compatible, dict):
            for other_pkg, other_versions in compatible.items():
                if isinstance(other_versions, list):
                    versions_str = ", ".join(other_versions)
                else:
                    versions_str = other_versions
                console.print(f"  • {other_pkg}: {versions_str}")
        elif isinstance(compatible, list):
            for item in compatible:
                console.print(f"  • {item}")
        
        console.print()
    
    console.print("[cyan]💡 Installation examples:[/cyan]\n")
    
    # Provide example install commands
    if package_lower == "langchain":
        console.print("# Stable older version:")
        console.print("pip install langchain==0.0.330 openai==0.28.1\n")
        console.print("# Latest version:")
        console.print("pip install langchain>=0.2.0 langchain-openai>=0.1.0 openai>=1.0.0\n")
    
    elif package_lower == "llama-index":
        console.print("# Stable older version:")
        console.print("pip install llama-index==0.8.69 openai==0.28.1\n")
        console.print("# Latest version:")
        console.print("pip install llama-index>=0.9.0 openai>=1.0.0\n")
    
    console.print("🚀 Faster with uv: Replace 'pip' with 'uv pip' for 10x speed!\n")


@main.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON for CI/CD integration')
def validate(file, output_json):
    """
    ✅ Validate a requirements file for conflicts.

    Example: aidep validate requirements.txt
    Example (CI/CD): aidep validate requirements.txt --json
    """
    file_path = Path(file)
    scanner = DependencyScanner(file_path.parent)

    if file_path.name.endswith('.toml'):
        dependencies = scanner.parse_pyproject_toml(file_path)
    else:
        dependencies = scanner.parse_requirements_txt(file_path)

    if not dependencies:
        if output_json:
            import json
            print(json.dumps({"valid": True, "conflicts": [], "message": "No dependencies found"}))
        else:
            console.print(f"\n[bold cyan]✅ Validating: {file}[/bold cyan]\n")
            console.print("[yellow]⚠️  No dependencies found in file[/yellow]")
        return

    ai_deps = scanner.filter_ai_frameworks(dependencies)

    if not ai_deps:
        if output_json:
            import json
            print(json.dumps({"valid": True, "conflicts": [], "message": "No AI frameworks"}))
        else:
            console.print(f"\n[bold cyan]✅ Validating: {file}[/bold cyan]\n")
            console.print("[green]✓ No AI framework dependencies to validate[/green]")
        return

    checker = ConflictChecker(ai_deps)
    conflicts = checker.check_all()

    if output_json:
        import json
        result = {
            "valid": len(conflicts) == 0,
            "file": str(file),
            "conflicts_count": len(conflicts),
            "conflicts": [
                {
                    "id": c['id'],
                    "severity": c['severity'],
                    "description": c['description'],
                    "affected_packages": c['affected_packages'],
                    "fix": c['fix'],
                    "helpful_tip": c.get('helpful_tip', '')
                }
                for c in conflicts
            ]
        }
        print(json.dumps(result, indent=2))
    else:
        console.print(f"\n[bold cyan]✅ Validating: {file}[/bold cyan]\n")
        console.print(f"[cyan]Found {len(ai_deps)} AI framework dependencies[/cyan]\n")

        if not conflicts:
            console.print(Panel(
                "[bold green]✅ Validation passed![/bold green]\n\n"
                "No known conflicts detected in this requirements file.",
                title="✅ Valid",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[bold red]❌ Validation failed![/bold red]\n\n"
                f"Found {len(conflicts)} potential conflict(s).",
                title="❌ Invalid",
                border_style="red"
            ))

            for conflict in conflicts:
                console.print(f"\n[red]• {conflict['description']}[/red]")
                if 'helpful_tip' in conflict:
                    console.print(f"  [cyan]{conflict['helpful_tip']}[/cyan]")

        console.print()

    # Exit with error code for CI/CD
    if conflicts:
        sys.exit(1)


@main.command()
def doctor():
    """
    🏥 Run health check on your AI development environment.

    Checks Python version, installed packages, and common issues.
    """
    import platform
    import importlib.metadata

    console.print("\n[bold cyan]🏥 AI Development Environment Check[/bold cyan]\n")

    # Python version check
    py_version = sys.version_info
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Check", style="cyan", width=30)
    table.add_column("Status", style="green", width=15)
    table.add_column("Details", style="white", width=40)

    # Python version
    if py_version >= (3, 8):
        table.add_row("Python Version", "✅ OK", f"{py_version.major}.{py_version.minor}.{py_version.micro}")
    else:
        table.add_row("Python Version", "❌ OLD", f"{py_version.major}.{py_version.minor}.{py_version.micro} (need 3.8+)")

    # Platform
    table.add_row("Platform", "ℹ️  INFO", platform.system())

    # Check for common packages
    packages_to_check = ['torch', 'transformers', 'langchain', 'llama-index', 'openai', 'pydantic']

    for pkg in packages_to_check:
        try:
            version = importlib.metadata.version(pkg)
            table.add_row(pkg, "✅ Installed", version)
        except Exception:
            table.add_row(pkg, "❌ Missing", "Not installed")

    console.print(table)
    console.print("\n[cyan]💡 Tip: Run 'aidep check' to scan for conflicts[/cyan]\n")


@main.command()
@click.argument('conflict_id')
def explain(conflict_id):
    """
    📖 Get detailed explanation of a specific conflict.

    Example: aidep explain langchain-openai-separate-package
    """
    console.print(f"\n[bold cyan]📖 Conflict Explanation: {conflict_id}[/bold cyan]\n")

    # Find conflict
    conflict = None
    for c in CONFLICTS:
        if c['id'] == conflict_id:
            conflict = c
            break

    if not conflict:
        console.print(f"[red]❌ Conflict '{conflict_id}' not found[/red]")
        console.print("\n[cyan]💡 Run 'aidep list-conflicts' to see all conflicts[/cyan]\n")
        return

    # Display detailed info
    console.print(Panel(
        f"[bold]{conflict['description']}[/bold]",
        title=f"🔍 {conflict['id']}",
        border_style="cyan"
    ))

    console.print(f"\n[yellow]Severity:[/yellow] {conflict['severity'].upper()}")
    console.print(f"\n[yellow]Affected Packages:[/yellow]")
    for pkg in conflict['packages']:
        console.print(f"  • {pkg}")

    if 'working_versions' in conflict:
        console.print(f"\n[green]Working Versions:[/green]")
        for pkg, ver in conflict['working_versions'].items():
            console.print(f"  • {pkg}: {ver}")

    if 'alternative' in conflict:
        console.print(f"\n[green]Alternative (Modern) Versions:[/green]")
        for pkg, ver in conflict['alternative'].items():
            console.print(f"  • {pkg}: {ver}")

    console.print(f"\n[bold green]💡 How to Fix:[/bold green]")
    console.print(Panel(conflict['fix'], border_style="green"))
    console.print()


@main.group()
def config():
    """⚙️  Manage aidep configuration."""
    pass


@config.command(name='set')
@click.argument('key')
@click.argument('value')
def config_set(key, value):
    """Set a configuration value."""
    from .config import Config
    cfg = Config()

    # Parse boolean strings
    if value.lower() in ('true', 'false'):
        value = value.lower() == 'true'

    cfg.set(key, value)
    console.print(f"[green]✓ Set {key} = {value}[/green]")


@config.command(name='show')
def config_show():
    """Show current configuration."""
    from .config import Config
    cfg = Config()

    console.print("\n[bold cyan]⚙️  Current Configuration[/bold cyan]\n")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    for key, value in cfg.config.items():
        table.add_row(key, str(value))

    console.print(table)
    console.print()


@main.command()
def list_conflicts():
    """
    📋 List all known AI framework conflicts.
    """
    console.print("\n[bold cyan]📋 Known AI Framework Conflicts Database[/bold cyan]\n")
    console.print(f"Total conflicts tracked: {len(CONFLICTS)}\n")

    for i, conflict in enumerate(CONFLICTS, 1):
        packages = ", ".join(conflict['packages'])
        console.print(f"[bold]{i}. {packages}[/bold]")
        console.print(f"   [yellow]Severity:[/yellow] {conflict['severity']}")
        console.print(f"   {conflict['description']}\n")

    console.print("[cyan]💡 Run 'aidep check' to scan your project against these conflicts[/cyan]\n")


if __name__ == "__main__":
    main()
