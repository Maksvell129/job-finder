from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from accounts.mixins import EmployerRequiredMixin
from jobs.forms import VacancyForm
from jobs.models import Vacancy


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
