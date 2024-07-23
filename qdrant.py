from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
import uuid
from tqdm import tqdm
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    api_version=os.getenv('OPENAI_API_VERSION'),
    azure_endpoint=os.getenv('OPENAI_API_ENDPOINT')
)

embedding_name = os.getenv('EMBEDDING_NAME')

def read_data_from_pdf():
    pdf_path = './Final.pdf'
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, length_function=len)
    chunks = text_splitter.split_text(text)
    return chunks

def get_embedding(text_chunks):
    points = []
    for idx, chunk in enumerate(tqdm(text_chunks, desc="Processing Chunks")):
        embeddings = client.embeddings.create(input=chunk, model=embedding_name).data[0].embedding
        point_id = str(uuid.uuid4())
        points.append(PointStruct(id=point_id, vector=embeddings, payload={"text": chunk}))
    return points

connection = QdrantClient(
    url=os.getenv('QDRANT_URL'), 
    api_key=os.getenv('QDRANT_API_KEY'),
)


connection.create_collection(
    collection_name="db",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
)

def insert_data(get_points):
    operation_info = connection.upsert(
        collection_name="db",
        wait=True,
        points=get_points
    )

def main():
    get_raw_text = read_data_from_pdf()
    chunks = get_text_chunks(get_raw_text)
    vectors = get_embedding(chunks)

    insert_data(vectors)

if __name__ == "__main__":
    main()
info = connection.get_collection(collection_name="test1")
print(info)