from django.urls import path
from . import views

urlpatterns = [
    # All cases
    path("", views.CaseListView.as_view(), name="case-list"),
    path("<int:pk>/", views.CaseDetailView.as_view(), name="case-detail"),
    # Cases by topic
    path("topics/<int:pk>/cases/", views.CaseListCreateView.as_view(), name="topic-cases"),
]
