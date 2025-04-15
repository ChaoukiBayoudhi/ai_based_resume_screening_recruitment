from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator, EmailValidator, MinValueValidator


class TimeStampedModel(models.Model):
    """Abstract base class that provides self-updating created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Applicant(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    full_name = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()])
    phone_number = models.CharField(max_length=20, validators=[
        RegexValidator(r'^\+?[0-9]{9,15}$', 'Enter a valid phone number.')
    ])
    skills = models.TextField()
    linkedin_profile = models.URLField(blank=True)

    class Meta:
        ordering = ['full_name']
        db_table = 'applicant'
        indexes = [
            models.Index(fields=['full_name']),
            models.Index(fields=['email'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_applicant_email')
        ]

    def __str__(self):
        return self.full_name


class Recruiter(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    contact_email = models.EmailField(validators=[EmailValidator()])

    class Meta:
        ordering = ['company_name']
        db_table = 'recruiter'
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['contact_email'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['contact_email'], name='unique_recruiter_email')
        ]

    def __str__(self):
        return f"{self.company_name} - {self.position}"


class Job(TimeStampedModel):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='jobs')
    applicants = models.ManyToManyField(Applicant, related_name='applied_jobs', blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100)

    class Meta:
        ordering = ['title']
        db_table = 'job'
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['location'])
        ]

    def __str__(self):
        return self.title


class Resume(TimeStampedModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'docx'])
    ])
    parsed_text = models.TextField(blank=True)
    extracted_skills = models.TextField(blank=True)
    ai_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0.0)])

    class Meta:
        ordering = ['-id']
        db_table = 'resume'
        indexes = [
            models.Index(fields=['applicant']),
            models.Index(fields=['ai_score'])
        ]

    def __str__(self):
        return f"Resume of {self.applicant.full_name}"


class Interview(TimeStampedModel):
    INTERVIEW_MODE_CHOICES = [
        ('online', 'Online'),
        ('in_person', 'In Person'),
    ]

    INTERVIEW_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='interviews')
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='interviews')
    date = models.DateField()
    time = models.TimeField()
    mode = models.CharField(max_length=20, choices=INTERVIEW_MODE_CHOICES)
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ['date', 'time']
        db_table = 'interview'
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['job', 'applicant'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['job', 'applicant', 'date', 'time'], name='unique_interview_schedule')
        ]

    def __str__(self):
        return f"Interview for {self.applicant.full_name} on {self.date} at {self.time}"


class ScreeningQuestion(TimeStampedModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='screening_questions')
    question_text = models.TextField()
    answer_text = models.TextField(blank=True)

    class Meta:
        ordering = ['job', 'question_text']
        db_table = 'screening_question'
        indexes = [
            models.Index(fields=['job']),
            models.Index(fields=['question_text'])
        ]

    def __str__(self):
        return f"Question for {self.job.title}: {self.question_text}"


class ScreeningAnswer(TimeStampedModel):
    question = models.ForeignKey(ScreeningQuestion, on_delete=models.CASCADE, related_name='answers')
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='screening_answers')
    answer_text = models.TextField()

    class Meta:
        ordering = ['question', 'applicant']
        db_table = 'screening_answer'
        indexes = [
            models.Index(fields=['question']),
            models.Index(fields=['applicant'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['question', 'applicant'], name='unique_screening_answer')
        ]

    def __str__(self):
        return f"Answer by {self.applicant.full_name} for question: {self.question.question_text}"


class Feedback(TimeStampedModel):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='feedbacks')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['-id']
        db_table = 'feedback'
        indexes = [
            models.Index(fields=['interview']),
            models.Index(fields=['reviewer'])
        ]

    def __str__(self):
        return f"Feedback for {self.interview.applicant.full_name} by {self.reviewer.username}"


class Notification(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        db_table = 'notification'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['is_read'])
        ]

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


class JobApplication(TimeStampedModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('interviewed', 'Interviewed'),
        ('offered', 'Offered'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected')
    ], default='applied')

    class Meta:
        ordering = ['-created_at']
        db_table = 'job_application'
        indexes = [
            models.Index(fields=['applicant']),
            models.Index(fields=['job'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['applicant', 'job'], name='unique_job_application')
        ]

    def __str__(self):
        return f"Application by {self.applicant.full_name} for {self.job.title}"