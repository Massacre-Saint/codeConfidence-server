# Generated by Django 4.1.7 on 2023-04-04 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ccapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='tech',
            new_name='learned_tech',
        ),
    ]