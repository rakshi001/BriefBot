📚 Brief Bot – Your PDF Partner
Brief Bot is an interactive chatbot designed to transform the way students engage with their study materials. By uploading PDFs, users can ask questions and receive precise, context-aware answers directly from the content of their documents. This tool is crafted with the goal of improving the educational experience by eliminating distractions and promoting focused learning.

🌟 Features
PDF Interaction: Upload one or multiple PDFs and interact with the content seamlessly.
AI-Powered Responses: Receive detailed, context-specific answers powered by Google Gemini AI.
Chat History: Retain the flow of conversation with a persistent chat history.
User-Friendly Interface: Built with Streamlit for an intuitive and clean user experience.
🛠️ Technologies Used
Python: Core programming language.
Streamlit: For building the interactive web application.
Google Generative AI: To provide intelligent and context-aware answers.
PyPDF2: For extracting text from uploaded PDFs.
dotenv: For managing API keys securely.
🚀 How to Run Locally
Clone the Repository:

bash
Copy code
git clone https://github.com/rakshi001/BriefBot.git
cd BriefBot
Set Up Environment:

Create a virtual environment:
bash
Copy code
python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Configure API Key:

Create a .env file in the project root:
plaintext
Copy code
GOOGLE_API_KEY=your_google_gemini_api_key
Run the Application:

bash
Copy code
streamlit run app1.py
Upload PDFs and Interact:

Open the app in your browser and start uploading PDFs to ask questions!
🎯 Purpose
Brief Bot is tailored for students to:

Simplify their interaction with academic materials.
Save time by directly querying PDFs without unnecessary distractions.
Enhance the educational experience with AI-driven insights.

📌 Future Enhancements
Support for additional file formats (e.g., Word documents).
Advanced NLP features for summarization and keyword extraction.
Multi-language support for global accessibility.


🤝 Contributions
Contributions are welcome! Feel free to open issues or submit pull requests to improve the tool.

🌐 Live Demo
Visit the hosted app here: https://briefbot-lnktgmpdknpuqgcjq3qscd.streamlit.app/
