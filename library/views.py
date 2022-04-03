import codecs
import csv

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from library.forms import IssueBookForm
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from .forms import IssueBookForm
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from datetime import date
from django.contrib.auth.decorators import login_required
fs = FileSystemStorage(location='tmp/')

def index(request):
    return render(request, "index.html")

@login_required(login_url = '/admin_login')
def upload_book(request):
    if request.method == "POST":
        file = request.FILES["csvbook"]
        content = file.read()  # these are bytes
        file_content = ContentFile(content)
        file_name = fs.save(
            "_tmp.csv", file_content
        )
        tmp_file = fs.path(file_name)

        csv_file = open(tmp_file, errors="ignore")
        reader = csv.reader(csv_file)
        next(reader)
        
        book_list = []
        for id_, row in enumerate(reader):
            (
                id,
                title,
                authors,
                average_rating,
                isbn,
                language_code,
                num_pages,
                publication_date,
                category,
                publisher,
                image_url,
            ) = row
            book_list.append(
                Book(
                    title=title,
                    authors=authors,
                    isbn=isbn,
                    language_code=language_code,
                    average_rating=average_rating,
                    num_pages=num_pages,
                    publication_date=publication_date,
                    publisher=publisher,
                    category=category,
                    image_url=image_url
                )
            )
        Book.objects.bulk_create(book_list)
        alert = True
        return render(request, "add_ubook.html", {'alert':alert,'title':'Upload Book'})
    return render(request, "add_ubook.html",{'title':'Upload Book'})

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['authors']
        isbn = request.POST['isbn']
        category = request.POST['category']
        language_code = request.POST['language_code']
        average_rating = request.POST['average_rating']
        num_pages = request.POST['num_pages']
        publication_date = request.POST['publication_date']
        publisher = request.POST['publisher']
        image_url = request.POST['image_url']
        books = Book.objects.create(
                    title=title,
                    authors=author,
                    isbn=isbn,
                    language_code=language_code,
                    average_rating=average_rating,
                    num_pages=num_pages,
                    publication_date=publication_date,
                    publisher=publisher,
                    category=category,
                    image_url=image_url
                )
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert,'title':'Add Book'})
    return render(request, "add_book.html",{'title':'Add Book'})

@login_required(login_url = '/admin_login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books':books,'title':'Book List'})

@login_required(login_url = '/admin_login')
def view_students(request):
    # User.objects.all().delete() 
    students = Student.objects.all()
    return render(request, "view_students.html", {'students':students,'title':'Student List'})

@login_required(login_url = '/admin_login')
def issue_book(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.student_id = request.POST['name2']
            obj.isbn = request.POST['isbn2']
            obj.save()
            alert = True
            return render(request, "issue_book.html", {'obj':obj, 'alert':alert})
    return render(request, "issue_book.html", {'form':form,'title':"Issue Books"})

@login_required(login_url = '/admin_login')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.Student.objects.filter(user=i.student_id))
        j=0
        for l in books:
            t=(students[j].user,students[j].user_id,books[j].name,books[j].isbn,i.issued_date,i.expiry_date,fine,i.id)
            j=j+1
            details.append(t)
    return render(request, "view_issued_book.html", {'details':details,'title':"View Issued Books"})

@login_required(login_url = '/admin_login')
def delete_issue(request, myid):
    books = IssuedBook.objects.filter(id=myid)
    books.delete()
    return redirect("/view_issued_book")

@login_required(login_url = '/admin_login')
def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")

@login_required(login_url = '/admin_login')
def delete_student(request, myid):
    students = Student.objects.filter(id=myid)
    # students.user.delete()
    students.delete()
    return redirect("/view_students")


@login_required(login_url = '/student_login')
def student_books_search(request):
    books = Book.objects.all()
    return render(request, "student_books_search.html", {'books':books,'title':"Book Search"})


@login_required(login_url = '/student_login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    for i in issuedBooks:
        days=(date.today()-i.issued_date)
        d=days.days
        fine=0
        if d>15:
            day=d-14
            fine=day*5
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t=(request.user.id, request.user.get_full_name, book.name,book.author,issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
            li1.append(t)
    return render(request,'student_issued_books.html',{'li1':li1,'title':"Issued Books"})

@login_required(login_url = '/student_login')
def student_add_favourite(request):
    # Favourite.objects.all().delete()
    book_id = request.GET['book_id']
    Favourite.objects.filter(student_id=request.user.id,book_id=book_id).delete()
    Favourite.objects.create(student_id=request.user.id,book_id=book_id)
    return redirect("/student_books_search")

@login_required(login_url = '/student_login')
def student_delete_favourite(request):
    book_id = request.GET['book_id']

    Favourite.objects.filter(student_id=request.user.id,id=book_id).delete()
    return redirect("/student_favourite_book")

def student_favourite_book(request):
    
    f_book = Favourite.objects.filter(student_id=request.user.id)
    li1 = []
    for i in f_book:
        iBooks = Book.objects.filter(id=i.book_id)
        for book in iBooks:
            t=(book.title,book.author,i.id)
            li1.append(t)
    return render(request, "student_favourite_book.html",{'li1':li1, 'title':'Favourite Books'})

@login_required(login_url = '/student_login')
def profile(request):
    return render(request, "profile.html",{'title':'Profile'})

@login_required(login_url = '/student_login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']

        student.user.email = email
        student.phone = phone
        student.branch = branch
        student.classroom = classroom
        student.roll_no = roll_no
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert':alert,'title':"Edit Profile"})
    return render(request, "edit_profile.html",{'title':"Edit Profile"})


@login_required(login_url = '/student_login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert':alert,'title':"Change Password"})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong':currpasswrong,'title':"Change Password"})
        except:
            pass
    return render(request, "change_password.html",{'title':"Change Password"})

def student_registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        branch = request.POST['branch']
        classroom = request.POST['classroom']
        roll_no = request.POST['roll_no']
        password = request.POST['password']
      
        user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
        student = Student.objects.create(user=user, phone=phone, branch=branch, classroom=classroom,roll_no=roll_no)
        student.save()
        user.save()
        alert = True
        return render(request, "student_registration.html", {'alert':alert,'title':"Register Student"})
    return render(request, "student_registration.html",{'title':"Register Student"})

def student_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/profile")
        else:
            alert = True
            return render(request, "student_login.html", {'alert':alert,'title':"Student Login"})
    return render(request, "student_login.html",{'title':"Student Login"})

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/view_students")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert':alert,'title':"Admin Login"})
    return render(request, "admin_login.html",{'title':"Admin Login"})

def Logout(request):
    logout(request)
    return redirect ("/")