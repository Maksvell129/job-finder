from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.db import transaction

from accounts.models import Employer, Organization

User = get_user_model()


class BootstrapDateInput(DateInput):
    input_type = 'date'
    input_class = 'form-control'


# class ApplicantSignUpForm(UserCreationForm):
#     username = forms.CharField(max_length=150, min_length=6)
#     phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='BY', attrs={'class': 'form-control '}),
#                                     label='Phone Number', required=True, )
#     date_of_birth = forms.DateField(label='Date of birth',
#     widget=forms.DateInput(attrs={'input_type': 'date',
#                                                     'input_class': 'form-control'}))
#
#     class Meta:
#         model = get_user_model()
#         fields = ('first_name', 'last_name', 'email', 'username', 'phone_number', 'date_of_birth')
#         widgets = {
#             'email': forms.TextInput(
#                 attrs={
#                     'required': True,
#                 }
#             ),
#         }
#
#
# class EmployerSignUpForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ("username", "email")
#         widgets = {
#             'email': forms.TextInput(
#                 attrs={
#                     'required': True,
#                 }
#             ),
#         }
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_employer = True
#         if commit:
#             user.save()
#         return user

class UserSignUpForm(UserCreationForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='BY', attrs={'class': 'form-control '}),
                                    label='Phone Number', required=True, )
    date_of_birth = forms.DateField(label='Date of birth', widget=BootstrapDateInput())

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'username', 'phone_number', 'date_of_birth')
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'required': True,
                }
            ),
        }


class ApplicantSignUpForm(UserSignUpForm):
    username = forms.CharField(max_length=150, min_length=6)


class EmployerSignUpForm(UserSignUpForm):
    company_name = forms.CharField(max_length=255)
    company_address = forms.CharField(max_length=255)
    company_description = forms.CharField(widget=forms.Textarea)

    class Meta(UserSignUpForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'username', 'phone_number', 'date_of_birth',)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        user.save()
        organization = Organization.objects.create(
            name=self.cleaned_data.get('company_name'),
            address=self.cleaned_data.get('company_address'),
            description=self.cleaned_data.get('company_description'),
            head=user,
        )
        Employer.objects.create(
            user=user,
            organization=organization
        )
        return user
