from rest_framework import generics, permissions
from .models import Case
from .serializers import CaseSerializer
from accounts.permissions import IsLecturerOrAdmin

# List & Create cases for a topic
class CaseListCreateView(generics.ListCreateAPIView):
    serializer_class = CaseSerializer

    def get_queryset(self):
        topic_id = self.kwargs["pk"]
        return Case.objects.filter(topic_id=topic_id)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        topic_id = self.kwargs["pk"]
        serializer.save(topic_id=topic_id)


# Case details
class CaseDetailView(generics.RetrieveAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
