from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Organization

User = get_user_model()


class Vacancy(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='vacancies')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_vacancies')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='responses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.applicant)
