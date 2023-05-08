from django.contrib import admin
from accounts.models import CustomUser, Organization, Employer, UserNotification, FavoriteVacancy

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(Employer)
admin.site.register(UserNotification)
admin.site.register(FavoriteVacancy)
