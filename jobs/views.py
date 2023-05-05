from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, View
from django.contrib import messages

from accounts.mixins import EmployerRequiredMixin
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
