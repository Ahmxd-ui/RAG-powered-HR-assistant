import gradio as gr
from backend import get_qa_chain

#  Initialize the AI Brain
# We load the chain once when the app starts so it's fast.
print("⏳ Loading AI Brain...")
qa_chain = get_qa_chain()
print("✅ AI Ready!")

def ask_recruiter(query):
    if not query:
        return "Please enter a question."
    
    #  Send question to Backend
    # The new backend returns a simple string, so we just return it.
    answer = qa_chain.invoke(query)
    
    return answer

#  Build the UI
with gr.Blocks(title="AI Resume Assistant") as demo:
    gr.Markdown("# 🤖 AI Technical Recruiter")
    gr.Markdown("Ask questions about the candidates in your database.")
    
    with gr.Row():
        input_box = gr.Textbox(label="Your Question", placeholder="e.g., Who has experience with Python and AWS?")
        submit_btn = gr.Button("Analyze Resumes", variant="primary")
    
    output_box = gr.Textbox(label="Recruiter's Recommendation", lines=12, interactive=False)
    
    # Connect the Enter key and the Button to the function
    submit_btn.click(fn=ask_recruiter, inputs=input_box, outputs=output_box)
    input_box.submit(fn=ask_recruiter, inputs=input_box, outputs=output_box)

#  Launch
if __name__ == "__main__":
    demo.launch()