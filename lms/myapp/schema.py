from ninja import Schema
from datetime import date 

#Request schema for Books.
class request_book(Schema):
    title : str
    author : str
    isbn : int 
    categories : str
    published_date : date 

#Response schema for books.
class create_book_schema(Schema):
    title : str
    author : str
    isbn : int 
    categories : str
    published_date : date 