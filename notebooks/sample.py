import base64
import os
import sys

from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI

NOTEBOOKS_DIR = os.path.dirname(__file__)
REPO_DIR = os.path.dirname(NOTEBOOKS_DIR)

sys.path.append(REPO_DIR)

from data_ingestion.settings import config


def encode_image(image_path):
    """Getting the base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def image_summarize(img_base64, prompt):
    """Make image summary"""
    llm = ChatVertexAI(model_name="gemini-pro-vision", credentials=config.CREDENTIALS)

    msg = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ]
    )

    return llm.invoke([msg]).content


def generate_img_summaries(path):
    """
    Generate summaries and base64 encoded strings for images
    path: Path to list of .jpg files extracted by Unstructured
    """

    # Store base64 encoded images
    img_base64_list = []

    # Store image summaries
    image_summaries = []

    # Prompt
    prompt = """You are an teaching assistant tasked with summarizing images for retrieval. \
    These summaries will be embedded and used to retrieve the raw image. \
    Give a detailed summary of the image that is well optimized for retrieval."""

    # Apply to images
    for img_file in sorted(os.listdir(path)):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            img_base64_list.append(base64_image)
            image_summaries.append(image_summarize(base64_image, prompt))

    return img_base64_list, image_summaries


_, sumy = generate_img_summaries("./notebooks")

for i, j in list(zip(_, sumy)):
    print(j)
