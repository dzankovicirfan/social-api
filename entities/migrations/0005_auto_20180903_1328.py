# Generated by Django 2.1 on 2018-09-03 11:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('entities', '0004_auto_20180821_1618'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('post', 'user')},
        ),
    ]
