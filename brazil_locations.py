"""
Dados de cidades e estados brasileiros para validação.
Fonte: IBGE (https://www.ibge.gov.br/explica/codigos-dos-municipios.php)
"""

# Estados brasileiros (sigla -> nome)
STATES = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

# Cidades principais por estado (estado -> lista de cidades)
MAJOR_CITIES = {
    'SP': [
        'São Paulo', 'Guarulhos', 'Campinas', 'São Bernardo do Campo', 'Santo André',
        'Osasco', 'São José dos Campos', 'Ribeirão Preto', 'Sorocaba', 'Santos',
        'São José do Rio Preto', 'Mogi das Cruzes', 'São Vicente', 'Jundiaí',
        'Limeira', 'Carapicuíba', 'Piracicaba', 'Bauru', 'Itaquaquecetuba',
        'São Caetano do Sul', 'Franca', 'Praia Grande', 'Guarujá', 'Taubaté'
    ],
    'RJ': [
        'Rio de Janeiro', 'São Gonçalo', 'Duque de Caxias', 'Nova Iguaçu', 'Niterói',
        'Belford Roxo', 'São João de Meriti', 'Petrópolis', 'Volta Redonda', 'Macaé',
        'Magé', 'Itaboraí', 'Nova Friburgo', 'Barra Mansa', 'Angra dos Reis',
        'Cabo Frio', 'Teresópolis', 'Mesquita', 'Maricá', 'Nilópolis'
    ],
    'MG': [
        'Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora', 'Betim',
        'Montes Claros', 'Ribeirão das Neves', 'Uberaba', 'Governador Valadares',
        'Ipatinga', 'Sete Lagoas', 'Divinópolis', 'Santa Luzia', 'Ibirité',
        'Poços de Caldas', 'Pouso Alegre', 'Patos de Minas', 'Pampulha', 'Barbacena'
    ],
    'RS': [
        'Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas', 'Santa Maria',
        'Gravataí', 'Viamão', 'Novo Hamburgo', 'São Leopoldo', 'Rio Grande',
        'Alvorada', 'Passo Fundo', 'Sapucaia do Sul', 'Uruguaiana', 'Santa Cruz do Sul',
        'Cachoeirinha', 'Guaíba', 'Bento Gonçalves', 'Bagé', 'Erechim'
    ],
    'PR': [
        'Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa', 'Cascavel',
        'São José dos Pinhais', 'Foz do Iguaçu', 'Colombo', 'Guarapuava', 'Paranaguá',
        'Araucária', 'Toledo', 'Apucarana', 'Pinhais', 'Campo Largo',
        'Arapongas', 'Almirante Tamandaré', 'Umuarama', 'Cambé', 'Piraquara'
    ],
    'BA': [
        'Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Camaçari', 'Itabuna',
        'Juazeiro', 'Lauro de Freitas', 'Ilhéus', 'Jequié', 'Teixeira de Freitas',
        'Barreiras', 'Alagoinhas', 'Porto Seguro', 'Simões Filho', 'Paulo Afonso',
        'Eunápolis', 'Santo Antônio de Jesus', 'Candeias', 'Itapetinga', 'Lucas do Rio Verde'
    ],
    'SC': [
        'Florianópolis', 'Joinville', 'Blumenau', 'São José', 'Criciúma',
        'Itajaí', 'Lages', 'Jaraguá do Sul', 'Palhoça', 'Balneário Camboriú',
        'Brusque', 'Tubarão', 'São Bento do Sul', 'Biguaçu', 'Itapema',
        'Camboriú', 'Chapecó', 'Navegantes', 'São Francisco do Sul', 'Imbituba'
    ],
    'PE': [
        'Recife', 'Jaboatão dos Guararapes', 'Olinda', 'Caruaru', 'Petrolina',
        'Paulista', 'Cabo de Santo Agostinho', 'Camaragibe', 'Garanhuns', 'Vitória de Santo Antão',
        'Santa Cruz do Capibaribe', 'São Lourenço da Mata', 'Igarassu', 'Abreu e Lima', 'Carpina',
        'Gravatá', 'Santa Maria da Boa Vista', 'Ipojuca', 'Goiana', 'Araripina'
    ],
    'CE': [
        'Fortaleza', 'Caucaia', 'Juazeiro do Norte', 'Maracanaú', 'Sobral',
        'Crato', 'Itapipoca', 'Maranguape', 'Iguatu', 'Quixadá',
        'Pacatuba', 'Quixeramobim', 'Aracati', 'Crateús', 'Acaraú',
        'Russas', 'Tianguá', 'Cascavel', 'Horizonte', 'Icó'
    ],
    'PA': [
        'Belém', 'Ananindeua', 'Santarém', 'Castanhal', 'Marituba',
        'Marabá', 'Bragança', 'Parauapebas', 'Abaetetuba', 'Cametá',
        'Altamira', 'Tucuruí', 'Paragominas', 'Itaituba', 'Tailândia',
        'Barcarena', 'Marapanim', 'Breves', 'Capanema', 'Moju'
    ]
}

