# Tweet to Article
Tweet-to-Article is a web application that converts public tweets from influential figures into neutral, newspaper-style news articles.

Social media posts are often brief and informal, which can make it difficult to understand their meaning, context, or implications especially for global audiences. This project bridges that gap by transforming short-form tweets into clear, readable articles while preserving the original message.

## How It Works
The system uses a hybrid approach:
- A rule-based analyzer extracts the core idea of the tweet to maintain factual grounding.
- An AI language model rewrites the content into a neutral, journalistic format without adding new facts or opinions.

Each generated article includes:
- A clear headline
- A concise explanatory paragraph
- An ethical disclaimer stating that claims are unverified

## Tech Stack
- Python, Flask
- HTML, CSS, JavaScript
- Groq LLM API
- Render (deployment)

## Use Cases
- Helping readers interpret public statements clearly
- Providing structured summaries for journalists and researchers
- Improving cross-border understanding of social media communication

## Live Demo
https://tweet-to-article.onrender.com/
