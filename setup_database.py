import os
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()


PDF_FOLDER_PATH = "./resumes"
DB_PATH = "./chroma_db_data"
HISTORY_FILE = "processed_files.txt"  # remember what we finished

def create_vector_db():
    #Setup Embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    #Get list of all PDF files
    if not os.path.exists(PDF_FOLDER_PATH):
        print(" No resumes folder found!")
        return
    
    all_files = [f for f in os.listdir(PDF_FOLDER_PATH) if f.endswith('.pdf')]
    
    #Check history (What have we already done?)
    processed_files = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            processed_files = f.read().splitlines()

    # Filter out files we already did
    files_to_do = [f for f in all_files if f not in processed_files]
    
    print(f"Total Resumes: {len(all_files)}")
    print(f"Already Done: {len(processed_files)}")
    print(f"Remaining to do: {len(files_to_do)}")
    
    if not files_to_do:
        print("All resumes are already in the database!")
        return

    #Initialize Database
    vector_db = Chroma(embedding_function=embeddings, persist_directory=DB_PATH)

    #Process ONE file at a time
    for file in files_to_do:
        print(f"\nProcessing: {file}...")
        
        try:
            # Load
            file_path = os.path.join(PDF_FOLDER_PATH, file)
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            # Chunk
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
            chunks = text_splitter.split_documents(docs)
            
            # Add metadata
            for chunk in chunks:
                chunk.metadata["source"] = file

            # Save to DB (The part that hits the API)
            vector_db.add_documents(chunks)
            
            # Update History File (Save Checkpoint)
            with open(HISTORY_FILE, "a") as f:
                f.write(file + "\n")
            
            print(f"Saved {file} to database.")
            
            # SLEEP
            print("Resting for 10 seconds to respect Google...")
            time.sleep(10)

        except Exception as e:
            if "429" in str(e):
                print(f"\nHIT RATE LIMIT on {file}!")
                print(" STOPPING SCRIPT. Please wait 5-10 minutes then run this script again.")
                print(" Don't worry, your progress on previous files is saved.")
                break # Exit the loop so you can restart later
            else:
                print(f"    Error on {file}: {e}")

if __name__ == "__main__":
    create_vector_db()