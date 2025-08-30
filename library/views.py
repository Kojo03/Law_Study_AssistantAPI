from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from drf_spectacular.utils import extend_schema
# from django_filters.rest_framework import DjangoFilterBackend  # Uncomment after installing django-filter
from .models import Book, BookCheckout, Category, Reservation, Transaction
from .serializers import (
    BookSerializer, BookCheckoutSerializer, CategorySerializer, ReservationSerializer,
    CheckoutRequestSerializer, ReturnRequestSerializer, ReservationRequestSerializer,
    TransactionSerializer, NotificationResponseSerializer
)
from accounts.permissions import IsAdminUser, IsAdminOrReadOnly

class BookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related('category').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = BookPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'isbn']
    ordering_fields = ['title', 'author', 'added_date']
    ordering = ['-added_date']
    
    def get_queryset(self):
        queryset = Book.objects.select_related('category').all()
        available_only = self.request.query_params.get('available_only', '')
        if available_only.lower() == 'true':
            queryset = queryset.filter(available_copies__gt=0)
        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user, is_active=True)

class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

@extend_schema(request=CheckoutRequestSerializer, responses=BookCheckoutSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_book(request):
    serializer = CheckoutRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    book_id = serializer.validated_data['book_id']
    book = get_object_or_404(Book, id=book_id)
    
    # Check if book is available
    if book.available_copies <= 0:
        return Response({'error': 'No copies available'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already has this book checked out
    existing_checkout = BookCheckout.objects.filter(
        user=request.user, book=book, is_returned=False
    ).exists()
    
    if existing_checkout:
        return Response({'error': 'You already have this book checked out'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        # Create checkout record
        checkout = BookCheckout.objects.create(user=request.user, book=book)
        # Reduce available copies
        book.available_copies -= 1
        book.save()
        
        # Create transaction record
        Transaction.objects.create(
            user=request.user,
            book=book,
            transaction_type='checkout',
            notes=f'Book checked out: {book.title}'
        )
        
        # Cancel any active reservation for this book by this user
        Reservation.objects.filter(
            user=request.user, book=book, is_active=True
        ).update(is_active=False)
    
    return Response(BookCheckoutSerializer(checkout).data, status=status.HTTP_201_CREATED)

@extend_schema(request=ReturnRequestSerializer, responses=BookCheckoutSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request):
    serializer = ReturnRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    checkout_id = serializer.validated_data['checkout_id']
    checkout = get_object_or_404(BookCheckout, id=checkout_id)
    
    if checkout.user != request.user:
        return Response({'error': 'You can only return your own books'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    if checkout.is_returned:
        return Response({'error': 'Book already returned'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        # Calculate fine if overdue
        checkout.calculate_fine()
        
        # Mark as returned
        checkout.is_returned = True
        checkout.return_date = timezone.now()
        checkout.save()
        
        # Increase available copies
        checkout.book.available_copies += 1
        checkout.book.save()
        
        # Create transaction record
        Transaction.objects.create(
            user=request.user,
            book=checkout.book,
            transaction_type='return',
            notes=f'Book returned: {checkout.book.title}'
        )
        
        # Notify users with reservations
        try:
            from .notifications import notify_book_availability
            notify_book_availability()
        except ImportError:
            pass
    
    return Response(BookCheckoutSerializer(checkout).data, status=status.HTTP_200_OK)

@extend_schema(responses=BookCheckoutSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_checkouts(request):
    checkouts = BookCheckout.objects.filter(user=request.user).select_related('book')
    serializer = BookCheckoutSerializer(checkouts, many=True)
    return Response(serializer.data)

@extend_schema(request=ReservationRequestSerializer, responses=ReservationSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reserve_book(request):
    serializer = ReservationRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    book_id = serializer.validated_data['book_id']
    book = get_object_or_404(Book, id=book_id)
    
    # Check if book is available
    if book.available_copies > 0:
        return Response({'error': 'Book is currently available for checkout'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already has a reservation for this book
    existing_reservation = Reservation.objects.filter(
        user=request.user, book=book, is_active=True
    ).exists()
    
    if existing_reservation:
        return Response({'error': 'You already have a reservation for this book'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    with transaction.atomic():
        reservation = Reservation.objects.create(user=request.user, book=book)
        
        # Create transaction record
        Transaction.objects.create(
            user=request.user,
            book=book,
            transaction_type='reservation',
            notes=f'Book reserved: {book.title}'
        )
    
    return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)

@extend_schema(responses=BookCheckoutSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overdue_books(request):
    overdue_checkouts = BookCheckout.objects.filter(
        user=request.user, is_returned=False, due_date__lt=timezone.now()
    ).select_related('book')
    serializer = BookCheckoutSerializer(overdue_checkouts, many=True)
    return Response(serializer.data)

@extend_schema(responses=TransactionSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_transactions(request):
    """Get user's transaction history"""
    transactions = Transaction.objects.filter(user=request.user).select_related('book')
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@extend_schema(responses=BookCheckoutSerializer(many=True))
@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_overdue_books(request):
    """Admin view of all overdue books"""
    overdue_checkouts = BookCheckout.objects.filter(
        is_returned=False, due_date__lt=timezone.now()
    ).select_related('book', 'user')
    
    # Update fines
    for checkout in overdue_checkouts:
        checkout.calculate_fine()
    
    serializer = BookCheckoutSerializer(overdue_checkouts, many=True)
    return Response(serializer.data)

@extend_schema(responses=NotificationResponseSerializer)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def send_overdue_notifications(request):
    """Admin endpoint to send overdue notifications"""
    from .notifications import check_overdue_books
    count = check_overdue_books()
    return Response({'message': f'Sent {count} overdue notifications'})