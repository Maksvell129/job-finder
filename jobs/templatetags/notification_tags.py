from django import template

register = template.Library()


@register.filter
def count_unread_notifications(user) -> int:
    """
    Count unread user notifications
    """
    return user.recipient_notifications.filter(status=1).count()
