import re
import spacy
from unidecode import unidecode
from typing import Dict, Optional, Tuple

class CityExtractor:
    def __init__(self):
        """Initialize the CityExtractor with spaCy model and state mappings."""
        self.nlp = spacy.load("pt_core_news_sm")
        
        # Mapeamento de estados (siglas e nomes completos)
        self.state_mapping = {
            'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
            'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
            'GO': 'Goiás', 'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul',
            'MG': 'Minas Gerais', 'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná',
            'PE': 'Pernambuco', 'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina',
            'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
        }
        
        # Criar mapeamento reverso (nome completo -> sigla)
        self.reverse_state_mapping = {v.lower(): k for k, v in self.state_mapping.items()}

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

        return None

    def extract_city(self, text: str, state: Optional[str] = None) -> Optional[str]:
        """Extract city name from text."""
        # Remove state information if present
        if state:
            text = re.sub(rf'\s*[-\/]\s*{state}\b', '', text, flags=re.IGNORECASE)
            text = re.sub(rf'\s*[-\/]\s*{self.state_mapping[state]}\b', '', text, flags=re.IGNORECASE)
        
        # Remove common separators
        text = re.sub(r'\s*[-\/]\s*', ' ', text)
        
        # Process with spaCy
        doc = self.nlp(text)
        
        # Get the first noun phrase or the whole text if no noun phrase is found
        city = None
        for chunk in doc.noun_chunks:
            if chunk.root.pos_ in ['NOUN', 'PROPN']:
                city = chunk.text.strip()
                break
        
        if not city:
            # If no noun phrase found, take the first part before any separator
            parts = re.split(r'\s*[-\/]\s*', text)
            city = parts[0].strip()
        
        return city if city else None

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extract city and state information from text.
        
        Args:
            text (str): Input text containing city and state information
            
        Returns:
            Dict[str, Optional[str]]: Dictionary with 'city' and 'state' keys
        """
        # First try to extract state
        state = self.extract_state(text)
        
        # Then extract city
        city = self.extract_city(text, state)
        
        return {
            'city': city,
            'state': state
        } 