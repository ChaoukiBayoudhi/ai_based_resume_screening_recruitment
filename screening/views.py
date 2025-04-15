from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import (
    Applicant, Job, Resume, Interview,
    ScreeningQuestion, ScreeningAnswer, Feedback,
    Notification, JobApplication
)
from .serializers import (
    ApplicantSerializer, JobSerializer, ResumeSerializer,
    InterviewSerializer, ScreeningQuestionSerializer,
    ScreeningAnswerSerializer, FeedbackSerializer,
    NotificationSerializer, JobApplicationSerializer
)

class ApplicantViewSet(viewsets.ModelViewSet):
    queryset = Applicant.objects.all()
    serializer_class = ApplicantSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def resumes(self, request, pk=None):
        applicant = self.get_object()
        resumes = applicant.resumes.all()
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def applicants(self, request, pk=None):
        job = self.get_object()
        applicants = job.applicants.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user.applicant_profile)

class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScreeningQuestionViewSet(viewsets.ModelViewSet):
    queryset = ScreeningQuestion.objects.all()
    serializer_class = ScreeningQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScreeningAnswerViewSet(viewsets.ModelViewSet):
    queryset = ScreeningAnswer.objects.all()
    serializer_class = ScreeningAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({'status': 'all notifications marked as read'})

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user.applicant_profile)