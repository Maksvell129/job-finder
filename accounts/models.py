from datetime import date

from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, )
    phone_number = PhoneNumberField(blank=True, unique=True, )
    date_of_birth = models.DateField()
    is_employer = models.BooleanField(default=False)

    favorite_vacancies = models.ManyToManyField('jobs.Vacancy', blank=True, through='FavoriteVacancy',
                                                related_name='favorited_by')
    resume = models.FileField(upload_to='resume/', null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    head = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='head_of_organization')

    def __str__(self):
        return self.name


class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='employers', null=True)


class FavoriteVacancy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey('jobs.Vacancy', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class UserNotification(models.Model):
    UNREAD = 1
    READ = 2

    STATUS = [
        (UNREAD, 'UNREAD'),
        (READ, 'READ'),
    ]

    message = models.TextField(max_length=1024)
    status = models.IntegerField(choices=STATUS, default=UNREAD)
    recipient = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='recipient_notifications')
    sender = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='sender_notifications', null=True)
    vacancy = models.ForeignKey('jobs.Vacancy', on_delete=CASCADE, related_name='notifications', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=CASCADE, related_name='notifications', null=True)
