# Generated migration for adding URL field to Document model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_course_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='url',
            field=models.URLField(blank=True, help_text='Lien vers la documentation en ligne', null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]

