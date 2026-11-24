import logging

import typer

from pipeline import crawl as crawl_stage
from pipeline import load as load_stage
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


@app.command()
def load() -> None:
    """Upsert sample/properties.csv into the properties table."""
    load_stage.run()


@app.command()
def crawl(
    limit: int | None = typer.Option(None, help="Crawl at most this many properties."),
) -> None:
    """Crawl each property's CAIXA page and photo."""
    crawl_stage.run(limit)
