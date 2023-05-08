from datetime import date

from django.core.management.base import BaseCommand, CommandError
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Closes admin user with next creds: admin pass1234'

    def handle(self, *args, **options):
        try:
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='pass1234',
                date_of_birth=date.today(),
                phone_number='+999999999999',
                is_staff=True,
                is_superuser=True,
                is_employer=True,
            )
        except Exception as ex:
            raise CommandError(f'Error : {ex}')
        self.stdout.write('Successfully created admin')
