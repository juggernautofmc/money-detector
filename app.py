from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

def detect_money_amount(pmpt):
    # Found money amounts will go here
    results = []

    # Define regex patterns
    # PATTERN 1: Currency -> Number
    ptn1 = re.compile(r"""
    (                               # currency (symbol OR code)
        [\$€£¥₹₽₿]                  # any one symbol
        |                           # OR
        USD|CAD|AUD|GBP|CHF|JPY|EUR|CNY|INR|MXN
    )
    \s{0,2}                             # optional space

    (                               # number part
        \d+(?!,\d)                    # digits NOT followed by comma
        |                           # OR
        \d{1,3}(,\d{3})+            # properly comma-grouped number
    )

    (\.\d+)?                        # optional decimal

    [KMBT]?                         # optional suffix (K, M, B, T)

    \b                              # word boundary
""", re.IGNORECASE | re.VERBOSE)
    
    # PATTERN 2: Number -> Currency
    ptn2 = re.compile(r"""
    (                               # number part
        \d+(?!,)                    # digits NOT followed by comma
        |                           # OR
        \d{1,3}(,\d{3})+            # properly comma-grouped number
    )

    (\.\d+)?                        # optional decimal

    [KMBT]?                         # optional suffix (K, M, B, T)

    (\s(hundred|thousand|million|billion|trillion))? # optional word suffix 

    \s?                             # optional space

    (                               
                                   # currency code
        USD|CAD|AUD|GBP|CHF|JPY|EUR|CNY|INR|MXN
        |                          # OR
        dollar(s)?|euro(s)?|yen|pound(s)?|franc(s)?|yuan|peso(s)?|rupee(s)?|ruble(s)?|bitcoin(s)?
                                   # word currency
    )

    \b                              # word boundary
""", re.IGNORECASE | re.VERBOSE)
    match1 = re.finditer(ptn1, pmpt)
    match2 = re.finditer(ptn2, pmpt)
    for match in match1:
        results.append({
            "text": match.group(),
            "start": match.start(),
            "end": match.end()
        })
    for match in match2:
        discard = False

        for match1 in results:
            if match.start() < match1["end"] and match1["start"] < match.end():
                discard = not discard
                break
        if (not discard):
            results.append({
                "text": match.group(),
                "start": match.start(),
                "end": match.end()
            })
    
    results.sort(key=lambda x: x["start"])
    
    return results

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    text = request.form.get("text", "")
    matches = detect_money_amount(text)

    return jsonify({
        "text": text,
        "matches": matches
    })



if __name__ == "__main__":
    app.run(debug=True)