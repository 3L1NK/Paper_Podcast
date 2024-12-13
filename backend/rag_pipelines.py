from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def summarize_with_rag(document_text):
    # Split the text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(document_text)

    # Create embeddings and store in FAISS
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(chunks, embeddings)

    # Run RAG-based summarization
    retriever = db.as_retriever()
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=retriever)
    return qa_chain.run("Summarize this document in a podcast-friendly format")
