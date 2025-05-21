import re
import spacy
from unidecode import unidecode
from typing import Dict, Optional, Tuple, List, Set
from difflib import get_close_matches
from brazil_locations import (
    STATES, MAJOR_CITIES, CITY_TO_STATE, LOCATION_INDICATORS, IGNORE_WORDS,
    NEIGHBORHOODS, NEIGHBORHOOD_TO_CITY
)

class CityExtractor:
    def __init__(self):
        """Initialize the CityExtractor with spaCy model and state mappings."""
        self.nlp = spacy.load("pt_core_news_sm")
        self.state_mapping = STATES
        self.reverse_state_mapping = {v.lower(): k for k, v in STATES.items()}
        self.city_to_state = CITY_TO_STATE
        self.location_indicators = LOCATION_INDICATORS
        self.ignore_words = IGNORE_WORDS
        self.neighborhoods = NEIGHBORHOODS
        self.neighborhood_to_city = NEIGHBORHOOD_TO_CITY
        
        # Cidades que são capitais de estado
        self.state_capitals = {
            'rio de janeiro': 'RJ',
            'são paulo': 'SP',
            'sao paulo': 'SP',
            'belo horizonte': 'MG',
            'salvador': 'BA',
            'fortaleza': 'CE',
            'brasília': 'DF',
            'brasilia': 'DF',
            'curitiba': 'PR',
            'manaus': 'AM',
            'recife': 'PE',
            'porto alegre': 'RS',
            'belém': 'PA',
            'belem': 'PA',
            'goiânia': 'GO',
            'goiania': 'GO',
            'guarulhos': 'SP',  # Maior cidade do estado de SP
            'campinas': 'SP',   # Segunda maior cidade do estado de SP
        }
        
        # Cria um índice de cidades por estado para busca rápida
        self.cities_by_state = {}
        for city, state in self.city_to_state.items():
            if state not in self.cities_by_state:
                self.cities_by_state[state] = []
            self.cities_by_state[state].append(city)
        
        # Cria um índice de cidades por prefixo para busca rápida
        self.cities_by_prefix = {}
        for city in self.city_to_state.keys():
            # Adiciona a cidade completa
            self.cities_by_prefix[city] = city
            # Adiciona o primeiro nome da cidade
            first_word = city.split()[0]
            if first_word not in self.cities_by_prefix:
                self.cities_by_prefix[first_word] = city
            # Adiciona variações comuns
            if first_word.startswith('sao '):
                self.cities_by_prefix['s.'] = city
                self.cities_by_prefix['s.'] = city
            elif first_word.startswith('santa '):
                self.cities_by_prefix['sta.'] = city
                self.cities_by_prefix['sta'] = city
        
        # Palavras que indicam que o próximo termo pode ser um bairro
        self.neighborhood_indicators = {
            'bairro', 'zona', 'região', 'regiao', 'área', 'area',
            'vila', 'jardim', 'parque', 'centro', 'largo', 'praça',
            'praça', 'avenida', 'av', 'rua', 'travessa', 'alameda'
        }
        
        # Sufixos comuns em nomes de bairros
        self.neighborhood_suffixes = {
            'vila', 'jardim', 'parque', 'centro', 'largo', 'praça',
            'praça', 'avenida', 'av', 'rua', 'travessa', 'alameda',
            'bosque', 'chácara', 'chacara', 'condomínio', 'condominio',
            'conjunto', 'residencial', 'residencial', 'setor', 'quadra'
        }

    def normalize_text(self, text: str) -> str:
        """Normalize text by removing accents and converting to lowercase."""
        return unidecode(text.lower().strip())

    def extract_state(self, text: str) -> Optional[str]:
        """Extract state information from text."""
        # Normalize the text
        normalized_text = self.normalize_text(text)
        
        # Try to find state by sigla (2 letters)
        state_sigla_match = re.search(r'\b([A-Z]{2})\b', text.upper())
        if state_sigla_match:
            state_sigla = state_sigla_match.group(1)
            if state_sigla in self.state_mapping:
                return state_sigla

        # Try to find state by full name
        for state_name, sigla in self.reverse_state_mapping.items():
            if state_name in normalized_text:
                return sigla

        # Try to find state from city name or neighborhood
        for location, state in self.city_to_state.items():
            if location in normalized_text:
                return state

        # Try to find state from state capitals
        for city, state in self.state_capitals.items():
            if city in normalized_text:
                return state

        return None

    def is_likely_neighborhood(self, text: str, context: List[str]) -> bool:
        """
        Determina se um texto provavelmente é um bairro baseado em várias heurísticas.
        
        Args:
            text (str): O texto a ser analisado
            context (List[str]): Palavras ao redor do texto que podem dar contexto
            
        Returns:
            bool: True se o texto provavelmente é um bairro
        """
        text = self.normalize_text(text)
        words = text.split()
        
        # Se já está na nossa lista de bairros conhecidos
        if text in self.neighborhood_to_city:
            return True
            
        # Se começa com um indicador de bairro
        if any(text.startswith(indicator) for indicator in self.neighborhood_indicators):
            return True
            
        # Se contém um sufixo comum de bairro
        if any(suffix in text for suffix in self.neighborhood_suffixes):
            return True
            
        # Se tem palavras de contexto que indicam bairro
        if any(indicator in context for indicator in self.neighborhood_indicators):
            return True
            
        # Se é um substantivo próprio (PROPN) e não é uma cidade/estado conhecida
        if (text not in self.city_to_state and 
            text not in self.reverse_state_mapping and
            text not in self.ignore_words):
            # Verifica se tem características de nome de bairro
            # 1. Geralmente tem 2-4 palavras
            # 2. Geralmente contém palavras como "vila", "jardim", etc.
            # 3. Geralmente não é muito longo
            if 1 <= len(words) <= 4 and len(text) <= 50:
                return True
                
        return False

    def find_location_entities(self, doc) -> List[Tuple[str, float, str]]:
        """
        Find potential location entities in the text using spaCy's NER and our city database.
        Returns a list of tuples (entity, confidence_score, entity_type).
        entity_type can be: 'city', 'neighborhood', 'state', or 'unknown'
        """
        locations = []
        current_entity = []
        words = []
        context = []
        
        # Primeiro, vamos coletar todas as palavras relevantes e seu contexto
        for token in doc:
            word = token.text.lower()
            if word in self.ignore_words:
                continue
            words.append((token.text, token.pos_, token.ent_type_))
            context.append(word)
            if len(context) > 7:  # 3 antes + atual + 3 depois
                context.pop(0)
        
        # Agora vamos processar as palavras para encontrar entidades
        i = 0
        while i < len(words):
            word, pos, ent_type = words[i]
            
            if word in self.location_indicators:
                if current_entity:
                    current_entity.append(word)
                i += 1
                continue
            
            if pos == "PROPN" or ent_type == "LOC":
                current_entity.append(word)
                i += 1
                
                while i < len(words):
                    next_word, next_pos, next_ent = words[i]
                    if (next_word in self.location_indicators or 
                        next_pos == "PROPN" or 
                        next_ent == "LOC"):
                        current_entity.append(next_word)
                        i += 1
                    else:
                        break
                
                if current_entity:
                    entity = " ".join(current_entity)
                    normalized_entity = self.normalize_text(entity)
                    
                    # Determina o tipo e confiança da entidade
                    entity_type = 'unknown'
                    confidence = 0.0
                    
                    if normalized_entity in self.city_to_state:
                        entity_type = 'city'
                        confidence = 1.0
                    elif normalized_entity in self.reverse_state_mapping:
                        entity_type = 'state'
                        confidence = 1.0
                    elif normalized_entity in self.neighborhood_to_city:
                        entity_type = 'neighborhood'
                        confidence = 0.9
                    elif self.is_likely_neighborhood(entity, context):
                        entity_type = 'neighborhood'
                        confidence = 0.7
                    elif ent_type == "LOC":
                        confidence = 0.5
                    elif pos == "PROPN":
                        confidence = 0.3
                    
                    if confidence > 0:
                        locations.append((entity, confidence, entity_type))
                    current_entity = []
            else:
                i += 1
        
        return locations

    def find_matching_city(self, partial_name: str, state: Optional[str] = None) -> Optional[str]:
        """
        Tenta encontrar uma cidade que corresponda ao nome parcial fornecido.
        
        Args:
            partial_name (str): Nome parcial ou abreviado da cidade
            state (Optional[str]): Estado para ajudar na busca
            
        Returns:
            Optional[str]: Nome completo da cidade se encontrado, None caso contrário
        """
        partial_name = self.normalize_text(partial_name)
        
        # Se temos o estado, procura apenas nas cidades daquele estado
        if state and state in self.cities_by_state:
            cities_to_search = self.cities_by_state[state]
        else:
            cities_to_search = list(self.city_to_state.keys())
        
        # 1. Procura por correspondência exata
        if partial_name in self.cities_by_prefix:
            return self.cities_by_prefix[partial_name]
        
        # 2. Procura por prefixo
        for city in cities_to_search:
            city_lower = self.normalize_text(city)
            if city_lower.startswith(partial_name):
                return city
        
        # 3. Procura por similaridade
        matches = get_close_matches(partial_name, cities_to_search, n=1, cutoff=0.6)
        if matches:
            return matches[0]
        
        # 4. Procura por primeiro nome
        first_word = partial_name.split()[0]
        if first_word in self.cities_by_prefix:
            return self.cities_by_prefix[first_word]
        
        return None

    def extract_city(self, text: str, state: Optional[str] = None) -> Optional[str]:
        """Extract city name from text."""
        # Normalize the text first
        normalized_text = self.normalize_text(text)
        
        # Check if the text itself is a state capital or major city
        if normalized_text in self.state_capitals:
            return text.strip()
            
        # If the text is only a state (either abbreviation or full name), return None
        if state and (text.upper() == state or normalized_text == self.state_mapping[state].lower()):
            return None
            
        # Remove state information if present
        if state:
            text = re.sub(rf'\s*[-\/]\s*{state}\b', '', text, flags=re.IGNORECASE)
            text = re.sub(rf'\s*[-\/]\s*{self.state_mapping[state]}\b', '', text, flags=re.IGNORECASE)
        
        # Remove common separators
        text = re.sub(r'\s*[-\/]\s*', ' ', text)
        
        if not text.strip():
            return None
            
        # Process with spaCy
        doc = self.nlp(text)
        
        # Find all potential location entities with confidence scores and types
        locations = self.find_location_entities(doc)
        
        if locations:
            # Ordena por confiança (maior primeiro)
            locations.sort(key=lambda x: x[1], reverse=True)
            
            # Primeiro procura por cidades
            cities = [(loc, conf) for loc, conf, type_ in locations if type_ == 'city']
            if cities:
                for city, confidence in cities:
                    city_lower = self.normalize_text(city)
                    # Se é uma capital de estado ou cidade importante
                    if city_lower in self.state_capitals:
                        return city.strip()
                    # Se é uma cidade normal
                    elif state is None or self.city_to_state[city_lower] == state:
                        return city.strip()
            
            # Se não encontrou cidade, procura por bairros
            neighborhoods = [(loc, conf) for loc, conf, type_ in locations if type_ == 'neighborhood']
            if neighborhoods:
                for neighborhood, confidence in neighborhoods:
                    neighborhood_lower = self.normalize_text(neighborhood)
                    
                    # Se é um bairro conhecido
                    if neighborhood_lower in self.neighborhood_to_city:
                        city = self.neighborhood_to_city[neighborhood_lower]
                        if state is None or self.city_to_state.get(city) == state:
                            return city.strip()
                    
                    # Se parece ser um bairro e temos confiança suficiente
                    elif confidence >= 0.7:
                        if state:
                            # Tenta inferir a cidade do bairro pelo contexto
                            for city, city_state in self.city_to_state.items():
                                if city_state == state and city in text.lower():
                                    return city.strip()
                        else:
                            # Se não temos estado, procura a cidade no contexto
                            for city in self.city_to_state:
                                if city in text.lower():
                                    return city.strip()
        
        # Se não encontrou nada pelos métodos anteriores, tenta encontrar por nome parcial
        # Pega a primeira palavra que parece um nome próprio
        for token in doc:
            if token.pos_ == "PROPN" and token.text.lower() not in self.ignore_words:
                possible_city = self.find_matching_city(token.text, state)
                if possible_city:
                    return possible_city
        
        # Última tentativa: verifica se o texto inteiro é uma cidade
        if normalized_text in self.state_capitals:
            return text.strip()
            
        return None

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract city and state information from text.
        
        Args:
            text (str): Input text containing city and state information
            
        Returns:
            Dict[str, Optional[str]]: Dictionary with 'city' and 'state' keys
        """
        # Normalize the text first
        normalized_text = self.normalize_text(text)
        
        # Se o texto é uma capital de estado, já sabemos a cidade e o estado
        if normalized_text in self.state_capitals:
            return {
                'city': text.strip(),
                'state': self.state_capitals[normalized_text]
            }
        
        # First try to extract state
        state = self.extract_state(text)
        
        # Then extract city
        city = self.extract_city(text, state)
        
        # Se encontrou uma cidade que é capital de estado, garante que o estado está correto
        if city:
            city_lower = self.normalize_text(city)
            if city_lower in self.state_capitals:
                state = self.state_capitals[city_lower]
        
        return {
            'city': city,
            'state': state
        } 