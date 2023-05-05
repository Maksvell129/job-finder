from django.urls import path

from jobs import views
from jobs.views import ApplicationCreateView

urlpatterns = [
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/apply/', ApplicationCreateView.as_view(), name='apply_vacancy'),
    path('create_vacancy/', views.VacancyCreateView.as_view(), name='create_vacancy'),
]
