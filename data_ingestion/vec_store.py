import os
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch

# from langchain_core.runnables import RunnablePassthrough
from embedding import EmbeddingClient

from settings import config

from db import MONGODB_COLLECTION, ATLAS_VECTOR_SEARCH_INDEX_NAME

# Load the PDF
# loader = PyPDFLoader("https://arxiv.org/pdf/2303.08774.pdf")
path = os.path.relpath(
    "~\\OneDrive - University of Southern California\\Books\\References\\"
    "3rd Edition Ethem Alpaydin-Introduction to Machine Learning-The MIT Press (2014).pdf"
)
loader = PyPDFLoader(path)
docs = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150))

# for doc in docs[:10]:
#     print(doc)

model_name = "textembedding-gecko@003"
project = config.PROJECT_ID
location = config.PROJECT_LOCATION
EMBEDDING_QPM = 1200
EMBEDDING_NUM_BATCH = 5

# insert the documents in MongoDB Atlas with their embedding
vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=EmbeddingClient(
        model_name="textembedding-gecko@latest",
        project=config.PROJECT_ID,
        location=config.PROJECT_LOCATION,
        requests_per_minute=EMBEDDING_QPM,
        num_instances_per_batch=EMBEDDING_NUM_BATCH,
    ),
    collection=MONGODB_COLLECTION,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)
