# Generated by Django 4.2 on 2023-05-07 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_favoritevacancy_customuser_favorite_vacancies'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='resume',
            field=models.FileField(null=True, upload_to='resume/'),
        ),
    ]