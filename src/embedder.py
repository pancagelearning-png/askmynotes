import os
import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

NOTES_DIR = os.path.join(os.path.dirname(__file__), "..", "notes")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
COLLECTION_NAME = "my_notes"

embedding_fn = DefaultEmbeddingFunction()


def read_file(path):
    if path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif path.endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return ""


def load_notes(notes_dir):
    notes = []
    for path in sorted(glob.glob(os.path.join(notes_dir, "*.txt")) +
                       glob.glob(os.path.join(notes_dir, "*.pdf"))):
        notes.append({"source": os.path.basename(path), "content": read_file(path)})
    return notes


def main():
    notes = load_notes(NOTES_DIR)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = []
    metadatas = []
    for note in notes:
        splits = splitter.split_text(note["content"])
        print(f"{note['source']}: {len(splits)} chunk(s)")
        chunks.extend(splits)
        metadatas.extend([{"source": note["source"]}] * len(splits))

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_or_create_collection(
        COLLECTION_NAME, embedding_function=embedding_fn
    )
    ids = [str(i) for i in range(len(chunks))]
    collection.add(documents=chunks, metadatas=metadatas, ids=ids)

    print(f"\nStored {len(chunks)} total chunks in ChromaDB collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    main()
