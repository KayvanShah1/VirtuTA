import time
from typing import List
from langchain_google_vertexai import VertexAIEmbeddings
from settings import config


def rate_limit(max_per_minute):
    period = 60 / max_per_minute
    print("Waiting")
    while True:
        before = time.time()
        yield
        after = time.time()
        elapsed = after - before
        sleep_time = max(0, period - elapsed)
        if sleep_time > 0:
            print(".", end="")
            time.sleep(sleep_time)


class EmbeddingClient:
    """
    Initialize the EmbeddingClient class to connect to Google Cloud's VertexAI for text embeddings.

    Parameters:
    - model_name: A string representing the name of the model to use for embeddings.
    - project: The Google Cloud project ID where the embedding model is hosted.
    - location: The location of the Google Cloud project, such as 'us-central1'.
    - requests_per_minute: Maximum number of requests per minute.
    - num_instances_per_batch: Number of instances (texts) per batch.
    """

    def __init__(
        self, model_name: str, project: str, location: str, requests_per_minute: int, num_instances_per_batch: int
    ):
        self.requests_per_minute = requests_per_minute
        self.num_instances_per_batch = num_instances_per_batch
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

    def embed_documents(self, texts: List[str]):
        limiter = rate_limit(self.requests_per_minute)
        results = []
        docs = list(texts)

        while docs:
            # Working in batches because the API accepts maximum 5
            # documents per request to get embeddings
            head, docs = (
                docs[: self.num_instances_per_batch],
                docs[self.num_instances_per_batch :],
            )
            chunk = self.client.get_embeddings(head)
            results.extend(chunk)
            next(limiter)

        return [r.values for r in results]
