import json
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from myapp.models import Book 



class Command(BaseCommand):
    help = 'Populate book details from a JSON file'

    def handle(self,*args,**kwargs):
        datafile= settings.BASE_DIR / 'data' / 'library_books.json'
        assert datafile.exists() 

        with open(datafile, 'r') as f:
            data= json.load(f)

        for book in data:
            book['published_date']= datetime.strptime(book['published_date'], "%Y-%m-%d").date()


        books = [Book(**book) for book in data]

        Book.objects.bulk_create(books)