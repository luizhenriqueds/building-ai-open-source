from pipeline.models import Property
from pipeline.visual import VisualAge, apply_assessment, compute_score


def make_assessment(**overrides) -> VisualAge:
    fields = {
        "is_property_photo": True,
        "facade": 8,
        "condition": 6,
        "standard": 5,
        "surroundings": 4,
        "age_class": "old",
        "age_years_low": 30,
        "age_years_high": 50,
        "note": "Plain facade with worn paint.",
    }
    return VisualAge(**{**fields, **overrides})


def test_compute_score_is_weighted_average_on_a_hundred_scale():
    assert compute_score(make_assessment()) == 64.0


def test_compute_score_is_none_for_non_property_photos():
    assert compute_score(make_assessment(is_property_photo=False)) is None


def test_apply_assessment_sets_visual_columns():
    item = Property(property_id="1")
    apply_assessment(item, make_assessment())
    assert (item.visual_score, item.visual_age) == (64.0, "old")
    assert item.visual_details["facade"] == 8
