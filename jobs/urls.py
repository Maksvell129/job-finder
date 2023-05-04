from django.urls import path

from jobs import views

urlpatterns = [
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('vacancies/<int:pk>/', views.VacancyDetailView.as_view(), name='vacancy_detail'),
    path('create_vacancy/', views.VacancyCreateView.as_view(), name='create_vacancy'),
]
