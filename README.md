# 🤖 AI-Powered Technical Recruiter (RAG Pipeline)
## 🎯 Objective

Build an AI-powered assistant capable of automating the resume screening process using Retrieval-Augmented Generation (RAG). The project allows recruiters to chat with a database of candidate resumes using natural language queries like "Who has experience with Python and AWS?" to instantly find the best fits.
## ❓ Problem

Technical recruitment is time-consuming and manual.

    Challenge: Recruiters have to manually open, read, and cross-reference hundreds of PDF resumes to find specific skills.

    Context: Keyword searches (Ctrl+F) often miss context (e.g., distinguishing "used Python" from "built Python tools").

The goal is to build a system that:

    Ingests raw PDF resumes.

    Understands context using Vector Embeddings.

    Recommends candidates based on semantic meaning, not just keywords.

## 🛠 Tech Stack

    Language: Python 3.10+

    LLM (Brain): Google Gemini 2.5 Flash (via Google AI Studio)

    Orchestration: LangChain (Modern LCEL Architecture)

    Vector Database: ChromaDB

    Embeddings: Google Generative AI Embeddings

    Interface: Gradio (Web UI)

    Utilities: PyPDFLoader, Dotenv

## 📂 Project Structure

Note: The resumes folder is where you place your candidate PDFs.
```Plaintext

RAG_hr_assistant/
├── app.py                 # Frontend (Gradio Web Interface)
├── backend.py             # RAG Logic & Chain Definition
├── setup_database.py      # Script to ingest PDFs into ChromaDB
├── processed_files.txt    # Log of resumes that have already been embedded
├── .env                   # API Keys (Not included in repo)
├── .gitignore             # Git exclusion rules
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── chroma_db_data/        # Vector Database storage (Auto-generated)
└── resumes/               # Folder for PDF resumes
```
## 🚀 How to Run
1. Clone the Repository
```Bash

git clone https://github.com/YOUR_USERNAME/ai-resume-assistant.git
cd ai-resume-assistant
```
2. Install Dependencies
```Bash

pip install -r requirements.txt
```
3. Configuration

Create a .env file in the root directory and add your Google API Key:
```Ini, TOML

GOOGLE_API_KEY=your_api_key_here
```
4. Build the Knowledge Base

Place your PDF resumes into the resumes/ folder, then run the ingestion script to create the vector database:
```Bash

python setup_database.py
```
Output: 🎉 Success! Database ready at './chroma_db_data'.
5. Launch the Recruiter AI

Run the application to start the web interface:
```Bash

python app.py
```
Click the local URL (e.g., http://127.0.0.1:7860) to open the chatbot.
## 📋 Examples

User Query:

    "Find me a candidate with strong Python skills but no cloud experience."

AI Response:

    "Based on the resumes, Candidate John Doe is a strong match. He has 5 years of experience in Python, specifically in Data Science and scripting. His resume mentions 'Local Server Management' but explicitly does not list AWS, Azure, or GCP experience, fitting your requirement for no cloud background."

## 🧩 RAG Pipeline Architecture

This project follows a Modern LangChain LCEL (LangChain Expression Language) workflow:
```Code snippet

graph TD;
    A[PDF Resumes] -->|PyPDFLoader| B[Text Chunks];
    B -->|Google Embeddings| C[Vector Database (Chroma)];
    D[User Question] -->|Retriever| C;
    C -->|Top 5 Context Matches| E[Prompt Template];
    E -->|Context + Question| F[Gemini 2.5 Flash];
    F --> G[Recruiter Recommendation];
```
## 💡 Key Features

    Semantic Search: Finds candidates based on meaning, not just keywords (e.g., "AI Expert" will find "Machine Learning Engineer").

    Modern Tech Stack: Built using the latest LangChain LCEL syntax for cleaner, faster code.

    Cost-Efficient: Optimized to use Gemini 2.5 Flash, balancing high speed with low API costs.

    Source Citations: The system retrieves and cites the specific resumes used to generate the answer.

    Interactive UI: Fully functional web interface using Gradio.

## 🔐 Authentication

This project uses a .env file to manage the GOOGLE_API_KEY securely. The key is never hardcoded into the script.
## 📜 License

This project is licensed under the MIT License. See the LICENSE file for more details.