from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, View, UpdateView
from django.contrib import messages

from accounts.mixins import EmployerRequiredMixin, ApplicantRequiredMixin
from jobs.forms import VacancyForm
from jobs.models import Vacancy, Application


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'jobs/vacancy_list.html'

    def get_queryset(self):
        return Vacancy.objects.all()


class VacancyCreateView(LoginRequiredMixin, EmployerRequiredMixin, CreateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'jobs/create_vacancy.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.organization = self.request.user.employer.organization
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'jobs/vacancy_detail.html'


@method_decorator(login_required, name='dispatch')
class ApplicationCreateView(View):

    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

        if Application.objects.filter(applicant=request.user, vacancy=vacancy).exists():
            messages.error(request, 'You have already applied to this vacancy')
            return redirect('vacancy_detail', pk=vacancy.pk)

        Application.objects.create(
            applicant=self.request.user,
            vacancy=vacancy
        )
        messages.success(request, 'You have successfully applied for the vacancy')
        return redirect('vacancy_detail', pk=vacancy.pk)


class EmployerVacancyListView(LoginRequiredMixin, EmployerRequiredMixin, ListView):
    model = Vacancy
    template_name = 'jobs/employer_vacancies.html'

    def get_queryset(self):
        user = self.request.user
        vacancies = Vacancy.objects.filter(organization=user.employer.organization)
        return vacancies


class VacancyUpdateView(EmployerRequiredMixin, UpdateView):
    model = Vacancy
    form_class = VacancyForm
    template_name = 'jobs/vacancy_form.html'
    success_url = reverse_lazy('employer_vacancies')


class EmployerApplicationListView(EmployerRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/employer_applications.html'

    def get_queryset(self):
        user = self.request.user
        vacancies = Vacancy.objects.filter(organization=user.employer.organization)
        applications = Application.objects.filter(vacancy__in=vacancies)
        return applications

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = context['object_list']
        pending_applications = applications.filter(status='pending')
        reviewed_applications = applications.exclude(status='pending')
        context['pending_applications'] = pending_applications
        context['reviewed_applications'] = reviewed_applications
        return context


class ApplicantApplicationListView(ApplicantRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/applicant_applications.html'

    def get_queryset(self):
        user = self.request.user
        return Application.objects.filter(applicant=user)


class ApplicationsChangeStatusView(LoginRequiredMixin, EmployerRequiredMixin, View):
    def post(self, request, application_id):
        action = request.POST.get('action')

        if not (application_id and action):
            return HttpResponseBadRequest('Invalid request')

        application = Application.objects.filter(id=application_id).first()
        if not application:
            return HttpResponseBadRequest('Invalid application')

        if application.status != 'pending':
            # Если статус отклика не "pending", то вернуть ошибку HTTP 400 (Bad Request)
            return HttpResponseBadRequest("You can only change the status of pending applications.")

        if action == 'approve':
            application.status = 'approved'
        elif action == 'reject':
            application.status = 'rejected'
        else:
            return HttpResponseBadRequest('Invalid action')

        application.save()
        return redirect('applications_for_employer')
