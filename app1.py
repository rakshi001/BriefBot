import streamlit as st
import requests
from PyPDF2 import PdfReader
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PDFChatbot:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.extracted_text = ""
        self.chat_history = []

    def extract_text_from_pdfs(self, pdf_files):
        """
        Extract text from uploaded PDF files
        """
        self.extracted_text = ""
        for pdf in pdf_files:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    self.extracted_text += page_text + "\n"

    def call_gemini_api(self, prompt):
        """
        Make a POST request to Gemini API (v1) to get the response
        """
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={self.api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            raise Exception(f"Gemini API Error {response.status_code}: {response.text}")

    def get_pdf_response(self, question, retries=3, backoff=2):
        """
        Generate response based on PDF content and user question, with retry logic
        """
        if not self.extracted_text:
            return "Please upload and process PDFs first."

        # Add question to chat history
        self.chat_history.append(f"User: {question}")

        # Create prompt using extracted text and previous messages
        prompt = f"""
        Context from PDF:
        {self.extracted_text}

        Previous Chat History:
        {" ".join(self.chat_history)}

        Question: {question}

        Please provide a helpful answer based only on the PDF context above. If the answer isn't present, say so.
        """

        for attempt in range(retries):
            try:
                response_text = self.call_gemini_api(prompt)
                self.chat_history.append(f"Bot: {response_text}")
                return response_text
            except Exception as e:
                if "429" in str(e):  # Handle rate limiting
                    wait = backoff ** attempt
                    st.warning(f"Rate limit hit. Retrying in {wait} seconds...")
                    time.sleep(wait)
                else:
                    return f"An error occurred: {str(e)}"

        return "Too many requests. Please try again later."

def main():
    st.set_page_config(page_title="Brief-Bot", page_icon="📚")
    st.title("📚 Brief Bot")
    st.header("Your PDF Partner 🤖")

    # Initialize the chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = PDFChatbot()

    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📄 Upload PDFs")
        pdf_files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)

        if st.button("Process PDFs"):
            if pdf_files:
                with st.spinner("Extracting text from PDFs..."):
                    st.session_state.chatbot.extract_text_from_pdfs(pdf_files)
                    st.success("PDFs processed successfully!")
            else:
                st.warning("Please upload at least one PDF file.")

    # Main chat area
    if 'chatbot' in st.session_state:
        if st.session_state.chatbot.chat_history:
            st.markdown("### Chat History")
            for message in st.session_state.chatbot.chat_history:
                st.write(message)

        user_question = st.text_input("Ask a question about your PDF:")

        if user_question:
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.get_pdf_response(user_question)
                st.write(f"**Response:** {response}")

if __name__ == "__main__":
    main()
