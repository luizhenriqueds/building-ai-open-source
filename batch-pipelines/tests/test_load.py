from pipeline.config import SAMPLE_COLUMNS
from pipeline.load import build_upsert_sql, read_sample


def test_read_sample_returns_all_columns_and_nulls_for_empty_cells():
    properties = read_sample()
    assert len(properties) == 100
    assert set(properties[0]) == set(SAMPLE_COLUMNS)
    assert any(prop["parking_spots"] is None for prop in properties)


def test_upsert_sql_updates_every_column_but_the_key():
    sql = build_upsert_sql()
    assert "on conflict (property_id) do update set" in sql
    assert "property_id = excluded.property_id" not in sql
    assert "link = excluded.link" in sql
