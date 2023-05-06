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

        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class VacancySearchForm(forms.Form):
    query = forms.CharField(label='Keywords', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='Location', required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    min_salary = forms.DecimalField(label='Minimum Salary', required=False,
                                    widget=forms.TextInput(attrs={'class': 'form-control'}))
