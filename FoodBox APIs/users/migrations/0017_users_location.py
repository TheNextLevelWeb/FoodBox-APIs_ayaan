# Generated by Django 4.2.3 on 2024-05-29 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_users_name_alter_users_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='location',
            field=models.CharField(default='India', max_length=30),
        ),
    ]
