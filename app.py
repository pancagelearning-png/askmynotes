import sys
import os
import traceback
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

print(f"GROQ_API_KEY present: {bool(os.environ.get('GROQ_API_KEY'))}", flush=True)

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
    try:
        print("Embedding notes...", flush=True)
        embed_notes()
        print("Ready!", flush=True)

        port = int(os.environ.get("PORT", 7860))
        demo.launch(server_port=port, server_name="0.0.0.0")
    except Exception as e:
        print(f"STARTUP ERROR: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)
