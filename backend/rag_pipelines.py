from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain_core.documents import Document  # Correct import
from dotenv import load_dotenv
from prompts import PODCAST_PROMPT
import os

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def summarize_with_rag(text):
    try:
        if not text:
            return "No text provided for summarization."

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        texts = text_splitter.split_text(text)

        documents = [Document(page_content=t) for t in texts]

        db = FAISS.from_documents(documents, embeddings)
        retriever = db.as_retriever()

        qa_chain = retriever | OpenAI(model="gpt-3.5-turbo", temperature=0.3)

        query = PODCAST_PROMPT
        result = qa_chain.run(query)

        print("Generated Summary:", result)
        return result

    except Exception as e:
        print("Error in RAG Pipeline:", e)
        return str(e)
