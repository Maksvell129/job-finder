from django import forms
from .models import Vacancy


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'description', 'salary', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = True
        self.fields['salary'].required = True


class VacancySearchForm(forms.Form):
    query = forms.CharField(label='Keywords', required=False)
    location = forms.CharField(label='Location', required=False)
    min_salary = forms.DecimalField(label='Minimum Salary', required=False)
