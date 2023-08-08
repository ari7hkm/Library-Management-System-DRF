from typing import Any
from django.contrib import admin
from django.contrib.admin.widgets import AdminDateWidget
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . models import Book, Language, Genre, Student, Borrow, BorrowItem


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    autocomplete_fields = ['genre', 'language']
    list_display = ['title', 'author', 'inventory', 'language']
    list_select_related = ['language']
    search_fields = ['title']
    ordering = ['title']


    

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_book']
    list_display = ['title', 'books_count']
    search_fields = ['title']
    ordering = ['title']

    @admin.display(ordering='books_count')
    def books_count(self, genre):
        url = (
            reverse('admin:library_book_changelist')
            + '?'
            + urlencode({
                'genre__id': str(genre.id)
            })
        )
        return format_html('<a href="{}">{} Books</a>', url, genre.books_count)



    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            books_count=Count('book')
        )



@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']



@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    list_display = ['id', 'first_name', 'last_name', 'birth_date']
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user']



class BorrowInline(admin.TabularInline):
    autocomplete_fields = ['book']
    min_num = 1
    max_num = 5
    model = BorrowItem
    extra = 0


@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    autocomplete_fields = ['student']
    list_display = ['student','date_issue']
    inlines = [BorrowInline]