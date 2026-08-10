from langchain_community.vectorstores import Chroma
from langchain_mistralai import MistralAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

from langchain_core.documents import Document

docs = [
    Document(page_content="Python is a easy, readable programming language.", metadata={"source": "Python_book"}),
    Document(page_content="Pandas is a fast tool for data rows and columns.", metadata={"source": "Datascience_book"}),
    Document(page_content="Neural Network (NN) is a brain-like layers for deep learning.", metadata={"source": "Deeplearning_book"})
]

embedding_model = MistralAIEmbeddings()

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="chroma-db"
)

result = vectorstore.similarity_search("which is a easy programming language?", k=2)

for r in result:
    print(r.page_content)
    print(r.metadata)

retriever = vectorstore.as_retriever()

docs = retriever.invoke("Explain nn?")

for d in docs:
    print(d.page_content)