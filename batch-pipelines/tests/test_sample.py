from pipeline.sample import allocate, parse_listing, stratified_sample, to_property

DESCRIPTION = (
    "Casa, 111.70 de área total, 100.00 de área privativa, 300.00 de área do terreno,  "
    "3 qto(s), WC, 1 sala(s), cozinha, 2 vaga(s) de garagem."
)


def cells(pid: str, description: str = DESCRIPTION, uf: str = "SP") -> list[str]:
    return [
        pid, uf, "CITY", "HOOD", "RUA A", "136.584,86", "200.000,00", "37.06", "Sim",
        description, "Venda Online", f"https://example.com/{pid}",
    ]  # fmt: skip


def test_to_property_parses_pt_br_values():
    prop = to_property(cells("1"))
    assert prop["property_type"] == "Casa"
    assert prop["sale_value"] == 136584.86
    assert prop["discount"] == 37.06
    assert (prop["area_m2"], prop["land_area"]) == (100.0, 300.0)
    assert (prop["bedrooms"], prop["parking_spots"]) == (3, 2)


def test_parse_listing_skips_land_and_requires_header():
    land = cells("2", "Terreno, 0.00 de área total, 600.00 de área do terreno.")
    text = "preamble\n" + "N° do imóvel;UF\n" + "\n".join(";".join(c) for c in [cells("1"), land])
    assert [p["property_id"] for p in parse_listing(text)] == ["1"]


def test_parse_listing_fails_without_header():
    try:
        parse_listing("<html>blocked</html>")
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_allocation_sums_to_sample_size():
    allocation = allocate({("Casa", "SP"): 700, ("Casa", "RJ"): 250, ("Loja", "AC"): 3}, 100)
    assert sum(allocation.values()) == 100


def test_sample_is_deterministic():
    props = [to_property(cells(str(i), uf="SP" if i % 3 else "RJ")) for i in range(300)]
    first, _, _ = stratified_sample(props)
    second, _, _ = stratified_sample(props)
    assert first == second
    assert len(first) == 100
