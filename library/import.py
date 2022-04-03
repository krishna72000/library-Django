# open file & create csvreader
import csv
# from . import forms, models
# import the relevant model
from models import Book
products=[]


with open("books.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
            book =Book.objects.create(id = row[0],title =row[10],author = row[8],isbn =row[7],category =row[9])
            book.save()
#ensure fields are named~ID,Product_ID,Name,Ratio,Description
#concatenate name and Product_id to make a new field a la Dr.Dee's answer
