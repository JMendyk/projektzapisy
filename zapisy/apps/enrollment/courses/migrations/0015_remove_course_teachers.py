# Generated by Django 2.0.8 on 2019-03-07 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20190212_1313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teachers',
        ),
    ]