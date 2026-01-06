"""Command-line interface for Sandevistan."""

import sys
import click

from . import __version__
from .analyzer import analyze_crash_files
from .config import get_api_key, save_api_key, get_config_path, get_config


@click.group()
@click.version_option(version=__version__, prog_name="sandy")
def cli():
    """Sandevistan - AI agent to analyze Apple crash files."""
    pass


@cli.command()
@click.argument("subfolder", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show detailed output")
def analyze(subfolder: str, verbose: bool):
    """Analyze crash files in the specified subfolder."""
    # Get API key from config
    api_key = get_api_key()

    if not api_key:
        click.echo("Error: Google API key not configured.", err=True)
        click.echo("")
        click.echo("Run: sandy config --api-key YOUR_KEY", err=True)
        click.echo("Get your API key at: https://makersuite.google.com/app/apikey", err=True)
        sys.exit(1)

    click.echo(f"Analyzing crashes in: {subfolder}")
    click.echo("-" * 80)

    try:
        result = analyze_crash_files(subfolder, api_key)
        click.echo(f"\nFound {len(result['ips_files'])} IPS file(s)")
        click.echo(result["analysis"])
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.option("--api-key", help="Set the Google API key")
@click.option("--show", is_flag=True, help="Display current configuration")
@click.option("--path", is_flag=True, help="Show config file location")
def config(api_key: str, show: bool, path: bool):
    """Manage Sandevistan configuration."""
    if path:
        click.echo(f"Config file: {get_config_path()}")
        return

    if show:
        cfg = get_config()
        if not cfg:
            click.echo("No configuration found.")
            click.echo(f"Config file would be created at: {get_config_path()}")
        else:
            click.echo("Current configuration:")
            click.echo("")
            # Mask API key for security
            if "api" in cfg and "google_api_key" in cfg["api"]:
                masked_key = cfg["api"]["google_api_key"][:8] + "..." + cfg["api"]["google_api_key"][-4:]
                click.echo(f"  API Key: {masked_key}")
            else:
                click.echo("  API Key: Not set")
        return

    if api_key:
        save_api_key(api_key)
        click.echo(f"API key saved to: {get_config_path()}")
        return

    # No options provided, show help
    click.echo("Error: Please provide an option.", err=True)
    click.echo("")
    click.echo("Examples:")
    click.echo("  sandy config --api-key YOUR_KEY    # Set API key")
    click.echo("  sandy config --show                # Show current config")
    click.echo("  sandy config --path                # Show config file location")
    sys.exit(1)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
