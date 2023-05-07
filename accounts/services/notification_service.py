from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from accounts.models import UserNotification
from jobs.models import Vacancy

User = get_user_model()


class NotificationsService:
    @staticmethod
    def create_notification_for_user(recipient: User, message: str, vacancy: Vacancy, sender: User = None) -> None:
        UserNotification.objects.create(
            recipient=recipient,
            message=message,
            sender=sender,
            vacancy=vacancy,
            created_by=sender,
        )

    @staticmethod
    def get_user_notifications(user: User) -> QuerySet[UserNotification]:
        """
        Get user notifications
        """
        return UserNotification.objects.filter(recipient=user).order_by("-id")

    @staticmethod
    def get_user_unread_notifications(user: User) -> QuerySet[UserNotification]:
        """
        Get unread user notifications
        """
        return NotificationsService.get_user_notifications(user).filter(status=UserNotification.UNREAD)

    @staticmethod
    def get_user_read_notifications(user: User) -> QuerySet[UserNotification]:
        """
        Get read user notifications
        """
        return NotificationsService.get_user_notifications(user).filter(status=UserNotification.READ)

    @staticmethod
    def get_notification(recipient: User, notification_id: int) -> UserNotification:
        """
        Get notification by id
        """
        return UserNotification.objects.filter(id=notification_id, recipient=recipient).first()

    @staticmethod
    def change_status(recipient: User, notification_id: int) -> None:
        """
        Mark notification as read
        """
        notification = NotificationsService.get_notification(recipient, notification_id)
        if notification.status == UserNotification.READ:
            notification.status = UserNotification.UNREAD
        else:
            notification.status = UserNotification.READ
        notification.save()

    @staticmethod
    def mark_all_as_read(user: User) -> None:
        """
        Mark all notifications as read
        """
        notifications = NotificationsService.get_user_notifications(user)
        notifications.update(status=UserNotification.READ)

    @staticmethod
    def mark_as_read(notification: UserNotification) -> UserNotification:
        """
        Mark notification as read
        """
        notification.status = UserNotification.READ
        return notification.save()
