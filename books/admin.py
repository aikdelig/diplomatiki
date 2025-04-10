from django.contrib import admin
from .models import CustomUser, Publisher, Author, Bookstore, Book, BookstoreStock

admin.site.register(CustomUser)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Bookstore)
admin.site.register(Book)
admin.site.register(BookstoreStock)
