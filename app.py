from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai

# -----------------------
# Load environment variables
# -----------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")

# -----------------------
# Configure Gemini
# -----------------------
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# -----------------------
# Create Flask app
# -----------------------
app = Flask(__name__)

# -----------------------
# Home route
# -----------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------
# Generate article route
# -----------------------
@app.route("/generate", methods=["POST"])
def generate_article():
    data = request.json or {}

    tweet = data.get("tweet", "").strip()
    author = data.get("author", "Public Figure")
    date = data.get("date", "Unknown date")

    if not tweet:
        return jsonify({"article": "Please enter a tweet to generate an article."})

    prompt = f"""
Rewrite the following tweet into a neutral, factual news-style article.

Rules:
- Do NOT verify or judge the claims
- Do NOT add new facts
- Use neutral journalistic language
- Mention that claims are unverified

Tweet Author: {author}
Date: {date}
Platform: Twitter (X)

Tweet:
\"\"\"{tweet}\"\"\"

Output:
- Headline
- 2–3 paragraph article
- Disclaimer
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 400
            }
        )

        # Safe extraction
        article = response.text.strip()

        if article:
            return jsonify({"article": article})

        raise Exception("Empty response from Gemini")

    except Exception as e:
        print("Gemini blocked or failed:", e)

        # ---- GUARANTEED FALLBACK (DEMO MODE) ----
        fallback_article = f"""
Headline:
{author} Shares Statement on Social Media

Article:
On {date}, {author} posted a message on Twitter that drew public attention.

The post reflects the views of the author as expressed on the platform. While the statement has been discussed due to the influence of public figures, the claims made in the post have not been independently verified.

Such statements often generate conversation because of the speed and reach of social media.

Disclaimer:
This article is an AI-generated, informational rewrite of a public tweet and does not verify or endorse the claims made.
"""

        return jsonify({"article": fallback_article})

# -----------------------
# Test route (sanity check)
# -----------------------
@app.route("/test")
def test():
    return "Flask server is running successfully."

# -----------------------
# Run the app (MUST be last)
# -----------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
