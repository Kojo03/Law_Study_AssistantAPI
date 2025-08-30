from django.contrib import admin
from .models import Book, BookCheckout, Category, Reservation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies', 'location']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['category', 'published_date', 'added_date']
    readonly_fields = ['added_date']

@admin.register(BookCheckout)
class BookCheckoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'checkout_date', 'due_date', 'return_date', 'is_returned', 'fine_amount']
    list_filter = ['is_returned', 'checkout_date', 'due_date']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['checkout_date', 'due_date']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'reservation_date', 'is_active', 'notified']
    list_filter = ['is_active', 'notified', 'reservation_date']
    search_fields = ['user__username', 'book__title']