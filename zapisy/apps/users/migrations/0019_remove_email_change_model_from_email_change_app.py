# Generated by Django 2.1.13 on 2019-12-10 14:55

from django.db import migrations

DROP_EMAIL_CHANGE_REQUEST_TABLE = """\
    DROP TABLE IF EXISTS email_change_emailchangerequest CASCADE;
"""


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20191209_1255'),
    ]

    operations = [
        migrations.RunSQL(DROP_EMAIL_CHANGE_REQUEST_TABLE)
    ]