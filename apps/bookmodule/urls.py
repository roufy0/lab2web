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

path('lab9_part1/listbooks', views.lab9_part1_listbooks, name="books.lab9_part1.listbooks"),
path('lab9_part1/addbook', views.lab9_part1_addbook, name="books.lab9_part1.addbook"),
path('lab9_part1/editbook/<int:id>', views.lab9_part1_editbook, name="books.lab9_part1.editbook"),
path('lab9_part1/deletebook/<int:id>', views.lab9_part1_deletebook, name="books.lab9_part1.deletebook"),

path('lab9_part2/listbooks', views.lab9_part2_listbooks, name="books.lab9_part2.listbooks"),
path('lab9_part2/addbook', views.lab9_part2_addbook, name="books.lab9_part2.addbook"),
path('lab9_part2/editbook/<int:id>', views.lab9_part2_editbook, name="books.lab9_part2.editbook"),
path('lab9_part2/deletebook/<int:id>', views.lab9_part2_deletebook,name="books.lab9_part2.deletebook"),
]
