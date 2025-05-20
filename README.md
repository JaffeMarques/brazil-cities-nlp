# Brazil Cities NLP

This project implements a Natural Language Processing (NLP) system to extract Brazilian city and state information from different text formats.

## Features

- Recognition of cities and states in different formats:
  - "Mogi das Cruzes - SP"
  - "Mogi das Cruzes / São Paulo"
  - "Mogi das Cruzes / SP"
  - "Mogi - SP"
- Text normalization
- Structured information extraction

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

4. Download the spaCy model:
```bash
python -m spacy download pt_core_news_sm
```

## Usage

```python
from city_extractor import CityExtractor

extractor = CityExtractor()
result = extractor.extract("Mogi das Cruzes - SP")
print(result)
# Output: {'city': 'Mogi das Cruzes', 'state': 'SP'}
```

## Testing

Run the tests with:
```bash
pytest
``` 