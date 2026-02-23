from django.http import HttpResponse
from django.shortcuts import render

<<<<<<< HEAD
def index(request):
    return render(request, "bookmodule/index.html")
def list_books(request):
    return render(request, 'bookmodule/list_books.html')
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html', {'bookId': bookId})
def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')
=======
def index2(request, val1 = 0): #add the view function (index2)
    return HttpResponse("value1 = "+str(val1))

def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})

def viewbook(request, bookId):
    # assume that we have the following books somewhere (e.g. database)
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId: targetBook = book1
    if book2['id'] == bookId: targetBook = book2
    context = {'book':targetBook}
    return render(request, 'bookmodule/show.html', context)
>>>>>>> d6335cfb46e8932c71840fbd7b5753783f956a79
