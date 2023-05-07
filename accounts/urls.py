from django.urls import path


from accounts.views import ProfileView, SignUpView, ApplicantSignUpView, EmployerSignUpView, NotificationListView, \
    change_notification_status, delete_notification, mark_all_as_read, user_unread_notifications, \
    delete_read_notifications

urlpatterns = [
    # path('home', views.index, name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/applicant/', ApplicantSignUpView.as_view(), name='applicant_signup'),
    path('signup/employer/', EmployerSignUpView.as_view(), name='employer_signup'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path("notifications/", NotificationListView.as_view(), name="user_notifications"),
    path("unread_notifications/", user_unread_notifications, name="user_unread_notifications"),
    path("notifications/change_status/<int:notification_id>/", change_notification_status,
         name="change_notification_status"),
    path("notifications/mark_all_as_read/", mark_all_as_read, name="mark_all_as_read"),
    path("notifications/delete_notifications/", delete_read_notifications, name="delete_read_notifications"),
    path("notifications/delete_notification/<int:notification_id>/", delete_notification, name="delete_notification"),
]
