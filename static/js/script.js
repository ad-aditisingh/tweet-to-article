function generateArticle() {
    const tweet = document.getElementById("tweet").value.trim();
    const author = document.getElementById("author").value.trim();
    const date = document.getElementById("date").value.trim();
    const output = document.getElementById("output");

    if (!tweet) {
        output.innerText = "Please enter a tweet.";
        return;
    }

    output.innerText = "Generating article...";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tweet, author, date })
    })
    .then(res => res.json())
    .then(data => {
        if (!data || !data.article) {
            output.innerText = "Could not generate article.";
            return;
        }

        let text = data.article;

        // -------- HEADLINE --------
        let headline = "";

        // Priority 1: Headline:
        const h1 = text.match(/Headline:\s*([\s\S]*?)\n\n/i);
        if (h1) {
            headline = h1[1].trim();
        } else {
            // Priority 2: **Markdown headline**
            const h2 = text.match(/\*\*(.+?)\*\*/);
            if (h2) {
                headline = h2[1].trim();
            } else {
                // Fallback
                headline = `${author || "Public Figure"} Highlights Key Views`;
            }
        }

        // -------- ARTICLE BODY --------
        let body = text;

        // Remove headline labels & markdown
        body = body
            .replace(/Headline:[\s\S]*?\n\n/i, "")
            .replace(/\*\*/g, "")
            .replace(/Disclaimer:[\s\S]*/i, "")
            .replace(/\n+/g, " ")
            .trim();

        output.innerHTML = `
            <div class="headline">${headline}</div>
            <div class="article">${body}</div>
            <div class="disclaimer">
                The statement attributed to ${author || "the author"} has not been independently verified and is presented here for informational purposes only.
            </div>
        `;
    })
    .catch(() => {
        output.innerText = "Server error. Please try again.";
    });
}
