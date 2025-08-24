from django.urls import path
from . import views

urlpatterns = [
    path("topics/<int:pk>/cases/", views.CaseListCreateView.as_view(), name="topic-cases"),
    path("<int:pk>/", views.CaseDetailView.as_view(), name="case-detail"),
]
