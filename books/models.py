from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('publisher', 'Εκδότης'),
        ('bookstore', 'Βιβλιοπωλείο'),
        ('author', 'Συγγραφέας'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    def __str__(self):
        return self.username


class Publisher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Bookstore(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    bookstore = models.ManyToManyField(Bookstore)

    def __str__(self):
        return self.title

class BookstoreStock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookstore = models.ForeignKey(Bookstore, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)

    class Meta:
        unique_together = ('book', 'bookstore')

    def __str__(self):
        return f'{self.book.title} - {self.bookstore.name}'
