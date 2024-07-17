from ninja import NinjaAPI
from .models import Book
from .schema import request_book, create_book_schema
from django.shortcuts import get_object_or_404

api = NinjaAPI()

#Api handles get requests to /books. 
@api.get("/books", response=list[request_book])
def list_books(request):
    books= Book.objects.all()
    return books

#API handles post requests to /books. 
@api.post("/books", response=create_book_schema)
def create_book(request,payload: create_book_schema):
    book = Book.objects.create(**payload.dict())
    return book



