from django.contrib import admin

from jobs.models import Vacancy, Application

# Register your models here.

admin.site.register(Vacancy)
admin.site.register(Application)
