from pipeline.common.models import Property
from pipeline.common.schemas import GeocodeResult
from pipeline.stages.geocode.stage import (
    apply_result,
    build_ladder,
    distance_km,
    geocode_property,
    parse_address,
)

CITY_POINT = (-23.55, -46.63)


class FakeGeocoder:
    def __init__(self, hits: dict[str, tuple[float, float]]):
        self.hits = hits

    def search(self, query: str):
        return self.hits.get(query)


def make_property(raw_address: str = "RUA A,N. 10 APTO. 2, CENTRO - CEP: 01000-000") -> Property:
    return Property(
        property_id="1", city="SAO PAULO", uf="SP", neighborhood="CENTRO", raw_address=raw_address
    )


def test_parse_address_drops_sn_and_plot_streets():
    assert parse_address("RUA A,N. 673 APTO. 1").number == "673"
    assert parse_address("RUA XI,N. SN LT 02").number is None
    assert parse_address("QUADRA 33,N. SN APTO. 201").street is None


def test_build_ladder_goes_from_street_to_city():
    precisions = [precision for precision, _ in build_ladder(make_property())]
    assert precisions == ["street", "neighborhood", "city"]


def test_distance_between_sao_paulo_and_rio_is_about_360_km():
    assert 340 < distance_km(CITY_POINT, (-22.91, -43.17)) < 380


def test_geocode_rejects_street_hit_in_another_city():
    prop = make_property()
    hits = {
        "SAO PAULO, SP, Brasil": CITY_POINT,
        "RUA A 10, CENTRO, SAO PAULO, SP, Brasil": (-22.91, -43.17),
        "CENTRO, SAO PAULO, SP, Brasil": (-23.54, -46.63),
    }
    result = geocode_property(FakeGeocoder(hits), prop)
    assert result.precision == "neighborhood"
    assert result.confidence == 0.5


def test_apply_result_never_lowers_confidence():
    prop = make_property()
    prop.geocode_confidence = 0.9
    assert not apply_result(prop, GeocodeResult(lat=1, lon=1, precision="city", confidence=0.3))
    assert prop.geocode_confidence == 0.9
