from rest_framework import serializers
from django.utils.html import escape
from .models import Book, BookCheckout, Category, Reservation, Transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
    
    def validate(self, attrs):
        # Sanitize text fields
        for field in ['name', 'description']:
            if field in attrs and attrs[field]:
                attrs[field] = escape(str(attrs[field]))
        return attrs

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'published_date', 'publisher', 
                 'category', 'category_name', 'total_copies', 'available_copies', 
                 'description', 'location', 'added_date', 'is_available']
        read_only_fields = ['added_date', 'available_copies']
    
    def validate(self, attrs):
        # Sanitize text fields
        for field in ['title', 'author', 'isbn', 'publisher', 'description', 'location']:
            if field in attrs and attrs[field]:
                attrs[field] = escape(str(attrs[field]))
        return attrs

class BookCheckoutSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = BookCheckout
        fields = ['id', 'user', 'book', 'book_title', 'user_username', 
                 'checkout_date', 'due_date', 'return_date', 'is_returned', 
                 'fine_amount', 'is_overdue', 'days_overdue']
        read_only_fields = ['checkout_date', 'due_date', 'return_date']

class ReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'user', 'book', 'book_title', 'user_username', 
                 'reservation_date', 'is_active', 'notified']
        read_only_fields = ['reservation_date']

class CheckoutRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(min_value=1)
    
    def validate_book_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid book ID")
        return value

class ReturnRequestSerializer(serializers.Serializer):
    checkout_id = serializers.IntegerField(min_value=1)
    
    def validate_checkout_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid checkout ID")
        return value

class ReservationRequestSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(min_value=1)
    
    def validate_book_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Invalid book ID")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'book_title', 'user_username', 
                 'transaction_type', 'transaction_date', 'notes']
        read_only_fields = ['transaction_date']

class NotificationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()