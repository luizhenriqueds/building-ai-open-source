from pipeline.load import read_sample
from pipeline.schemas import PropertyRecord


def test_read_sample_returns_typed_records():
    records = read_sample()
    assert len(records) == 100
    assert isinstance(records[0].appraised_value, float)


def test_empty_cells_become_none():
    record = PropertyRecord(property_id="1", property_type="Casa", uf="SP", bedrooms="")
    assert record.bedrooms is None
