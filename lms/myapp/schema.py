from ninja import Schema
from datetime import date 

#Request schema for Books.
class BookSchema(Schema):
    id : int 
    title : str
    author : str
    isbn : int 
    categories : str
    published_date : date 

#Response schema for books.
class CreateBookSchema(Schema):
    title : str
    author : str
    isbn : int 
    categories : str
    published_date : date 