# Criar dicionário reverso (nome da cidade -> estado)
CITY_TO_STATE = {}
for state, cities in MAJOR_CITIES.items():
    for city in cities:
        CITY_TO_STATE[city.lower()] = state

# Adicionar estados como cidades também (para casos como "São Paulo capital")
for state, state_name in STATES.items():
    CITY_TO_STATE[state_name.lower()] = state

# Palavras que podem indicar localização
LOCATION_INDICATORS = {
    'em', 'no', 'na', 'nos', 'nas',  # Preposições
    'de', 'do', 'da', 'dos', 'das',  # Artigos
    'capital', 'cidade', 'município', 'municipio',  # Indicadores de cidade
    'estado', 'uf'  # Indicadores de estado
}

# Bairros importantes por cidade (cidade -> lista de bairros)
NEIGHBORHOODS = {
    'rio de janeiro': [
        'copacabana', 'ipanema', 'leblon', 'botafogo', 'flamengo',
        'laranjeiras', 'catete', 'glória', 'centro', 'santa teresa',
        'lapa', 'tijuca', 'jardim botânico', 'gávea', 'barra da tijuca',
        'recreio dos bandeirantes', 'jacarepaguá', 'campo grande', 'madureira',
        'méier', 'vila isabel', 'maracanã', 'são cristóvão', 'benfica'
    ],
    'são paulo': [
        'vila mariana', 'mooca', 'pinheiros', 'vila madalena', 'jardins',
        'itaim bibi', 'morumbi', 'campo belo', 'santo amaro', 'brooklin',
        'vila leopoldina', 'lapa', 'perdizes', 'jardim paulista', 'jardim europa',
        'vila olimpia', 'berrini', 'chácara klabin', 'santa cecília', 'bela vista',
        'centro', 'consolação', 'vila buarque', 'liberdade', 'bom retiro'
    ],
    'belo horizonte': [
        'savassi', 'lourdes', 'funcionários', 'centro', 'santa efigênia',
        'santo antônio', 'cidade nova', 'santa tereza', 'floresta', 'carlos prates',
        'prado', 'gutierrez', 'serra', 'anchieta', 'cidade jardim',
        'buritis', 'nova lima', 'estrela dalva', 'belvedere', 'mangabeiras'
    ],
    'porto alegre': [
        'moinhos de vento', 'bela vista', 'petrópolis', 'auxiliadora', 'bom fim',
        'rio branco', 'centro histórico', 'cidade baixa', 'menino deus', 'três figueiras',
        'jardim botânico', 'jardim carvalho', 'jardim do salso', 'jardim lindóia',
        'jardim sabará', 'jardim são pedro', 'jardim são salvador', 'jardim são sebastião',
        'jardim são valentim', 'jardim são vicente'
    ]
}

# Criar dicionário reverso (nome do bairro -> cidade)
NEIGHBORHOOD_TO_CITY = {}
for city, neighborhoods in NEIGHBORHOODS.items():
    for neighborhood in neighborhoods:
        NEIGHBORHOOD_TO_CITY[neighborhood.lower()] = city

# Atualizar CITY_TO_STATE para incluir bairros
for neighborhood, city in NEIGHBORHOOD_TO_CITY.items():
    if city in CITY_TO_STATE:
        CITY_TO_STATE[neighborhood] = CITY_TO_STATE[city]

# Atualizar IGNORE_WORDS para remover 'bairro' já que agora tratamos bairros
IGNORE_WORDS = {
    'quero', 'procuro', 'busco', 'alugar', 'comprar', 'vender',  # Verbos de intenção
    'imóvel', 'imovel', 'casa', 'apartamento', 'terreno',  # Tipos de imóvel
    'zona', 'região', 'regiao', 'área', 'area'  # Indicadores de área
} 