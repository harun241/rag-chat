from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
from dotenv import load_dotenv

load_dotenv()

def ingest():
    loader = DirectoryLoader("data/", glob="*.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="db"
    )

    vectordb.persist()
    print("Vector DB created successfully!")

if __name__ == "__main__":
    ingest()
