# from unstructured.partition.pdf import partition_pdf
import io
import base64
import fitz
from PIL import Image
from pdf2image import convert_from_path
from tqdm import tqdm
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chat_models import ChatVertexAI
from langchain.prompts import PromptTemplate
from langchain.llms import VertexAI
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnableLambda
import os

def extract_images(pdf_path, output_path):
    # pdf_path = "data/ML textbook 1.pdf"
    pdf = fitz.open(pdf_path)
    # output_path = "pdf_images/"
    vector_drawings = []
    count = 1
    for pg in tqdm(range(len(pdf))):
        page = pdf[pg]
        images = page.get_images(full=True)

        vector_drawings.append(pdf[pg].get_drawings())

        for annot in page.annots():
            print('annot type:', annot)
            if (annot.type[0] == 4):
                print('polygon found')
                points = annot.vertices
                x_coords = [pt.x for pt in points]
                y_coords = [pt.y for pt in points]
                bbox = (min(x_coords), min(y_coords), max(x_coords), max(y_coords))
                image = page.get_pixmap(matrix=fitz.Matrix(), clip=bbox)
                image.save(output_path + "vector_image_{}".format(annot.number) + ".jpg")

        for index, image in enumerate(images):
            xref = image[0]
            base_image = pdf.extract_image(xref)
            image_in_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_in_bytes))
            image.save(output_path + "image_{}".format(count) + ".jpg")
            count += 1

def encode_image(image_path):
    """Getting the base64 string"""
    print('Encoding images')
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_summarize(img_base64, prompt):
    """Make image summary"""
    model = ChatVertexAI(model_name="gemini-pro-vision", max_output_tokens=1024)

    msg = model(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
                    },
                ]
            )
        ]
    )
    print('image summary:', msg.content)
    return msg.content

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
    prompt = """You are an assistant tasked with summarizing images for retrieval. \
    These summaries will be embedded and used to retrieve the raw image. \
    Give a concise summary of the image that is well optimized for retrieval."""

    # Apply to images
    for img_file in sorted(os.listdir(path)):
        print('img file:', img_file)
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            img_base64_list.append(base64_image)
            image_summaries.append(image_summarize(base64_image, prompt))

    return img_base64_list, image_summaries

# fpath = "./"
# Image summaries
# img_base64_list, image_summaries = generate_img_summaries(fpath)

def main():

    pdf_path = "data/ML textbook 1.pdf"
    output_path = "pdf_images/"
    # extract_images(pdf_path, output_path)

    img_base64_list, image_summaries = generate_img_summaries("pdf_images")

    print('image summaries:', image_summaries)



    # print('vector drawings:', vector_drawings)
    # extract_images(pdf_path, output_path)

main()