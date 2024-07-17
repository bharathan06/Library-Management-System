from django.db import models

# Create your models here.

#Book model. 
class Book(models.Model):
    title= models.CharField(max_length=100)
    author= models.CharField(max_length=50)
    isbn= models.CharField(max_length=13, unique=True)
    categories= models.CharField(max_length=50)
    published_date= models.DateField()

    def __str__(self):
        return self.title 
    


#Readers model. 
class Readers(models.Model):
    user_id= models.CharField(max_length=10, unique=True)
    email= models.EmailField(max_length = 254)
    fname= models.CharField(max_length=50)
    lname= models.CharField(max_length=50)
    phone= models.CharField(max_length=15)


    def __str__(self):
        return self.user_id 
    

#Reserve/Return RP model.
class Reserve_return(models.Model):
    return_date= models.DateField()
    due_date= models.DateField()
    books= models.ForeignKey(Book, on_delete=models.CASCADE)
    reader= models.ForeignKey(Readers, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reader} - {self.books}"
    
