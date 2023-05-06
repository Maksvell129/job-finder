from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView

from accounts.forms import ApplicantSignUpForm, EmployerSignUpForm, EmployerEditForm, UserEditForm

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


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_employer:
            form = EmployerEditForm(instance=request.user)
        else:
            form = UserEditForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'user_form': form, 'employer_form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_employer:
            form = EmployerEditForm(request.POST, instance=request.user)
        else:
            form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'user_form': form, 'employer_form': form})
