import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

DB_PATH = "./chroma_db_data"

def format_docs(docs):
    # This takes the list of documents and joins their content into one big string
    return "\n\n".join(doc.page_content for doc in docs)

def get_qa_chain():
    #  Connect to Memory
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})

    #  Connect to Brain
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    #  Prompt
    prompt = PromptTemplate.from_template(
        """
        You are an expert Technical Recruiter.
        Answer the question based ONLY on the following resumes.

        RESUMES:
        {context}

        QUESTION: {question}

        ANSWER:
        """
    )

    #  The Chain (With Formatting)
    rag_chain = (
        {
            # We pipe the retriever results into our helper function
            "context": retriever | format_docs, 
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


if __name__ == "__main__":
    try:
        qa = get_qa_chain()
        print(" Recruiter AI is ready! (Type 'exit' to stop)")

        while True:
            query = input("\nRecruiter: ")
            if query.lower() == "exit": break

            # Invoke the chain
            response = qa.invoke(query)
            print(f"\n Answer:\n{response}")
            
    except Exception as e:
        print(f" Error: {e}")