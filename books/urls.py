from django.urls import path
from . import views

urlpatterns = [
    # Subjects
    path("subjects/", views.SubjectListCreateView.as_view(), name="subjects"),
    path("subjects/<int:pk>/", views.SubjectDetailView.as_view(), name="subject-detail"),

    # Topics
    path("subjects/<int:pk>/topics/", views.TopicListCreateView.as_view(), name="subject-topics"),
    path("topics/<int:pk>/", views.TopicDetailView.as_view(), name="topic-detail"),

    # Notes
    path("topics/<int:pk>/notes/", views.NoteCreateView.as_view(), name="create-note"),
    path("notes/", views.NoteListView.as_view(), name="notes"),
    path("notes/<int:pk>/", views.NoteDetailView.as_view(), name="note-detail"),

    # Quizzes
    path("topics/<int:pk>/quiz/", views.TopicQuizView.as_view(), name="topic-quiz"),
    path("quiz/attempt/", views.QuizAttemptView.as_view(), name="quiz-attempt"),
    path("quiz/attempts/", views.QuizHistoryView.as_view(), name="quiz-history"),
]
