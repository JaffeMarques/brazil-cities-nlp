from city_extractor import CityExtractor

extractor = CityExtractor()

# Test some examples
examples = [
    "Mogi das Cruzes - SP",
    "EU QUERO ALUGAR EM SÃO PAULO, GUARULHOS",
    "Procuro imóvel no Rio de Janeiro, Copacabana",
    "Apartamento em Belo Horizonte, Savassi",
    "Casa em São Paulo capital",
    "Quero morar em Porto Alegre, bairro Moinhos",
    "Mogi das Cruzes / São Paulo",
    "Mogi das Cruzes / SP",
    "Mogi - SP",
    "São Paulo - SP",
    "Rio de Janeiro / RJ",
    "Rio de Janeiro - RJ",
    "Rio de Janeiro",
    "RJ",
    "SP",
    "São Paulo",
    "SP",
    "MG",
    "Minas Gerais",
    "BA",
    "Bahia",
    "AC",
    "Acre",
    "AM",
    "Amazonas",
    "AP",
    "Amapá",
    "AL",
    "Alagoas",
]

for example in examples:
    result = extractor.extract(example)
    print(f"Input: {example}")
    print(f"Result: {result}\n")