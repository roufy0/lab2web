from django.urls import path
from . import views
<<<<<<< HEAD

urlpatterns = [
path(''
, views.index, name= "books.index"),
path('list_books/', views.list_books, name= "books.list_books"),
path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
path('aboutus/', views.aboutus, name="books.aboutus"),
=======
urlpatterns = [
    path('', views.index),
    path('index2/<int:val1>/', views.index2),
    path('<int:bookId>', views.viewbook),
>>>>>>> d6335cfb46e8932c71840fbd7b5753783f956a79
]
