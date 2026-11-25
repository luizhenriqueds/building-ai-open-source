from pipeline.embed import build_text, label_for, percentile_rank
from pipeline.embed_config import SEGMENT_CUTS, SEGMENT_LABELS, SIZE_CUTS, SIZE_LABELS
from pipeline.models import Property
from prompts.embedding import build_query_prompt


def test_percentile_rank_counts_strictly_lower_peers():
    assert percentile_rank(10, [10, 20, 30, 40]) == 0
    assert percentile_rank(40, [10, 20, 30, 40]) == 75


def test_label_for_uses_band_cuts():
    assert label_for(10, SIZE_CUTS, SIZE_LABELS) == "pequeno"
    assert label_for(50, SIZE_CUTS, SIZE_LABELS) == "médio"
    assert label_for(90, SEGMENT_CUTS, SEGMENT_LABELS) == "alto"


def test_build_text_skips_missing_parts():
    item = Property(
        property_id="1",
        property_type="Casa",
        uf="SP",
        city="Campinas",
        neighborhood="Centro",
        area_m2=80.4,
        bedrooms=3,
        occupancy_status="Ocupado",
    )
    assert build_text(item, "médio", "popular") == (
        "Casa de porte médio, padrão popular. 80 m² de área construída. 3 quartos. "
        "Imóvel ocupado. Localizada no bairro Centro em Campinas-SP."
    )


def test_build_text_without_neighborhood_or_labels():
    item = Property(property_id="1", property_type="Apartamento", uf="RJ", city="Niterói")
    assert build_text(item, None, None) == "Apartamento. Localizada em Niterói-RJ."


def test_query_prompt_has_instruction_and_query():
    prompt = build_query_prompt("house with 3 bedrooms")
    assert prompt.startswith("Instruct: ") and prompt.endswith("Query: house with 3 bedrooms")
