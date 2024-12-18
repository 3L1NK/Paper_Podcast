from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os

load_dotenv()

# Access API key
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def summarize_with_rag(text):
    try:
        # 1. Split the input text
        print("Input Text:", text[:500])  # Print the first 500 characters
        if not text:
            return "No text provided for summarization."

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_text(text)
        print("Text Chunks Created:", len(texts))  # Debugging

        # 2. Convert to documents
        documents = [Document(page_content=t) for t in texts]

        # 3. Initialize Embeddings and Vectorstore
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(documents, embeddings)
        print("FAISS Vectorstore Created Successfully")

        # 4. Initialize RAG Chain
        retriever = db.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(model="gpt-3.5-turbo", temperature=0),
            retriever=retriever,
            chain_type="stuff"
        )

        # 5. Ask a summary question
        query = "Summarize the following text into a concise podcast script."
        print("RAG Query:", query)

        result = qa_chain.run(query)
        print("Generated Summary:", result)  # Print the result
        return result

    except Exception as e:
        print("Error in RAG Pipeline:", e)
        return str(e)

