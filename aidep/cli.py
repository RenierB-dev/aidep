"""
CLI interface for aidep.
Main commands: check, suggest, validate
"""

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
@click.version_option(version="0.1.0")
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
def validate(file):
    """
    ✅ Validate a requirements file for conflicts.
    
    Example: aidep validate requirements.txt
    """
    console.print(f"\n[bold cyan]✅ Validating: {file}[/bold cyan]\n")
    
    file_path = Path(file)
    scanner = DependencyScanner(file_path.parent)
    
    if file_path.name.endswith('.toml'):
        dependencies = scanner.parse_pyproject_toml(file_path)
    else:
        dependencies = scanner.parse_requirements_txt(file_path)
    
    if not dependencies:
        console.print("[yellow]⚠️  No dependencies found in file[/yellow]")
        return
    
    ai_deps = scanner.filter_ai_frameworks(dependencies)
    
    if not ai_deps:
        console.print("[green]✓ No AI framework dependencies to validate[/green]")
        return
    
    console.print(f"[cyan]Found {len(ai_deps)} AI framework dependencies[/cyan]\n")
    
    checker = ConflictChecker(ai_deps)
    conflicts = checker.check_all()
    
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
