# Generated by Django 3.0.10 on 2020-10-10 16:07
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0006_notificationpreferencesteacher_thesis_voting_has_been_activated'),
    ]

    def DeleteDuplicates(apps, schema_editor):
        Model = apps.get_model('notifications', 'notificationpreferencesstudent')
        for row in Model.objects.all():
            if Model.objects.filter(user=row.user).count() > 1:
                row.delete()
        Model = apps.get_model('notifications', 'notificationpreferencesteacher')
        for row in Model.objects.all():
            if Model.objects.filter(user=row.user).count() > 1:
                row.delete()

    operations = [
        migrations.RunPython(DeleteDuplicates),
        migrations.AlterField(
            model_name='notificationpreferencesstudent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='użytkownik'),
        ),
        migrations.AlterField(
            model_name='notificationpreferencesteacher',
            name='thesis_voting_has_been_activated',
            field=models.BooleanField(default=True, verbose_name='Powiadomienie o głosowaniu (dotyczy członka Komisji Prac Dyplomowych)'),
        ),
        migrations.AlterField(
            model_name='notificationpreferencesteacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='użytkownik'),
        ),
    ]