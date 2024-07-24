import os
from openai import AzureOpenAI
from qdrant_client import QdrantClient

from dotenv import load_dotenv
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    api_version=os.getenv('OPENAI_API_VERSION'),
    azure_endpoint=os.getenv('OPENAI_API_ENDPOINT')
)

connection = QdrantClient(
    url=os.getenv('QDRANT_URL'), 
    api_key=os.getenv('QDRANT_API_KEY'),
)

deployment_name = os.getenv('DEPLOYMENT_NAME')
embedding_name = os.getenv('EMBEDDING_NAME')

def get_answer_from_kb(query: str):
    embeddings = client.embeddings.create(input = query, model=embedding_name).data[0].embedding
    search_result = connection.search(
        collection_name="db",
        query_vector=embeddings,
        limit=5
    )
    examples=""
    for result in search_result:
        examples += result.payload['text'] + "\n"
    system_prompt = """
    ###
    You are a helpful AI assistant called 'MLSAide' who is an expert at answering questions about the Microsoft Learn Student Ambassadors program. You are here to help students with their queries and provide them with accurate information. You were created by Mohammed Raza Syed who is a Beta Microsoft Learn Student Ambassador and part of MLSA community for more than 1.5 years. You are provided with the following question and context to help the student with their query. Use context to provide accurate and relevant information to the student.
    
    ###
    Question: {0}
    Context: {1}
    
    ###
    Below are the rules you must follow while answering the question:
    
    - Now your task is to answer the question to the best of your ability. Remember to provide accurate, relevant and helpful information to the student. Do not overwhelm the students with additional information that is not relevant to the question. Be concise and to the point.
    
    - If you are unsure about the answer, then only you can let them know that you are unable to answer the question and should verify the information from SA-Handbook: https://stdntpartners.sharepoint.com/sites/SAProgramHandbook.
        
    - At the end of your response in one sentence respond that you are happy to help with any other questions.
    
    - Do not repeat your answers.
    
    - Take only relevant example from the Context and respond with a relevant answer.
    
    - If the user concludes the conversation, simply answer with a goodbye message.
    
    - If you are asked anything unrelated to the Microsoft Learn Student Ambassadors program and Context provided such as code, explanation etc. not related to MLSA, respond that you are unable to answer the question.
    """

    # print(system_prompt)
    response = client.completions.create(
        model=deployment_name,
        prompt=system_prompt.format(query, examples),
        temperature=0.6,
        max_tokens=1024,
    )
    return (response.choices[0].text.strip())
# x = get_answer_from_kb(input("Enter your query: "))
# print(x)