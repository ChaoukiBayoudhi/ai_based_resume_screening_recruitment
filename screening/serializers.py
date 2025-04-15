from rest_framework import serializers
from .models import (
    Applicant, Job, Resume, Interview,
    ScreeningQuestion, ScreeningAnswer, Feedback,
    Notification, JobApplication
)

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ['id', 'user', 'full_name', 'email', 'phone_number', 'skills', 'linkedin_profile','user_id']
        read_only_fields = ['user']

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'recruiter', 'title', 'description', 'required_skills', 'location', 'salary_range']

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'applicant', 'file', 'parsed_text', 'extracted_skills', 'ai_score']
        read_only_fields = ['applicant', 'parsed_text', 'extracted_skills', 'ai_score']

class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'job', 'applicant', 'date', 'time', 'mode', 'status', 'feedback']

class ScreeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningQuestion
        fields = ['id', 'job', 'question_text', 'answer_text']

class ScreeningAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningAnswer
        fields = ['id', 'question', 'applicant', 'answer_text']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'interview', 'reviewer', 'comments', 'rating']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
        read_only_fields = ['user', 'created_at']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'applicant', 'job', 'status']
        read_only_fields = ['applicant']

