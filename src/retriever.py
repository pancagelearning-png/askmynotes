import os
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "my_notes"

embedding_fn = DefaultEmbeddingFunction()
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(
    COLLECTION_NAME, embedding_function=embedding_fn
)


def search(query, n_results=3):
    results = collection.query(query_texts=[query], n_results=n_results)
    hits = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        hits.append({"source": meta["source"], "text": doc})
    return hits


if __name__ == "__main__":
    query = "what was discussed in the meeting?"
    print(f"Query: {query}\n")
    for i, hit in enumerate(search(query), 1):
        print(f"Result {i} — {hit['source']}")
        print(hit["text"])
        print()
