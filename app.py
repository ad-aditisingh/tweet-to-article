from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from groq import Groq
from analyzer import build_description

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_article():
    data = request.json or {}

    tweet = data.get("tweet", "").strip()
    author = data.get("author", "Public Figure")
    date = data.get("date", "Unknown date")

    if not tweet:
        return jsonify({"article": "Please enter a tweet."})

    # 🔹 Your deterministic system
    description = build_description(tweet, author, date)

    prompt = f"""
You are a professional journalist.

Rewrite the following description into a neutral, well-written news article.
Do NOT add new facts.
Do NOT remove information.
Improve clarity and flow only.

Description:
\"\"\"{description}\"\"\"

Output format:
Headline:
Article:
Disclaimer:
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You rewrite text into neutral news articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )

        article = response.choices[0].message.content.strip()
        return jsonify({"article": article})

    except Exception as e:
        print("GROQ ERROR:", e)

        fallback = f"""
Headline:
{author} Shares Statement on Social Media

Article:
{description}

Disclaimer:
This article is an AI-assisted rewrite of a public tweet and does not verify or endorse the claims made.
"""
        return jsonify({"article": fallback})

@app.route("/test")
def test():
    return jsonify({"status": "Flask + Groq + Analyzer system is running."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
