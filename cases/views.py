from rest_framework import generics, permissions, filters
from django.db.models import Q
from django.utils.html import escape
from .models import Case
from .serializers import CaseSerializer
from accounts.permissions import IsAdminOrReadOnly

# List & Create cases for a topic
class CaseListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'suit_number']
    ordering_fields = ['title', 'year']
    ordering = ['title']

    def get_queryset(self):
        topic_id = int(escape(str(self.kwargs["pk"])))
        queryset = Case.objects.filter(topic_id=topic_id)
        
        # Filter by availability
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(available_copies__gt=0)
            
        return queryset

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrReadOnly()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        topic_id = int(escape(str(self.kwargs["pk"])))
        serializer.save(topic_id=topic_id)

# List all cases with filtering
class CaseListView(generics.ListAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'suit_number']
    ordering_fields = ['title', 'year']
    ordering = ['title']
    
    def get_queryset(self):
        queryset = Case.objects.all()
        
        # Filter by availability
        available_only = escape(str(self.request.query_params.get('available_only', '')))
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(available_copies__gt=0)
            
        return queryset

# Case details
class CaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
    permission_classes = [IsAdminOrReadOnly]
