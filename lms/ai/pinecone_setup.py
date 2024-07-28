import os
from myapp.models import Book
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from pinecone import QueryRequest
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



#Initialize the environment. 
api_key = os.getenv('PINECONE_API_KEY')
if not api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set")

environment = os.getenv('PINECONE_ENVIRONMENT', 'us-west1-gcp')
pc = Pinecone(api_key=api_key, environment=environment)

index_name = "library-index"


#Check if an index exists and delete it.
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)


#Creating a serverless index 
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
index = pc.Index(index_name)

#Used to find the semantic meaning of the title of the book so it can be related to.
model = SentenceTransformer('all-MiniLM-L6-v2')

books = Book.objects.all()
vectors = []

#The data from backend is converted into vectors and upserted. 
for book in books: 
    vector= model.encode(book.title)            #Returns numerical vector values that represent the semantic meaning.
    vectors.append({"id": str(book.id), "values": vector.tolist()})

#Vectors are upserted. 
index.upsert(vectors=vectors, namespace="ns1")


def serialize_book(book):
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,  
    }

#Function to convert into a vector. 
def embed_text(text):
    return model.encode(text).tolist()

def search(query, top_k=5):
    #Query is converted into a vector. 
    query_vector = embed_text(query)

    
    #Query is made at this point. 
    query_response = index.query(
        namespace="ns1",
        vector=query_vector, 
        top_k=top_k,
        include_values=True
    )
    
    #Displaying the results. 
    matches_list = []
    for match in query_response.get('matches', []):
        try:
            # Retrieve the book instance for the matched ID
            book_instance = get_object_or_404(Book, id=match['id'])
            
            # Serialize the book metadata
            serialized_book = serialize_book(book_instance)

            matches_list.append({
                'id': match['id'],
                'score': match['score'],
                'values': serialized_book  # Include the serialized book metadata here
            })
        except Exception as e:
            print(f"Error processing ID {match['id']}: {e}")

    results = {
        'matches': matches_list,
        'metadata': query_response.get('metadata', {})  # Metadata from Pinecone query response
    }

    # Return a JSON response
    return JsonResponse(results)

    return query_response
