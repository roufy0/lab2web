from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Sum, Avg, Max, Min, F, FloatField, ExpressionWrapper
from django.contrib.auth.decorators import login_required
from .models import Book, Address, Student, Publisher, Author, Address2, Student2, Product
from .forms import BookForm, AddressForm, StudentForm, Address2Form, Student2Form, ProductForm

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

def insert_books(request):
    mybook1 = Book(
            title='Clean Code',
            author='Robert C. Martin',
            price=110.00,
            edition=1
        )
    mybook1.save()

    mybook2 = Book.objects.create(
            title='Design Patterns',
            author='Erich Gamma',
            price=95.00,
            edition=2
        )
    mybook2.save()

    mybooks = Book.objects.all()
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})

def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='The') 
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='the').filter(edition__gte=3).exclude(price__lte=70)[:1]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')
    
def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8_task1.html', {'books': books})

def lab8_task2(request):
    books = Book.objects.filter(Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu')))
    return render(request, 'bookmodule/lab8_task2.html', {'books': books})

def lab8_task3(request):
    books = Book.objects.filter(~Q(edition__gt=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu')))
    return render(request, 'bookmodule/lab8_task3.html', {'books': books})

def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/lab8_task4.html', {'books': books})

def lab8_task5(request):
    stats = Book.objects.aggregate(
        count=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price'),
    )
    return render(request, 'bookmodule/lab8_task5.html', {'stats': stats})

def lab8_task7(request):
    city_counts = Address.objects.annotate(student_count=Count('student')).values('city', 'student_count')
    return render(request, 'bookmodule/lab8_task7.html', {'city_counts': city_counts})

def lab9_task1(request):
    total_quantity = Book.objects.aggregate(Sum('quantity')) ['quantity__sum'] or 1

    books = Book.objects.annotate(
        availability=F('quantity') * 100 / total_quantity)

    return render(request, 'bookmodule/lab9_task1.html', {'books': books})


def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'bookmodule/lab9_task2.html', {'publishers': publishers})

def lab9_task3(request):
    publishers = Publisher.objects.annotate(oldest_pubdate=Min('book__pubdate'))
    return render(request, 'bookmodule/lab9_task3.html', {'publishers': publishers})

def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price'),
    )
    return render(request, 'bookmodule/lab9_task4.html', {'publishers': publishers})

def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_count=Count('book', filter=Q(book__rating__gte=4)),
        highly_rated_quantity=Sum('book__quantity', filter=Q(book__rating__gte=4)),
    )
    return render(request, 'bookmodule/lab9_task5.html', {'publishers': publishers})

def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        book_count=Count(
            'book',
            filter=Q(book__price__gt=50) & Q(book__quantity__lt=5) & Q(book__quantity__gte=1)
        )
    )
    return render(request, 'bookmodule/lab9_task6.html', {'publishers': publishers})

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


@login_required
def lab11_task1_list_addresses(request):
    addresses = Address.objects.all().order_by('id')
    return render(request, 'bookmodule/lab11_task1_list_addresses.html', {'addresses': addresses})


@login_required
def lab11_task1_add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task1.list_addresses')
    else:
        form = AddressForm()
    return render(request, 'bookmodule/lab11_task1_add_address.html', {'form': form})


@login_required
def lab11_task1_edit_address(request, id):
    address = get_object_or_404(Address, id=id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task1.list_addresses')
    else:
        form = AddressForm(instance=address)
    return render(request, 'bookmodule/lab11_task1_edit_address.html', {'form': form, 'address': address})


@login_required
def lab11_task1_delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    return redirect('books.lab11.task1.list_addresses')


@login_required
def lab11_task1_list_students(request):
    students = Student.objects.select_related('address').order_by('id')
    return render(request, 'bookmodule/lab11_task1_list_students.html', {'students': students})


@login_required
def lab11_task1_add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task1.list_students')
    else:
        form = StudentForm()
    return render(request, 'bookmodule/lab11_task1_add_student.html', {'form': form})


@login_required
def lab11_task1_edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task1.list_students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'bookmodule/lab11_task1_edit_student.html', {'form': form, 'student': student})


@login_required
def lab11_task1_delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('books.lab11.task1.list_students')



@login_required
def lab11_task2_list_addresses(request):
    addresses = Address2.objects.all().order_by('id')
    return render(request, 'bookmodule/lab11_task2_list_addresses.html', {'addresses': addresses})


@login_required
def lab11_task2_add_address(request):
    if request.method == 'POST':
        form = Address2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task2.list_addresses')
    else:
        form = Address2Form()
    return render(request, 'bookmodule/lab11_task2_add_address.html', {'form': form})


@login_required
def lab11_task2_edit_address(request, id):
    address = get_object_or_404(Address2, id=id)
    if request.method == 'POST':
        form = Address2Form(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task2.list_addresses')
    else:
        form = Address2Form(instance=address)
    return render(request, 'bookmodule/lab11_task2_edit_address.html', {'form': form, 'address': address})


@login_required
def lab11_task2_delete_address(request, id):
    address = get_object_or_404(Address2, id=id)
    address.delete()
    return redirect('books.lab11.task2.list_addresses')


@login_required
def lab11_task2_list_students(request):
    students = Student2.objects.prefetch_related('addresses').order_by('id')
    return render(request, 'bookmodule/lab11_task2_list_students.html', {'students': students})


@login_required
def lab11_task2_add_student(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task2.list_students')
    else:
        form = Student2Form()
    return render(request, 'bookmodule/lab11_task2_add_student.html', {'form': form})


@login_required
def lab11_task2_edit_student(request, id):
    student = get_object_or_404(Student2, id=id)
    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task2.list_students')
    else:
        form = Student2Form(instance=student)
    return render(request, 'bookmodule/lab11_task2_edit_student.html', {'form': form, 'student': student})


@login_required
def lab11_task2_delete_student(request, id):
    student = get_object_or_404(Student2, id=id)
    student.delete()
    return redirect('books.lab11.task2.list_students')

@login_required
def lab11_task3_list_products(request):
    products = Product.objects.all().order_by('id')
    return render(request, 'bookmodule/lab11_task3_list_products.html', {'products': products})


@login_required
def lab11_task3_add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task3.list_products')
    else:
        form = ProductForm()
    return render(request, 'bookmodule/lab11_task3_add_product.html', {'form': form})


@login_required
def lab11_task3_edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('books.lab11.task3.list_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'bookmodule/lab11_task3_edit_product.html', {'form': form, 'product': product})


@login_required
def lab11_task3_delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('books.lab11.task3.list_products')
