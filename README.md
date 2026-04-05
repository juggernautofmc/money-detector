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

## Evaluation

### Runtime Analysis

The system operates in **linear time O(n)** with respect to input length.

- Each regex pattern performs a full scan over the input string
- Two patterns are used → total complexity remains O(n)
- Post-processing (sorting + overlap resolution) is also O(n log n) in the worst case due to sorting, but the number of matches is typically small relative to input size

In practice, the system performs efficiently even on long inputs, as demonstrated by stress testing with large multi-paragraph text.

---

### Stress Test Evaluation

The following long-form input was used to evaluate correctness, robustness, and edge case handling.
```text
The financial report mentioned that the company spent $12,450.75 on infrastructure, while another department recorded expenses of €9,999.99 for travel. In contrast, a smaller team only used GBP 1,200 for miscellaneous costs, and someone casually noted they had about 300 dollars left in their account.

Meanwhile, an investor claimed to have CHF 75,000.50 stored across multiple accounts, but another said they only had AUD 15,000 in liquid funds. Someone else transferred MXN 2,500 to a friend, while another logged JPY 120,000 as an expense. 

Things start getting weird: $1,23 is invalid, $12,34,567 is questionable, and $ 4x500 should definitely not count. Neither should expressions like $a + b$ or $x^2$. Also, phrases like “he ran a 10K race” or “the dataset had 100K entries” should not trigger money detection.

Now mixing formats: USD 500, CAD 1,000.25, EUR 7500, INR 85,000, CNY 6,500.00, ₿0.75, ₹500000, £120.00, and ¥3000 all appear in various contexts. Some are tightly formatted like CHF486.50 or AUD15000, others spaced like USD  200 or €  1,000.00.

Natural language creeps in: someone said they had five hundred dollars, another mentioned one thousand euros, and someone else talked about “a couple hundred bucks” or “a few grand” which should be ambiguous. There’s also “half a million in assets” and “north of ten million dollars” which your current system probably won’t catch.

Edge chaos continues: 100,000 (valid number but no currency), 12,00 (invalid grouping), 1,234,56 (invalid), $1000000 (valid), $ 1000000 (valid), $100,000,000 (valid), and random strings like $xyz123 or €abc shouldn’t pass.

Now overlapping bait: “I spent $500 and also around 500 dollars on something else,” and “He converted €1,000 into 1000 euros equivalent.” These might create competing matches.

More mixed input: CAD 2,500.75 was logged, followed by “approximately two thousand five hundred dollars” and then another entry of $2,500.75 again. Someone also wrote USD1000 without space, and EUR1000.50, and GBP100000.

Now filler spam to stress performance:

zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq

Final chaos: $999,999,999.99, EUR 0.01, GBP 123,456,789.00, INR 1,00,000 (Indian format, tricky), and random garbage like $ 12,3,4 or € 1,23,45 should test your grouping logic. Also we have $10k, €10m, or 10k pounds

End of stress test. AYYAAYAYAYAYAYAYAY
```

#### ✅ Correctly Detected

The system successfully detected structured monetary expressions including:

- `$12,450.75`
- `€9,999.99`
- `GBP 1,200`
- `300 dollars`
- `CHF 75,000.50`
- `AUD 15,000`
- `MXN 2,500`
- `JPY 120,000`
- `USD 500`
- `CAD 1,000.25`
- `EUR 7500`
- `INR 85,000`
- `CNY 6,500.00`
- `₿0.75`
- `₹500000`
- `£120.00`
- `¥3000`
- `CHF486.50`
- `AUD15000`
- `USD  200`
- `€  1,000.00`
- `$1000000`
- `$ 1000000`
- `$100,000,000`
- `$500`
- `500 dollars`
- `€1,000`
- `1000 euros`
- `CAD 2,500.75`
- `$2,500.75`
- `USD1000`
- `EUR1000.50`
- `GBP100000`
- `$999,999,999.99`
- `EUR 0.01`
- `GBP 123,456,789.00`
- `$10k`
- `€10m`
- `10k pounds`

These demonstrate support for:
- currency symbols and codes
- comma-grouped numbers
- decimals
- suffixes (K, M)
- flexible spacing
- both Currency → Number and Number → Currency formats

---

#### ❌ Correctly Rejected

The system correctly ignored invalid or non-monetary patterns:

- `$1,23` (invalid grouping)
- `$12,34,567` (invalid grouping)
- `$ 4x500` (non-numeric contamination)
- `$a + b`, `$x^2` (mathematical expressions)
- `10K race`, `100K entries` (non-monetary usage)
- `100,000` (no currency context)
- `12,00` (invalid grouping)
- `1,234,56` (invalid grouping)
- `$xyz123`, `€abc` (invalid format)
- `$ 12,3,4` (invalid grouping)
- `€ 1,23,45` (invalid grouping)

This demonstrates strong precision and resistance to false positives.

---

#### ⚠️ Known Limitations

The system intentionally does not detect:

- Fully written amounts:
  - "five hundred dollars"
  - "one thousand euros"
- Ambiguous or slang expressions:
  - "a couple hundred bucks"
  - "a few grand"
- Contextual phrases:
  - "half a million"
  - "north of ten million dollars"

These cases require semantic understanding and are better suited for NLP/ML-based approaches.

---

### Summary

The system demonstrates:

- High precision on structured monetary expressions
- Robust handling of edge cases and malformed inputs
- Strong performance on long, mixed-format text
- Clear separation between valid and invalid patterns

This validates the effectiveness of a deterministic, regex-based approach as a fast and reliable baseline system.

---

## Future Work
 
This system can be extended into a hybrid architecture:
- **Regex layer:** fast, deterministic detection for structured formats
- **ML/NLP layer:** handles ambiguous or fully natural language expressions
 
Potential improvements:
- Parsing written-out numbers into numeric form
- Context-aware disambiguation
- Confidence scoring for matches
- Integration with lightweight NLP models
 
## Author
 
Sami Alkharrat