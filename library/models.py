from django.conf import settings
from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4



class Genre(models.Model):
    title = models.CharField(max_length=100)
    featured_book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    author = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Language, on_delete=models.PROTECT, null=True)
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    picture = models.ImageField(upload_to='books/image', blank=True, null=True)

    def __str__(self):
        return self.title
    


class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    total_books_due = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='students/image', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    



class Borrow(models.Model):
    BORROWED_STATUS_PENDING = 'P'
    BORROWED_STATUS_COMPELETE = 'C'

    BORROWED_STATUS_CHOICES = [
        (BORROWED_STATUS_PENDING, 'Pending'),
        (BORROWED_STATUS_COMPELETE, 'Complete')
    ]


    student = models.ForeignKey(Student, on_delete=models.CASCADE) 
    date_issue = models.DateTimeField(auto_now_add=True)
    borrowed_status = models.CharField(
        max_length=1, choices=BORROWED_STATUS_CHOICES,
                                       default=BORROWED_STATUS_PENDING)

    


class BorrowItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='orderitems')
    borrow = models.ForeignKey(Borrow, on_delete=models.PROTECT, related_name='items')
    date_of_return = models.DateField(null=True)

    

    def __str__(self):
        return self.book.title
    

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_review = models.DateField(auto_now_add=True)




class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_of_return = models.DateField(null=True)

    class Meta:
        unique_together = [['order', 'book']]