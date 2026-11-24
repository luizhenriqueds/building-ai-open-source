import pytest

from pipeline.config import SAMPLE_SIZE
from pipeline.sample import allocate, draw_sample, group_by_stratum, parse_listing, to_property
from pipeline.schemas import PropertyRecord

HOUSE_DESCRIPTION = (
    "Casa, 111.70 de área total, 100.00 de área privativa, 300.00 de área do terreno,  "
    "3 qto(s), WC, 1 sala(s), cozinha, 2 vaga(s) de garagem."
)
LAND_DESCRIPTION = "Terreno, 0.00 de área total, 600.00 de área do terreno."


def make_cells(property_id: str, description: str = HOUSE_DESCRIPTION, uf: str = "SP") -> list[str]:
    return [
        property_id, uf, "CITY", "HOOD", "RUA A", "136.584,86", "200.000,00", "37.06", "Sim",
        description, "Venda Online", f"https://example.com/{property_id}",
    ]  # fmt: skip


def draw(properties: list[PropertyRecord]) -> list[PropertyRecord]:
    strata = group_by_stratum(properties)
    allocation = allocate({stratum: len(rows) for stratum, rows in strata.items()}, SAMPLE_SIZE)
    return draw_sample(strata, allocation)


def test_to_property_parses_pt_br_values():
    prop = to_property(make_cells("1"))
    assert prop.property_type == "Casa"
    assert prop.sale_value == 136584.86
    assert prop.discount == 37.06
    assert (prop.area_m2, prop.land_area) == (100.0, 300.0)
    assert (prop.bedrooms, prop.parking_spots) == (3, 2)


def test_parse_listing_skips_land():
    rows = [make_cells("1"), make_cells("2", LAND_DESCRIPTION)]
    text = "preamble\nN° do imóvel;UF\n" + "\n".join(";".join(row) for row in rows)
    assert [prop.property_id for prop in parse_listing(text)] == ["1"]


def test_parse_listing_fails_without_header():
    with pytest.raises(ValueError):
        parse_listing("<html>blocked</html>")


def test_allocation_sums_to_sample_size():
    allocation = allocate({("Casa", "SP"): 700, ("Casa", "RJ"): 250, ("Loja", "AC"): 3}, 100)
    assert sum(allocation.values()) == 100


def test_sample_is_deterministic():
    properties = [
        to_property(make_cells(str(index), uf="SP" if index % 3 else "RJ")) for index in range(300)
    ]
    assert draw(properties) == draw(properties)
    assert len(draw(properties)) == SAMPLE_SIZE
