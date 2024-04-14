from typing import List
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.vision_models import MultiModalEmbeddingModel, Image, MultiModalEmbeddingResponse
from PyPDF2 import PdfReader

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings, huggingface, huggingface_hub

import fitz

def get_pdf_images(pdf):

    images = []

    for page in pdf:

        images_in_page = page.get_images()

        if(images_in_page):
            for image_index, img in enumerate(images_in_page):
                xref = img[0]
                image = pdf.extract_image(xref)
                image_in_bytes = image["image"]
                # images.append(image_in_bytes)
                formatted_image = Image(image_in_bytes)
                images.append(formatted_image)

    return images

def get_pdf_text(pdf):

    text = ""
    for page in pdf:
        text += page.get_text()
    # for page in pdf_docs.pages:
    #     text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=100, length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

# def embed_text(
#     texts: List[str] = ["banana muffins? ", "banana bread? banana muffins?"],
#     task: str = "RETRIEVAL_DOCUMENT",
#     model_name: str = "textembedding-gecko@003",
# ) -> List[List[float]]:

def embed_text(
        texts,
        task: str = "RETRIEVAL_DOCUMENT",
        # model_name: str = "textembedding-gecko@003",
        model_name: str = "textembedding-gecko@003",

) -> List[List[float]]:


    """Embeds texts with a pre-trained, foundational model."""
    model = TextEmbeddingModel.from_pretrained(model_name)
    inputs = [TextEmbeddingInput(text, task) for text in texts]
    embeddings = model.get_embeddings(inputs)
    return [embedding.values for embedding in embeddings]

def embed_images(images,
                 model_name: str = "multimodalembedding",
                 ):
    model = MultiModalEmbeddingModel.from_pretrained(model_name)
    # test_image = images[0]
    img_embeddings = []
    for i in images:
        img_embedding = model.get_embeddings(image=i)
        img_embeddings.append(img_embedding.image_embedding)
    return img_embeddings


def main():

    # pdf = PdfReader("data/DSCI 552 Lecture 11.pdf")
    pdf = fitz.open("data/DSCI 552 Lecture 11.pdf")

    # print('images:', images[0])

    # print('pdf:', pdf)
    text = get_pdf_text(pdf)
    # print('text:', text)
    chunks = get_text_chunks(text)
    embeddings = embed_text(chunks)
    print('len chunks[0]', len(chunks[0]))
    print('text embeddings:', len(embeddings[0]))

    images = get_pdf_images(pdf)
    image_embeddings = embed_images(images)
    print('image embeddings:', len(image_embeddings[0]))


main()