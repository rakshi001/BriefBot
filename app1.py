import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class PDFChatbot:
    def __init__(self):
        # Initialize the model and chat history
        self.model = genai.GenerativeModel('gemini-pro')
        self.extracted_text = ""
        self.chat_history = []  # Store chat history to maintain context

    def extract_text_from_pdfs(self, pdf_files):
        """
        Extract text from uploaded PDF files
        """
        self.extracted_text = ""
        for pdf in pdf_files:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                self.extracted_text += page.extract_text()

    def get_pdf_response(self, question, retries=3, backoff=2):
        """
        Generate response based on PDF content and user question with retry logic for handling 429 errors
        """
        if not self.extracted_text:
            return "Please upload and process PDFs first."
        
        # Append user's question to chat history
        self.chat_history.append(f"User: {question}")

        # Combine the chat history and extracted PDF text
        prompt = f"""
        Context from PDF:
        {self.extracted_text}

        Previous Chat History:
        {" ".join(self.chat_history)}

        Question: {question}

        Please provide a detailed and accurate answer based on the PDF context.
        If the information is not available in the context, you can say it's not available in the PDF.
        """
        
        # Retry logic with exponential backoff for handling 429 errors
        for attempt in range(retries):
            try:
                # Generate response
                response = self.model.generate_content(prompt)
                self.chat_history.append(f"Bot: {response.text}")  # Append bot's response to history
                return response.text
            except Exception as e:
                if "429" in str(e):  # Check for "429 Resource Exhausted"
                    wait_time = backoff ** attempt  # Exponential backoff
                    st.warning(f"Rate limit hit, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)  # Wait before retrying
                else:
                    return f"An error occurred: {str(e)}"

        # If retries are exhausted
        return "We are experiencing high demand. Please try again later."

def main():
    st.set_page_config(page_title="Brief-Bot", page_icon="📚")
    st.title("Brief Bot📚")
    st.header("Your PDF Partner ")

    # Initialize the chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = PDFChatbot()

    # Sidebar for PDF upload
    with st.sidebar:
        st.header("Upload PDFs")
        pdf_files = st.file_uploader(
            "Choose PDF files", 
            type=['pdf'], 
            accept_multiple_files=True
        )

        if st.button("Process PDFs"):
            if pdf_files:
                with st.spinner("Processing PDFs..."):
                    st.session_state.chatbot.extract_text_from_pdfs(pdf_files)
                    st.success("PDFs processed successfully!")
            else:
                st.warning("Please upload PDF files first.")

    # Main chat interface
    if 'chatbot' in st.session_state:
        # Display chat history
        if st.session_state.chatbot.chat_history:
            for message in st.session_state.chatbot.chat_history:
                st.write(message)

        user_question = st.text_input("Ask a question about your PDF:")

        if user_question:
            with st.spinner("Generating response..."):
                response = st.session_state.chatbot.get_pdf_response(user_question)
                st.write(f"Response: {response}")

if __name__ == "__main__":
    main()
