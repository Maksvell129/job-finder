from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.db import transaction
from django.utils.translation import gettext_lazy as _
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


class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, min_length=6)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='BY', attrs={'class': 'form-control '}),
                                    label='Phone Number', required=True, )
    date_of_birth = forms.DateField(label='Date of birth', widget=BootstrapDateInput())

    resume = forms.FileField(label='Upload resume', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'resume']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True


class EmployerEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, min_length=6)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='BY', attrs={'class': 'form-control '}),
                                    label='Phone Number', required=True, )
    date_of_birth = forms.DateField(label='Date of birth', widget=BootstrapDateInput())

    organization_name = forms.CharField(label=_('Organization name'), max_length=255, required=False)
    organization_address = forms.CharField(label=_('Organization address'), max_length=255, required=False)
    organization_description = forms.CharField(label=_('Organization description'),
                                               widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'date_of_birth']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        if self.instance.is_employer:
            try:
                self.initial['organization_name'] = self.instance.employer.organization.name
                self.initial['organization_address'] = self.instance.employer.organization.address
                self.initial['organization_description'] = self.instance.employer.organization.description
            except Organization.DoesNotExist:
                pass

    def save(self, commit=True):
        user = super().save(commit=False)

        if user.is_employer:
            organization_name = self.cleaned_data.get('organization_name')
            organization_address = self.cleaned_data.get('organization_address')
            organization_description = self.cleaned_data.get('organization_description')

            organization = user.employer.organization
            organization.name = organization_name
            organization.address = organization_address
            organization.description = organization_description
            organization.save()

        if commit:
            user.save()

        return user
