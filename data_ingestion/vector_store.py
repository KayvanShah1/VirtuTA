import io
import os
import tempfile
from pprint import pprint

from db import ATLAS_VECTOR_SEARCH_INDEX_NAME, MONGODB_COLLECTION
from embedding import EmbeddingClient
from langchain_community.document_loaders.pdf import PyMuPDFLoader, PyPDFLoader
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image
from pypdf import PdfReader
from settings import config
from tqdm import tqdm

# Load the PDF
# loader = PyPDFLoader("https://arxiv.org/pdf/2303.08774.pdf")
path = os.path.relpath(
    "c:\\Users\\shahk\\OneDrive - University of Southern California\\Books\\References\\"
    "3rd Edition Ethem Alpaydin-Introduction to Machine Learning-The MIT Press (2014).pdf"
)

# loader = PyMuPDFLoader(path)
# # docs = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150))
# docs = loader.load()

# for doc in docs[:30]:
#     print(doc.json())

with tempfile.TemporaryDirectory() as temp_dir:
    reader = PdfReader(path)

    for i in tqdm(range(len(reader.pages))):
        page = reader.pages[i]

        if page.images:
            for j, img in enumerate(page.images):
                print(i + 1, j + 1, img.name, img.image)
                image = Image.open(io.BytesIO(img.data))
                image.show()
                # rgb_image = image.convert("RGB")
                image_path = os.path.join(temp_dir, f"page{i}_img{j}.png")
                image.save(image_path)

# model_name = "textembedding-gecko@003"
# project = config.PROJECT_ID
# location = config.PROJECT_LOCATION
# EMBEDDING_QPM = 1200
# EMBEDDING_NUM_BATCH = 5

# # insert the documents in MongoDB Atlas with their embedding
# vector_search = MongoDBAtlasVectorSearch.from_documents(
#     documents=docs,
#     embedding=EmbeddingClient(
#         model_name="textembedding-gecko@latest",
#         project=config.PROJECT_ID,
#         location=config.PROJECT_LOCATION,
#         requests_per_minute=EMBEDDING_QPM,
#         num_instances_per_batch=EMBEDDING_NUM_BATCH,
#     ),
#     collection=MONGODB_COLLECTION,
#     index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
# )
