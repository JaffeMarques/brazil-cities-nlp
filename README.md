# Brazil Cities NLP

This project implements a Natural Language Processing (NLP) system to extract Brazilian city and state information from different text formats. It's a fun project that demonstrates how to use NLP techniques to parse and understand location information in Brazilian Portuguese text.

## Project Purpose

This project was created as a fun exercise to explore NLP techniques for location extraction in Brazilian Portuguese. It's particularly useful for:
- Processing real estate listings
- Analyzing location mentions in social media
- Extracting structured location data from unstructured text
- Learning about NLP techniques for Portuguese language processing

## How It Works

The system uses a combination of techniques to extract location information:

1. **Text Normalization**
   - Removes accents and converts text to lowercase
   - Handles common variations in city and state names
   - Processes different separators (-, /, etc.)

2. **Named Entity Recognition (NER)**
   - Uses spaCy's Portuguese language model to identify location entities
   - Processes both full names and abbreviations
   - Handles compound names (e.g., "São Paulo", "Rio de Janeiro")

3. **Context-Aware Processing**
   - Recognizes neighborhood names in major cities
   - Understands location indicators (e.g., "em", "no", "na")
   - Handles state capitals and major cities specially

4. **Fuzzy Matching**
   - Uses similarity matching for partial city names
   - Handles common abbreviations and variations
   - Maintains a database of known cities and states

## Features

- Recognition of cities and states in different formats:
  - "Mogi das Cruzes - SP"
  - "Mogi das Cruzes / São Paulo"
  - "Mogi das Cruzes / SP"
  - "Mogi - SP"
- Text normalization
- Structured information extraction
- Neighborhood recognition for major cities
- Support for state capitals and abbreviations
- Context-aware location extraction

## Libraries Used

- **spaCy (3.7.2)**: For Portuguese language processing and NER
- **pandas (2.1.4)**: For data handling and processing
- **unidecode (1.3.7)**: For text normalization and accent removal
- **python-dotenv (1.0.0)**: For environment variable management
- **pytest (7.4.4)**: For testing

## Installation

1. Clone the repository
2. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note**: After installing the requirements, you need to download the Portuguese language model for spaCy. This is a separate step because language models are not included in the requirements.txt file.

4. Download the spaCy model:
```bash
python -m spacy download pt_core_news_sm
```

## Usage

```python
from city_extractor import CityExtractor

extractor = CityExtractor()

# Basic usage
result = extractor.extract("Mogi das Cruzes - SP")
print(result)
# Output: {'city': 'Mogi das Cruzes', 'state': 'SP'}

# Complex examples
examples = [
    "EU QUERO ALUGAR EM SÃO PAULO, GUARULHOS",
    "Procuro imóvel no Rio de Janeiro, Copacabana",
    "Apartamento em Belo Horizonte, Savassi",
    "Casa em São Paulo capital",
    "Quero morar em Porto Alegre, bairro Moinhos"
]

for example in examples:
    result = extractor.extract(example)
    print(f"Input: {example}")
    print(f"Result: {result}\n")
```

## Testing

The project includes comprehensive tests covering:
- Basic city and state extraction
- Complex compound names
- State-only inputs
- Invalid inputs
- Neighborhood recognition
- Context-aware extraction

Run the tests with:
```bash
pytest
```

## Contributing

Feel free to contribute to this project! Some ideas for improvement:
- Add more cities and neighborhoods
- Improve neighborhood recognition
- Add support for more location formats
- Enhance the NLP model with custom training
- Add more test cases

## License

This project is open source and available under the MIT License. 