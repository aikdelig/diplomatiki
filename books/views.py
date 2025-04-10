from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from books.forms import BookUpdateForm
from books.models import Book, Author, Bookstore, Publisher, BookstoreStock

@login_required
@csrf_protect
def dashboard(request):
    user = request.user
    if user.role == 'publisher':
        try:
            publisher = Publisher.objects.get(user=user)
        except Publisher.DoesNotExist:
            return render(request, 'books/publisher_dashboard.html', {'error': 'Δεν βρέθηκε εκδότης'})

        books = Book.objects.filter(publisher=publisher)

        bookstore_books = {}

        for book in books:
            bookstore_stocks = BookstoreStock.objects.filter(book=book)
            for bookstore_stock in bookstore_stocks:
                bookstore = bookstore_stock.bookstore
                if bookstore not in bookstore_books:
                    bookstore_books[bookstore] = []
                bookstore_books[bookstore].append({
                    'book': book,
                    'stock': bookstore_stock.stock,
                    'sold': bookstore_stock.sold
                })

        return render(request, 'books/publisher_dashboard.html', {
            'publisher': publisher,
            'bookstore_books': bookstore_books
        })

    elif user.role == 'bookstore':
        try:
            bookstore = Bookstore.objects.get(user=user)
        except Bookstore.DoesNotExist:
            bookstore = None
            books = []

        if bookstore:
            bookstore_stocks = BookstoreStock.objects.filter(bookstore=bookstore)
            books = [stock.book for stock in bookstore_stocks]

            if request.method == "POST":
                book_id = request.POST.get("book_id")
                book = get_object_or_404(Book, id=book_id)
                form = BookUpdateForm(request.POST, instance=book)

                if form.is_valid():
                    form.save()
                    return redirect('dashboard')

        return render(request, 'books/bookstore_dashboard.html', {
            'books': books,
            'bookstore': bookstore,
            'bookstore_stocks': bookstore_stocks
        })

    elif user.role == 'author':
        try:
            author = Author.objects.get(user=user)
            books = Book.objects.filter(author=author)

        except Author.DoesNotExist:
            books = []
        if books:
            bookstore_stocks = BookstoreStock.objects.filter(book__in=books)
            books = [stock.book for stock in bookstore_stocks]
        return render(request, 'books/author_dashboard.html', {'user': user, 'books': books,'bookstore_stocks': bookstore_stocks})

    else:
        return redirect('login')


def custom_logout(request):
    logout(request)
    return redirect('/')
