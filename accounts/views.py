from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView

from accounts.forms import ApplicantSignUpForm, EmployerSignUpForm

User = get_user_model()


def index(request):
    return render(request, 'accounts/index.html')


class SignUpView(TemplateView):
    template_name = 'registration/sign_up.html'


class ApplicantSignUpView(CreateView):
    model = User
    form_class = ApplicantSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'applicant'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')
