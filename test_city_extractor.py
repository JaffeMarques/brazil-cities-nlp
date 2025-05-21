import pytest
from city_extractor import CityExtractor

@pytest.fixture
def extractor():
    return CityExtractor()

def test_basic_extraction(extractor):
    test_cases = [
        ("Mogi das Cruzes - SP", {"city": "Mogi das Cruzes", "state": "SP"}),
        ("Mogi das Cruzes / São Paulo", {"city": "Mogi das Cruzes", "state": "SP"}),
        ("Mogi das Cruzes / SP", {"city": "Mogi das Cruzes", "state": "SP"}),
        ("Mogi - SP", {"city": "Mogi", "state": "SP"}),
        ("São Paulo - SP", {"city": "São Paulo", "state": "SP"}),
        ("Rio de Janeiro / RJ", {"city": "Rio de Janeiro", "state": "RJ"}),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract(input_text)
        assert result == expected, f"Failed for input: {input_text}"

def test_state_extraction(extractor):
    test_cases = [
        ("SP", "SP"),
        ("São Paulo", "SP"),
        ("sao paulo", "SP"),
        ("RJ", "RJ"),
        ("Rio de Janeiro", "RJ"),
        ("rio de janeiro", "RJ"),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract_state(input_text)
        assert result == expected, f"Failed for input: {input_text}"

def test_city_extraction(extractor):
    test_cases = [
        ("Mogi das Cruzes - SP", "Mogi das Cruzes"),
        ("São Paulo - SP", "São Paulo"),
        ("Rio de Janeiro / RJ", "Rio de Janeiro"),
    ]
    
    for input_text, expected in test_cases:
        state = extractor.extract_state(input_text)
        result = extractor.extract_city(input_text, state)
        assert result == expected, f"Failed for input: {input_text}"

def test_invalid_inputs(extractor):
    test_cases = [
        ("", {"city": None, "state": None}),
        ("Invalid", {"city": "Invalid", "state": None}),
        ("XX", {"city": "XX", "state": None}),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract(input_text)
        assert result == expected, f"Failed for input: {input_text}"

def test_state_only_inputs(extractor):
    test_cases = [
        ("SP", {"city": None, "state": "SP"}),
        ("São Paulo", {"city": None, "state": "SP"}),
        ("sao paulo", {"city": None, "state": "SP"}),
        ("RJ", {"city": None, "state": "RJ"}),
        ("Rio de Janeiro", {"city": None, "state": "RJ"}),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract(input_text)
        assert result == expected, f"Failed for input: {input_text}"

def test_compound_city_names(extractor):
    test_cases = [
        ("Rio de Janeiro / RJ", {"city": "Rio de Janeiro", "state": "RJ"}),
        ("São Paulo - SP", {"city": "São Paulo", "state": "SP"}),
        ("Mogi das Cruzes - SP", {"city": "Mogi das Cruzes", "state": "SP"}),
        ("Porto Alegre / RS", {"city": "Porto Alegre", "state": "RS"}),
        ("Belo Horizonte - MG", {"city": "Belo Horizonte", "state": "MG"}),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract(input_text)
        assert result == expected, f"Failed for input: {input_text}"

def test_complex_sentences(extractor):
    test_cases = [
        ("EU QUERO ALUGAR EM SÃO PAULO, GUARULHOS", {"city": "Guarulhos", "state": "SP"}),
        ("Procuro imóvel no Rio de Janeiro, Copacabana", {"city": "Copacabana", "state": "RJ"}),
        ("Apartamento em Belo Horizonte, Savassi", {"city": "Savassi", "state": "MG"}),
        ("Casa em São Paulo capital", {"city": "São Paulo", "state": "SP"}),
        ("Quero morar em Porto Alegre, bairro Moinhos", {"city": "Porto Alegre", "state": "RS"}),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract(input_text)
        assert result == expected, f"Failed for input: {input_text}"

def test_compound_names(extractor):
    test_cases = [
        ("Rio de Janeiro / RJ", {"city": "Rio de Janeiro", "state": "RJ"}),
        ("São Paulo - SP", {"city": "São Paulo", "state": "SP"}),
        ("Mogi das Cruzes - SP", {"city": "Mogi das Cruzes", "state": "SP"}),
        ("Porto Alegre / RS", {"city": "Porto Alegre", "state": "RS"}),
        ("Belo Horizonte - MG", {"city": "Belo Horizonte", "state": "MG"}),
        ("São José dos Campos - SP", {"city": "São José dos Campos", "state": "SP"}),
        ("Campo Grande - MS", {"city": "Campo Grande", "state": "MS"}),
    ]
    
    for input_text, expected in test_cases:
        result = extractor.extract(input_text)
        assert result == expected, f"Failed for input: {input_text}" 