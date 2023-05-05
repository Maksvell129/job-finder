from django import template

register = template.Library()


@register.filter
def has_applied(vacancy, user):
    return vacancy.responses.filter(applicant=user).exists()
