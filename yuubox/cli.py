import sys
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from yuubox import YuuBox, ResourceLimits

console = Console()

@click.group()
@click.version_option("1.0.0")
def cli():
    """YuuBox - Self-Healing Code Execution"""
    pass

@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--language", "-l")
@click.option("--max-iterations", default=5)
@click.option("--no-healing", is_flag=True)
@click.option("--timeout", default=60)
@click.option("--memory", default=256)
def run(file, language, max_iterations, no_healing, timeout, memory):
    """Execute code file with self-healing"""
    
    with open(file) as f:
        code = f.read()
    
    if not language:
        if file.endswith(".py"):
            language = "python"
        elif file.endswith(".js"):
            language = "javascript"
        elif file.endswith(".rs"):
            language = "rust"
        else:
            console.print("[red]Cannot detect language. Use --language[/red]")
            sys.exit(1)
    
    console.print(f"\n[bold blue]Executing {file}[/bold blue]")
    console.print(f"[dim]Language: {language}, Max iterations: {max_iterations}[/dim]\n")
    
    box = YuuBox(max_iterations=max_iterations)
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Running...", total=None)
        result = box.execute(
            code, language,
            limits=ResourceLimits(memory_mb=memory, timeout_seconds=timeout),
            no_healing=no_healing,
        )
        progress.remove_task(task)
    
    if result.success:
        console.print(f"\n[bold green]✓ Success after {result.iterations} iteration(s)[/bold green]\n")
        if result.stdout:
            console.print("[bold]Output:[/bold]")
            console.print(result.stdout)
    else:
        console.print(f"\n[bold red]✗ Failed after {result.iterations} iteration(s)[/bold red]\n")
        console.print("[bold]Error:[/bold]")
        console.print(result.stderr[:500])
        sys.exit(1)

def main():
    cli()

if __name__ == "__main__":
    main()
