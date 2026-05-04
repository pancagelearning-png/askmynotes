import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import gradio as gr
from chain import answer
from embedder import main as embed_notes


def chat(message, history):
    response = answer(message)
    return response


demo = gr.ChatInterface(
    fn=chat,
    title="AskMyNotes",
    description="Ask questions about your personal notes and PDFs",
    type="messages",
)

if __name__ == "__main__":
    print("Embedding notes...")
    embed_notes()
    print("Ready!")

    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_port=port, server_name="0.0.0.0")
