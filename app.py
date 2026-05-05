import sys
import os
import traceback

print("Step 1: basic imports done", flush=True)

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
    print(f"GROQ_API_KEY present: {bool(os.environ.get('GROQ_API_KEY'))}", flush=True)

    print("Step 2: importing gradio", flush=True)
    import gradio as gr

    print("Step 3: importing embedder", flush=True)
    from embedder import main as embed_notes

    print("Step 4: importing chain", flush=True)
    from chain import answer

    print("Step 5: all imports done", flush=True)

    def chat(message, history):
        response = answer(message)
        return response

    demo = gr.ChatInterface(
        fn=chat,
        title="AskMyNotes",
        description="Ask questions about your personal notes and PDFs",
    )

    if __name__ == "__main__":
        print("Step 6: starting embedding", flush=True)
        embed_notes()
        print("Step 7: embedding done, launching gradio", flush=True)

        demo.launch()

except Exception as e:
    print(f"STARTUP ERROR: {e}", flush=True)
    traceback.print_exc()
    sys.exit(1)
