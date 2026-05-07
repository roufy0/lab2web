from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Book, Author, Publisher
from .forms import BookForm

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def index(request):
    return render(request, "bookmodule/index.html")
def list_books(request):
    return render(request, 'bookmodule/list_books.html')
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html', {'bookId': bookId})
def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links_page(request):
    return render(request, 'bookmodule/links.html')

def formatting_page(request):
    return render(request, 'bookmodule/formatting.html')

def listing_page(request):
    return render(request, 'bookmodule/listing.html')

def tables_page(request):
    return render(request, 'bookmodule/tables.html')

def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})
    else:
        return render(request, 'bookmodule/search.html')


def lab9_part1_listbooks(request):
    books = Book.objects.all().order_by('id')
    return render(request, 'bookmodule/lab9_part1_listbooks.html', {'books': books})


def lab9_part1_addbook(request):
    publishers = Publisher.objects.all()
    authors = Author.objects.all()
    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        price = request.POST.get('price', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        pubdate = request.POST.get('pubdate', '').strip()
        rating = request.POST.get('rating', '').strip()
        publisher_id = request.POST.get('publisher')
        author_ids = request.POST.getlist('authors')

        if not title or not price or not quantity or not pubdate or not rating:
            error = "All fields except publisher/authors are required."
        else:
            try:
                book = Book.objects.create(
                    title=title,
                    price=float(price),
                    quantity=int(quantity),
                    pubdate=pubdate,
                    rating=int(rating),
                    publisher=Publisher.objects.filter(id=publisher_id).first() if publisher_id else None,
                )
                if author_ids:
                    book.authors.set(Author.objects.filter(id__in=author_ids))
                return redirect('books.lab9_part1.listbooks')
            except (ValueError, TypeError) as e:
                error = f"Invalid input: {e}"

    return render(request, 'bookmodule/lab9_part1_addbook.html', {
        'publishers': publishers,
        'authors': authors,
        'error': error,
        'data': request.POST,
    })


def lab9_part1_editbook(request, id):
    book = get_object_or_404(Book, id=id)
    publishers = Publisher.objects.all()
    authors = Author.objects.all()
    error = None

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        price = request.POST.get('price', '').strip()
        quantity = request.POST.get('quantity', '').strip()
        pubdate = request.POST.get('pubdate', '').strip()
        rating = request.POST.get('rating', '').strip()
        publisher_id = request.POST.get('publisher')
        author_ids = request.POST.getlist('authors')

        if not title or not price or not quantity or not pubdate or not rating:
            error = "All fields except publisher/authors are required."
        else:
            try:
                book.title = title
                book.price = float(price)
                book.quantity = int(quantity)
                book.pubdate = pubdate
                book.rating = int(rating)
                book.publisher = Publisher.objects.filter(id=publisher_id).first() if publisher_id else None
                book.save()
                book.authors.set(Author.objects.filter(id__in=author_ids))
                return redirect('books.lab9_part1.listbooks')
            except (ValueError, TypeError) as e:
                error = f"Invalid input: {e}"

    return render(request, 'bookmodule/lab9_part1_editbook.html', {
        'book': book,
        'publishers': publishers,
        'authors': authors,
        'selected_authors': set(book.authors.values_list('id', flat=True)),
        'error': error,
    })


def lab9_part1_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.lab9_part1.listbooks')



def lab9_part2_listbooks(request):
    books = Book.objects.all().order_by('id')
    return render(request, 'bookmodule/lab9_part2_listbooks.html', {'books': books})


def lab9_part2_addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab9_part2.listbooks')
    else:
        form = BookForm()
    return render(request, 'bookmodule/lab9_part2_addbook.html', {'form': form})


def lab9_part2_editbook(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books.lab9_part2.listbooks')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookmodule/lab9_part2_editbook.html', {'form': form, 'book': book})


def lab9_part2_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.lab9_part2.listbooks')
