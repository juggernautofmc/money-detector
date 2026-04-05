# Money Amount Detector

A lightweight web application that detects and highlights monetary amounts in text using rule-based pattern matching. The system supports multiple currencies, formats, and edge cases, and is designed to be fast, explainable, and extensible.

---

## Overview

This project extracts monetary expressions from free-form text and highlights them in a user-friendly interface.

It focuses on:
- Structured monetary formats (e.g. `$120`, `€3,200`, `CHF 486.50`)
- Currency codes (e.g. `USD 1000`, `AUD 15,000`)
- Word-based expressions (e.g. `500 dollars`, `10k dollars`)
- Performance and robustness on long inputs

The system is implemented using Python (Flask) for the backend and JavaScript for the frontend.

---

## Features

- Detects currency symbols: `$ € £ ¥ ₹ ₽ ₿`
- Detects currency codes: `USD, CAD, AUD, GBP, CHF, JPY, EUR, CNY, INR, MXN`
- Supports comma-grouped numbers (e.g. `1,000`, `123,456`)
- Supports decimals (e.g. `89.99`)
- Supports suffixes (`K, M, B, T`)
- Handles both:
  - Currency → Number (`$100`, `USD 500`)
  - Number → Currency (`500 dollars`, `10k dollars`)
- Highlights detected values directly in the UI
- Handles long inputs efficiently

---

## Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS, JavaScript
- Core Logic: Python `re` (regular expressions)

---

## How It Works

### 1. Pattern Matching

Two primary regex patterns are used:

- Pattern 1: Currency → Number  
  Examples:
  - `$120`
  - `€3,200`
  - `CHF 486.50`

- Pattern 2: Number → Currency  
  Examples:
  - `500 dollars`
  - `10k dollars`
  - `1000 euros`

Both patterns are run over the full input text to generate candidate matches.

---

### 2. Match Aggregation

Matches from both patterns are:
- Collected into a single list
- Sorted by their position in the text
- Filtered to remove overlapping or conflicting matches

When overlaps occur, more structured matches such as symbol-based or currency-code-based formats are preferred over word-based matches.

---

### 3. Highlighting
 
The backend returns data in the following format:
 
```json
{
  "text": "...",
  "matches": [...]
}
```
 
The frontend then:
- Reconstructs the original string
- Wraps detected spans in `<span>` elements
- Applies CSS styling to highlight each detected money amount
 
This allows the user to see both the original input and the exact locations where monetary values were detected.
 
## Deployment
 
This project is deployed on Vercel via GitHub
 
 [Live Demo](https://money-detector-dusky.vercel.app)
 
## Example Input
 
```
I spent $120 on groceries and another €3,200 on a trip.
I also had about 500 dollars left.
```
 
## Example Output
 
- `$120` highlighted
- `€3,200` highlighted
- `500 dollars` highlighted
 
## Limitations
 
Does not currently support:
- Fully written numbers (e.g. "one hundred thousand dollars")
- Slang expressions (e.g. "a couple hundred bucks", "five mil")
 
Some ambiguous numeric phrases are intentionally ignored to reduce false positives. The regex-based approach prioritizes precision over recall for unstructured language.
 
## Future Work
 
This system can be extended into a hybrid architecture:
- **Regex layer:** fast, deterministic detection for structured formats
- **ML/NLP layer:** handles ambiguous or fully natural language expressions
 
Potential improvements:
- Parsing written-out numbers into numeric form
- Context-aware disambiguation
- Confidence scoring for matches
- Integration with lightweight NLP models
 
## Design Philosophy
 
The system prioritizes:
- **Speed:** linear-time scanning
- **Explainability:** deterministic pattern matching
- **Modularity:** easy extension with additional rules or models
 
## Author
 
Sami Alkharrat