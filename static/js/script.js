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
        body: JSON.stringify({
            tweet: tweet,
            author: author,
            date: date
        })
    })
    .then(res => res.json())
    .then(data => {
        if (!data || !data.article) {
            output.innerText = "Could not generate article.";
            return;
        }

        const text = data.article;

        // ----------------------------
        // HEADLINE (with safe fallback)
        // ----------------------------
        const headlineMatch = text.match(/Headline:\s*([\s\S]*?)\n\n/i);
        const headline = headlineMatch
            ? headlineMatch[1].trim()
            : `${author || "Public Figure"} Shares Views on Technology`;

        // ----------------------------
        // ARTICLE BODY (ROBUST)
        // ----------------------------
        const articleMatch = text.match(/Article:\s*([\s\S]*)/i);
        let articleBody = articleMatch ? articleMatch[1] : text;

        // Keep ONLY first paragraph, remove extra text safely
        articleBody = articleBody
            .replace(/Disclaimer:[\s\S]*/gi, "")
            .replace(/\n+/g, " ")
            .trim();


        // ----------------------------
        // RENDER OUTPUT (PLAIN STYLE)
        // ----------------------------
        output.innerHTML = `
            <div class="headline">${headline}</div>
            <div class="article">${articleBody}</div>
            <div class="disclaimer">
                The statement attributed to ${author || "the author"} has not been independently verified and is presented here for informational purposes only.
            </div>
        `;
    })
    .catch(() => {
        output.innerText = "Server error. Please try again.";
    });
}
