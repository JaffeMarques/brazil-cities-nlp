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