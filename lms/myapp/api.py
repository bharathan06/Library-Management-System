from ninja import NinjaAPI
from .models import Book
from .schema import BookSchema, CreateBookSchema
from django.shortcuts import get_object_or_404
from pinecone_setup import search

api = NinjaAPI()




#Api handles get requests to /books. 
@api.get("/books", response=list[BookSchema])
def list_books(request):
    books= Book.objects.all()
    return books

#Everything below this is CRUD type of API calls 

#API handles creation of a book. 
@api.post("/books", response=BookSchema)
def create_book(request,payload: CreateBookSchema):
    book = Book.objects.create(**payload.dict())
    return book


#API handles the retrieval of a book. 
@api.get("/books/{book_id}", response=BookSchema)
def get_book(request, book_id: int):
    book= get_object_or_404(Book, id=book_id)
    return book


#API handles the updation of a book. 
@api.post("/books/{book_id}", response=BookSchema)
def update_book(request, book_id: int,payload: CreateBookSchema):
    book= get_object_or_404(Book, id=book_id)
    for attr,value in payload.dict().items():
        setattr(book, attr, value)
    book.save()
    return book


#API handles the deletion of a book.
@api.delete("/books/{book_id}")  
def delete_book(request, book_id : int):
    book= get_object_or_404(Book, id=book_id)
    book.delete()
    return {"Success" : True} 


from langchain_setup import vectorstore



#This API handles the langchain + Pinecone query in natural language.
@api.get("/search")
def search_books(request, query : str):
    results = search(query)
    return results