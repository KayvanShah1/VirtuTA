import streamlit as st
from langchain_google_vertexai import VertexAIEmbeddings
from settings import config


class EmbeddingClient:
    """
    Initialize the EmbeddingClient class to connect to Google Cloud's VertexAI for text embeddings.

    Parameters:
    - model_name: A string representing the name of the model to use for embeddings.
    - project: The Google Cloud project ID where the embedding model is hosted.
    - location: The location of the Google Cloud project, such as 'us-central1'.
    """

    def __init__(self, model_name, project, location):
        self.client = VertexAIEmbeddings(
            model_name=model_name,
            project=project,
            location=location,
            credentials=config.CREDENTIALS,
        )

    def embed_query(self, query):
        """
        Uses the embedding client to retrieve embeddings for the given query.

        :param query: The text query to embed.
        :return: The embeddings for the query or None if the operation fails.
        """
        vectors = self.client.embed_query(query)
        return vectors

    def embed_documents(self, documents):
        """
        Retrieve embeddings for multiple documents.

        :param documents: A list of text documents to embed.
        :return: A list of embeddings for the given documents.
        """
        try:
            return self.client.embed_documents(documents)
        except AttributeError:
            print("Method embed_documents not defined for the client.")
            return None


if __name__ == "__main__":
    model_name = "textembedding-gecko@003"
    project = config.PROJECT_ID
    location = config.PROJECT_LOCATION

    embedding_client = EmbeddingClient(model_name, project, location)
    vectors = embedding_client.embed_query("Hello World!")
    if vectors:
        st.write(vectors)
        print(vectors)
        st.write("Successfully used the embedding client!")
        print("Successfully used the embedding client!")
