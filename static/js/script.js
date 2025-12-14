function generateArticle() {
    const tweet = document.getElementById("tweet").value;
    const author = document.getElementById("author").value;
    const date = document.getElementById("date").value;

    document.getElementById("output").innerText = "Generating article...";

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            tweet: tweet,
            author: author,
            date: date
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.article) {
            document.getElementById("output").innerText = data.article;
        } else {
            document.getElementById("output").innerText = "Error generating article.";
        }
    })
    .catch(error => {
        document.getElementById("output").innerText = "Server error.";
    });
}

