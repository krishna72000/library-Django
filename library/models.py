from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'

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

def expiry():
    return datetime.today() + timedelta(days=14)
class IssuedBook(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=100, blank=True) 
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
