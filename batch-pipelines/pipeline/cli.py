import logging

import typer

from pipeline import sample as sample_stage

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """Semantic Lens Lite pipeline."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")


@app.command()
def sample() -> None:
    """Draw the stratified sample of 100 properties and save it to sample/properties.csv."""
    sample_stage.run()
