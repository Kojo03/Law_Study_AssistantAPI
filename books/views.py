from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Subject, Topic, Note, Quiz, QuizAttempt
from .serializers import (
    SubjectSerializer, TopicSerializer,
    NoteSerializer, QuizSerializer, QuizAttemptSerializer
)
from accounts.permissions import IsLecturerOrAdmin

# ----- SUBJECTS -----
class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [permissions.AllowAny()]


class SubjectDetailView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


# ----- TOPICS -----
class TopicListCreateView(generics.ListCreateAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        subject_id = self.kwargs["pk"]
        return Topic.objects.filter(subject_id=subject_id)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsLecturerOrAdmin()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        subject_id = self.kwargs["pk"]
        serializer.save(subject_id=subject_id)


class TopicDetailView(generics.RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


# ----- NOTES -----
class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class NoteCreateView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        topic_id = self.kwargs["pk"]
        serializer.save(user=self.request.user, topic_id=topic_id)


# ----- QUIZZES -----
class TopicQuizView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        topic_id = self.kwargs["pk"]
        return Quiz.objects.filter(topic_id=topic_id).prefetch_related('answers')


class QuizAttemptView(generics.CreateAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        topic_id = self.request.data.get("topic")
        answers = self.request.data.get("answers", {})
        
        quizzes = Quiz.objects.filter(topic_id=topic_id)
        score = 0
        
        for quiz in quizzes:
            correct_answers = quiz.answers.filter(is_correct=True).values_list('id', flat=True)
            user_answer = answers.get(str(quiz.id))
            
            if user_answer and int(user_answer) in correct_answers:
                score += 1
                
        serializer.save(user=self.request.user, topic_id=topic_id, score=score)


class QuizHistoryView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(user=self.request.user)
