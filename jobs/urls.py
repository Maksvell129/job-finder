from django.urls import path

from jobs import views
from jobs.views import ApplicationCreateView, EmployerApplicationListView, ApplicantApplicationListView, \
    ApplicationsChangeStatusView, EmployerVacancyListView, VacancyUpdateView, ToggleFavoriteVacancyView, \
    FavoriteVacanciesListView, VacancyDeleteView

urlpatterns = [
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('vacancies/<int:vacancy_id>/apply/', ApplicationCreateView.as_view(), name='apply_vacancy'),
    path('vacancies/employer/', EmployerVacancyListView.as_view(), name='employer_vacancies'),
    path('vacancies/<int:pk>/edit/', VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('vacancies/<int:pk>/delete/', VacancyDeleteView.as_view(), name='vacancy_delete'),
    path('vacancies/favorite/<int:pk>/', ToggleFavoriteVacancyView.as_view(), name='vacancy_favorite'),
    path('vacancies/favorites/', FavoriteVacanciesListView.as_view(), name='favorites_vacancies'),
    path('create_vacancy/', views.VacancyCreateView.as_view(), name='create_vacancy'),


    path('applications/employer/', EmployerApplicationListView.as_view(), name='applications_for_employer'),
    path('applications/applicant/', ApplicantApplicationListView.as_view(), name='applications_for_applicant'),
    path('applications/employer/change_status/<int:application_id>', ApplicationsChangeStatusView.as_view(),
         name='change_application_status'),
]
