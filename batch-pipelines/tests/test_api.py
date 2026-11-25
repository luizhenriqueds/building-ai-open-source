import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.deps import get_db
from api.main import app
from api.params import SearchParams
from api.queries import keep_closest


def test_bbox_is_read_as_four_numbers():
    assert SearchParams(bbox="-47,-24,-46,-23").bbox_values == [-47, -24, -46, -23]
    assert SearchParams().bbox_values is None


@pytest.mark.parametrize("bbox", ["1,2,3", "a,b,c,d"])
def test_malformed_bbox_is_rejected(bbox):
    with pytest.raises(ValidationError):
        SearchParams(bbox=bbox)


def test_type_alias_fills_property_type():
    assert SearchParams.model_validate({"type": "Casa"}).property_type == "Casa"


def test_properties_rejects_bad_bbox_with_422():
    response = TestClient(app).get("/properties", params={"bbox": "1,2"})
    assert response.status_code == 422


def test_properties_accepts_a_comma_separated_bbox(monkeypatch):
    received = {}

    def fake_search(session, params, vector):
        received["bbox"] = params.bbox_values
        return []

    monkeypatch.setattr("api.routes.queries.search_properties", fake_search)
    app.dependency_overrides[get_db] = lambda: None
    try:
        response = TestClient(app).get("/properties", params={"bbox": "-47,-24,-46,-23"})
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert received["bbox"] == [-47, -24, -46, -23]


def test_keep_closest_drops_rows_far_below_the_best_score():
    rows = [{"similarity": 0.50}, {"similarity": 0.47}, {"similarity": 0.40}]
    assert keep_closest(rows, 0.04) == rows[:2]


def test_keep_closest_leaves_unranked_results_alone():
    rows = [{"similarity": None}, {"similarity": None}]
    assert keep_closest(rows, 0.04) == rows
