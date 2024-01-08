# chatbot_ui.py

import gradio as gr
import os
# Import necessary components from your chatbot implementation
if "OPENAI_API_KEY" not in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

from mvd_chatbot import MVDAssistant
# Initialize your chatbot
chatbot = MVDAssistant()

def chat_with_bot(message, history):
    """
    Function to get chatbot response for the user input.
    """
    try:
        # Assuming the last message in history is the user's message
        response = chatbot.run_query(message)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

# Create a Gradio ChatInterface
iface = gr.ChatInterface(
    fn=chat_with_bot, 
    title="RAG Chatbot - Indian Motor Vehicles Law",
    description="RAG chatbot using OpenAI and FAISS vector db"
)

if __name__ == "__main__":
    iface.launch()