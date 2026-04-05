function highlightText(text, matches) {
    let result = "";
    let idx = 0;
    let numFound = 0;

    matches.forEach(match => {
        result += text.slice(idx, match.start);

        result += '<span class="highlight">' + text.slice(match.start, match.end) + "</span>";

        idx = match.end;
        numFound++;
    });
    result += text.slice(idx);

    document.getElementById("output").innerHTML = result;
    document.getElementById("num").innerHTML = numFound;
}

async function detect(e) {
    e.preventDefault();

    const text = document.getElementById("input").value;
    const formData = new FormData();
    formData.append("text", text);

    try {
        const response = await fetch("/detect", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        highlightText(data.text, data.matches);

    }
    catch (error) {
        console.error("Failed to fetch data:", error);
    }
}