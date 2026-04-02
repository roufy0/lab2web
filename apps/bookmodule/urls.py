from django.urls import path
from . import views

urlpatterns = [
path(''
, views.index, name= "books.index"),
path('list_books/', views.list_books, name= "books.list_books"),
path('<int:bookId>/', views.viewbook, name="books.view_one_book"),
path('aboutus/', views.aboutus, name="books.aboutus"),
path('html5/links', views.links_page, name="books.html5.links"),
path('html5/text/formatting', views.formatting_page, name="books.html5.formatting"),
path('html5/listing', views.listing_page, name="books.html5.listing"),
path('html5/tables', views.tables_page, name="books.html5.tables"),
path('search/', views.search_books, name="books.search"),
]
