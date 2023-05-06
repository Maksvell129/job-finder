from django import template

register = template.Library()


@register.filter
def has_applied(vacancy, user):
    return vacancy.responses.filter(applicant=user).exists()

#
# @register.filter(name='is_favorite')
# def is_favorite(vacancy, user):
#     return user.favorite_vacancies.filter(pk=vacancy.pk).exists()
