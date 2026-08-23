"""Command-line entry point for the emergence pipeline."""

from typing import Annotated

import typer

from emergence import __version__

app = typer.Typer(
    name="emergence",
    help="AI-augmented startup triage pipeline: source, analyze, recommend.",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Print the package version and exit.",
            is_eager=True,
            callback=_version_callback,
        ),
    ] = False,
) -> None:
    """emergence — AI-augmented startup triage pipeline."""
