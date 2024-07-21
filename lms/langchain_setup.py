
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
import os
from pinecone_setup import index_name

OPENAI_API_KEY = os.getenv('sk-proj-PuHM29oRWPGtNyZSAzNuT3BlbkFJhMDw0liMVWI5UOaLhGEd')

model_name = 'text-embedding-ada-002'

embeddings = OpenAIEmbeddings(model=model_name, api_key=os.getenv('OPENAI_API_KEY'))

text_field = "text"
vectorstore = Pinecone(index_name, embeddings.embed_query,text_field)
