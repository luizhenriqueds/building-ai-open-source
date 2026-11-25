import logging

import typer

from pipeline import crawl as crawl_stage
from pipeline import embed as embed_stage
from pipeline import geocode as geocode_stage
from pipeline import load as load_stage
from pipeline import pois as pois_stage
from pipeline import sample as sample_stage
from pipeline import visual as visual_stage

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


@app.command()
def geocode() -> None:
    """Geocode properties with Nominatim (street, then neighborhood, then city)."""
    geocode_stage.run()


@app.command()
def pois() -> None:
    """Fetch nearby places from Overpass and link them to each property."""
    pois_stage.run()


@app.command()
def embed() -> None:
    """Embed each property's description with Ollama."""
    embed_stage.run()


@app.command()
def visual(
    limit: int | None = typer.Option(None, help="Score at most this many properties."),
) -> None:
    """Score each property photo with a local vision model."""
    visual_stage.run(limit)
