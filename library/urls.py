from django.urls import path,re_path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("book_list", views.book_list, name="book_list"),
    path("upload_book/", views.upload_book, name="upload_book"),
    path("add_book/", views.add_book, name="add_book"),
    # path("view_books/", views.view_books, name="view_books"),
    re_path(r'^getbooks/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.getbooks,name='getbooks'),
    path("view_students/", views.view_students, name="view_students"),
    path("issue_book/", views.issue_book, name="issue_book"),
    path("view_issued_book/", views.view_issued_book, name="view_issued_book"),
    path("recommended/", views.recommended, name="recommended"),
    path("student_books_list/", views.student_books_list, name="student_books_list"),
    re_path(r'^student_books_search/(?:(?P<pk>\d+)/)?(?:(?P<action>\w+)/)?', views.student_books_search,name='student_books_search'),
    path("student_issued_books/", views.student_issued_books, name="student_issued_books"),
    path("student_favourite_book/", views.student_favourite_book, name="student_favourite_book"),
    path("student_add_favourite/", views.student_add_favourite, name="student_add_favourite"),
    path("student_delete_favourite/", views.student_delete_favourite, name="student_delete_favourite"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

    path("student_registration/", views.student_registration, name="student_registration"),
    path("change_password/", views.change_password, name="change_password"),
    path("student_login/", views.student_login, name="student_login"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("logout/", views.Logout, name="logout"),

    path("delete_issue/<int:myid>/", views.delete_issue, name="delete_issue"),
    path("delete_book/<int:myid>/", views.delete_book, name="delete_book"),
    path("delete_student/<int:myid>/", views.delete_student, name="delete_student"),
]