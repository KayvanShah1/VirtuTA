from pprint import pprint

from db import ATLAS_VECTOR_SEARCH_INDEX_NAME, MONGODB_COLLECTION
from embedding import EmbeddingClient
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_vertexai import ChatVertexAI, VertexAI
from langchain_mongodb import MongoDBAtlasVectorSearch
from settings import config

model_name = "textembedding-gecko@003"
project = config.PROJECT_ID
location = config.PROJECT_LOCATION

# Embedding
EMBEDDING_QPM = 1200
EMBEDDING_NUM_BATCH = 5


embedding = EmbeddingClient(
    model_name="textembedding-gecko@003",
    project=config.PROJECT_ID,
    location=config.PROJECT_LOCATION,
    requests_per_minute=EMBEDDING_QPM,
    num_instances_per_batch=EMBEDDING_NUM_BATCH,
)

vector_search = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION, embedding=embedding, index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME
)

# qa_retriever = vector_search.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 25},
# )


# query = "What is linear regression?"

# results = vector_search.similarity_search_with_score(query=query, k=5)
# print(results)

# # Display results
# for result in results:
#     print(result)


# Instantiate Atlas Vector Search as a retriever
retriever = vector_search.as_retriever(search_type="similarity", search_kwargs={"k": 10, "score_threshold": 0.75})

# Define a prompt template
template = """

Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""
custom_rag_prompt = PromptTemplate.from_template(template)

llm = VertexAI(model_name="gemini-pro", max_output_tokens=2048, temperature=0.2, top_p=0.8, top_k=40, streaming=True)

# chat = ChatVertexAI()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# Construct a chain to answer questions on your data
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

# Prompt the chain
question = "What is linear regression? What does it represent mathematically? In which doesn't this work? What are the other choices?"
answer = rag_chain.invoke(question)

print("Question: " + question)
print("Answer: " + answer)

# # Return source documents
# documents = retriever.get_relevant_documents(question)
# print("\nSource documents:")
# pprint(documents)
