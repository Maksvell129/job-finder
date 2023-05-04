from django.contrib.auth.mixins import UserPassesTestMixin


class EmployerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.is_employer
