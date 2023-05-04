from django.urls import path

from accounts import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/applicant/', views.ApplicantSignUpView.as_view(), name='applicant_signup'),
    path('signup/employer/', views.EmployerSignUpView.as_view(), name='employer_signup'),
]
