import os
from dotenv import load_dotenv
from groq import Groq
from retriever import search

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using only the provided notes.

You MUST reply using EXACTLY this format, no deviations:

- Summary: <one line answer>

- Key Points:
  - <point 1>
  - <point 2>
  - <point 3>

- Source: <filename only — no square brackets, no punctuation around it>

- Confidence: <write only one word: High, Medium, or Low>

- Related Topics:
  - <main subject or theme extracted from Chunk 2>
  - <main subject or theme extracted from Chunk 3>

Rules:
- Do not add any text before or after the format above.
- Do not rename, skip, or reorder any section.
- If the answer is not in the notes at all, reply only with: I don't know based on my notes.
- For Related Topics: always extract the main subject or theme from Chunk 2 and Chunk 3. Never write None.

Example of a perfect response:

- Summary: The meeting discussed the Q3 product roadmap.

- Key Points:
  - The team agreed to prioritize the mobile app rewrite.
  - Budget approved is 50,000 USD.
  - Next meeting is on Friday.

- Source: monday_meeting.txt

- Confidence: High

- Related Topics:
  - Building self-confidence
  - Flirting techniques
"""


def answer(query, n_results=3):
    hits = search(query, n_results=n_results)

    context = "\n\n".join(
        f"Chunk {i} [{hit['source']}]\n{hit['text']}"
        for i, hit in enumerate(hits, 1)
    )

    prompt = (
        f"Use ONLY the following notes to answer the question.\n\n"
        f"{context}\n\n"
        f"Question: {query}\n\n"
        f"Use the topics from Chunk 2 and Chunk 3 to fill the Related Topics section. "
        f"Extract the main subject or theme from each of those chunks as related topics. "
        f"Never write None.\n\n"
        f"Answer:"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    query = "what was discussed in monday's meeting?"
    print(f"Q: {query}\n")
    print(answer(query))
