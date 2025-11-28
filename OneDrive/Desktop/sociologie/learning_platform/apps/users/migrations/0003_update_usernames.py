# Generated manually for data migration

from django.db import migrations


def update_usernames_to_emails(apps, schema_editor):
    CustomUser = apps.get_model('users', 'CustomUser')
    for user in CustomUser.objects.all():
        user.username = user.email
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.RunPython(update_usernames_to_emails),
    ]
