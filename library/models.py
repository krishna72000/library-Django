from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils.translation import gettext as _

class Book(models.Model):
    id = models.AutoField(_("id"),primary_key=True)
    title = models.CharField(_("title"), max_length=255)
    authors = models.CharField(_("authors"), max_length=255)
    average_rating = models.FloatField(_("average rating"))
    isbn = models.CharField(_("isbn"), max_length=150)
    language_code = models.CharField(_("language code"), max_length=10)
    num_pages = models.IntegerField(_("number of pages"))
    publication_date = models.CharField(_("publication date"), max_length=15)
    publisher = models.CharField(_("publisher"), max_length=150)
    image_url = models.CharField(_("image_url"), max_length=250)
    category = models.CharField(_("category"), max_length=50)
    
    def __str__(self):
        return str(self.title) + " ["+str(self.isbn)+']'
        
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'

class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=100, blank=True)
    book_id = models.CharField(max_length=100, blank=True) 
    # book_id = models.ForeignKey(Book,on_delete=models.CASCADE)

def expiry():
    return datetime.today() + timedelta(days=14)
class IssuedBook(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=100, blank=True) 
    book_id = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)

    def __str__(self):
        return str(self.student_id) + " ["+str(self.book_id)+']' + " ["+str(self.issued_date)+']'
