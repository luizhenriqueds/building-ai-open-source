from pipeline.stages.pois.stage import build_query, category_of, parse_element


def test_build_query_covers_every_selector_and_kind():
    query = build_query("SP")
    assert query.count("node[") == 3
    assert query.count("relation[") == 3
    assert "BR-SP" in query and "leisure" in query and "out center tags" in query


def test_category_of_maps_aliases_and_ignores_other_places():
    assert category_of({"amenity": "college"}) == "university"
    assert category_of({"shop": "mall"}) == "shopping_center"
    assert category_of({"leisure": "park"}) == "park"
    assert category_of({"amenity": "bar"}) is None
    assert category_of({"leisure": "pitch"}) is None


def test_parse_element_uses_center_for_ways():
    element = {
        "type": "way",
        "id": 7,
        "center": {"lat": -23.5, "lon": -46.6},
        "tags": {"shop": "mall", "name": "Centro"},
    }
    poi = parse_element(element)
    assert (poi.osm_id, poi.category, poi.name) == ("way/7", "shopping_center", "Centro")


def test_parse_element_skips_unwanted_elements():
    assert (
        parse_element({"type": "node", "id": 1, "lat": 0, "lon": 0, "tags": {"amenity": "bar"}})
        is None
    )
