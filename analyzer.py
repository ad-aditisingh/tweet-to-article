def extract_main_statement(tweet: str) -> str:
    if not tweet:
        return ""

    for sep in [".", "!", "?"]:
        if sep in tweet:
            return tweet.split(sep)[0].strip()

    return tweet.strip()


def build_description(tweet: str, author: str, date: str) -> str:
    main_statement = extract_main_statement(tweet)

    description = f"""
On {date}, {author} posted a message on Twitter stating that {main_statement.lower()}.

The post reflects the author's personal viewpoint as shared publicly on social media.
The statement has not been independently verified and is presented here for informational purposes only.
"""

    return description.strip()
