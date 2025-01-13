import chromadb
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter


# Initialize Chroma client with persistent storage
client = chromadb.Client(settings=chromadb.config.Settings(
    persist_directory="./"  # Directory to store embeddings
))

persist_dir = "vectorstore_email_db"

# Choose the collection name and set a path for persistent storage
collection = client.create_collection(name="emails_collection")
# Initialize OpenAI Embeddings

def store_to_chroma(emails_list):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250,  # Split the text into chunks of 250 characters
        chunk_overlap=50  # Each chunk will overlap by 50 characters
    )
    doc_splits = text_splitter.split_documents(emails_list)
    embedding = GPT4AllEmbeddings()

    # Add the email document chunks to the "vector store"
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        embedding=embedding,
        persist_directory=persist_dir
    )
    return vectorstore
