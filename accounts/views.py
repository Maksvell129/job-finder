from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView

from accounts.forms import ApplicantSignUpForm, EmployerSignUpForm, EmployerEditForm, UserEditForm
from accounts.models import UserNotification
from accounts.services import NotificationsService

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
        context = {'form': form}
        return render(request, 'accounts/profile.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_employer:
            form = EmployerEditForm(request.POST, request.FILES, instance=request.user)
        else:
            form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        context = {'form': form}
        return render(request, 'accounts/profile.html', context)


@method_decorator(login_required, name='dispatch')
class NotificationListView(ListView):
    model = UserNotification
    template_name = 'accounts/notifications.html'
    context_object_name = "notifications"

    def get_queryset(self):
        user = self.request.user
        qs = NotificationsService.get_user_notifications(user=user)
        return qs


@login_required()
def user_unread_notifications(request: HttpRequest) -> HttpResponse:
    """
    Render unread user notifications
    """
    notifications = NotificationsService.get_user_unread_notifications(user=request.user)
    context = {
        "notifications": notifications,
    }
    return render(request, "accounts/notifications.html", context=context)


@login_required()
def change_notification_status(request: HttpRequest, notification_id: int) -> HttpResponseRedirect:
    """
    Change notification status
    """
    NotificationsService.change_status(request.user, notification_id)

    return redirect("user_notifications")


@login_required()
def mark_all_as_read(request: HttpRequest) -> HttpResponseRedirect:
    """
    Mark all notifications as read
    """
    NotificationsService.mark_all_as_read(request.user)
    return redirect("user_notifications")


@login_required()
def delete_read_notifications(request: HttpRequest) -> HttpResponseRedirect:
    """
    Delete read notifications
    """
    notifications = NotificationsService.get_user_read_notifications(user=request.user)
    notifications.delete()
    return redirect("user_notifications")


@login_required()
def delete_notification(request: HttpRequest, notification_id: int) -> HttpResponseRedirect:
    """
    Delete notification
    """
    notification = NotificationsService.get_notification(request.user, notification_id)
    notification.delete()

    return redirect("user_notifications")
