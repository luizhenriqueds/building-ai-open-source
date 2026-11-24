from datetime import date

from pipeline.crawl import is_blocked, parse_page

MARKDOWN = """Quartos: **2**
Situação: **Ocupado**
Área total = **98,07m2**
Área privativa = **59,00m2**
Área do terreno = **1.627,18m2**
**Endereço:**
RUA A, N. 1, CENTRO - CEP: 01000-000, SAO PAULO
Data do 1º Leilão - 20/01/2027 - 10h00
Data do 2º Leilão - 26/01/2027 - 10h00
"""
HTML = '<img id="preview" src="/fotos/F123.jpg"><a href="x">"/fotos/F999.jpg"</a>'


def test_parse_page_extracts_all_fields():
    details = parse_page(HTML, MARKDOWN)
    assert details.bedrooms == 2
    assert details.occupancy_status == "Ocupado"
    assert (details.area_m2, details.land_area) == (59.0, 1627.18)
    assert details.raw_address == "RUA A, N. 1, CENTRO - CEP: 01000-000, SAO PAULO"
    assert details.auction_date == date(2027, 1, 20)
    assert details.image_url == "https://venda-imoveis.caixa.gov.br/fotos/F123.jpg"


def test_parse_page_handles_missing_fields():
    details = parse_page("<html></html>", "Área total = **0,00m2**")
    assert details.area_m2 is None
    assert details.image_url is None
    assert details.auction_date is None


def test_is_blocked_detects_radware_page():
    assert is_blocked("<title>Radware Bot Manager CAPTCHA</title>")
    assert not is_blocked("Número do imóvel: 123")
