from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, View, UpdateView, DeleteView, TemplateView
from django.contrib import messages

from accounts.mixins import EmployerRequiredMixin, ApplicantRequiredMixin
from accounts.services import NotificationsService
from jobs.forms import VacancyForm, VacancySearchForm
from jobs.models import Vacancy, Application
from emails import EmailService


class VacancyListView(ListView):
    model = Vacancy
    template_name = 'jobs/vacancy_list.html'

    def get_queryset(self):
        qs = Vacancy.objects.filter(status='published')

        form = VacancySearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            location = form.cleaned_data['location']
            min_salary = form.cleaned_data['min_salary']

            if query:
                qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))

            if location:
                qs = qs.filter(location__icontains=location)

            if min_salary:
                qs = qs.filter(salary__gte=min_salary)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = VacancySearchForm(self.request.GET)
        return context


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


class VacancyDeleteView(UserPassesTestMixin, DeleteView):
    model = Vacancy
    success_url = reverse_lazy('employer_vacancies')

    def test_func(self):
        vacancy = self.get_object()
        return self.request.user == vacancy.created_by

    def form_valid(self, form):
        # получаем объект вакансии
        vacancy = self.get_object()
        # сохраняем название вакансии для последующего использования в сообщении
        title = vacancy.title
        # вызываем метод удаления вакансии
        vacancy.delete()
        # добавляем сообщение об успешном удалении вакансии в контекст
        messages.success(self.request, f'The "{title}" vacancy has been deleted.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ApplicationCreateView(View):

    def post(self, request, vacancy_id):
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)

        if Application.objects.filter(applicant=request.user, vacancy=vacancy).exists():
            messages.error(request, 'You have already applied to this vacancy')
            return redirect('vacancy_detail', pk=vacancy.pk)

        message = request.POST.get('message', '')

        Application.objects.create(
            applicant=self.request.user,
            vacancy=vacancy,
            message=message,
        )
        messages.success(request, f'You have successfully applied for the vacancy: {vacancy.title}')

        NotificationsService.create_notification_for_user(
            recipient=vacancy.created_by,
            message=f"{request.user.first_name} {request.user.last_name} applied to vacancy: {vacancy.title}",
            vacancy=vacancy,
            sender=self.request.user,
        )

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
        return Application.objects.filter(applicant=user).order_by('-created_at')


class ApplicationsChangeStatusView(LoginRequiredMixin, EmployerRequiredMixin, View):
    def post(self, request, application_id):
        action = request.POST.get('action')
        message = request.POST.get('message')

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

        EmailService.send_application_response(application.vacancy.title, action, message, application.applicant.email)

        NotificationsService.create_notification_for_user(
            recipient=application.applicant,
            message=f"{request.user.first_name} {request.user.last_name} replied "
                    f"to you about vacancy: {application.vacancy.title}",
            vacancy=application.vacancy,
            sender=self.request.user,
        )

        application.response_message = message
        application.save()
        return redirect('applications_for_employer')


class ToggleFavoriteVacancyView(LoginRequiredMixin, View):
    def post(self, request, pk):
        vacancy = get_object_or_404(Vacancy, pk=pk)
        user = request.user
        if vacancy in user.favorite_vacancies.all():
            user.favorite_vacancies.remove(vacancy)
        else:
            user.favorite_vacancies.add(vacancy)
        return redirect(request.META.get('HTTP_REFERER', 'home'))


class FavoriteVacanciesListView(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'jobs/favorite_vacancies.html'

    def get_queryset(self):
        vacancies = self.request.user.favorite_vacancies.filter(status='published')
        return vacancies


class SearchView(TemplateView):
    template_name = "jobs/search.html"
