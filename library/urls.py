from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Books CRUD
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Reservations
    path('reservations/', views.ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('reserve/', views.reserve_book, name='reserve-book'),
    
    # Checkout/Return
    path('checkout/', views.checkout_book, name='checkout-book'),
    path('return/', views.return_book, name='return-book'),
    path('my-checkouts/', views.user_checkouts, name='user-checkouts'),
    path('overdue/', views.overdue_books, name='overdue-books'),
    
    # Transactions
    path('transactions/', views.user_transactions, name='user-transactions'),
    
    # Admin endpoints
    path('admin/overdue/', views.all_overdue_books, name='admin-overdue'),
    path('admin/notifications/', views.send_overdue_notifications, name='send-notifications'),
]