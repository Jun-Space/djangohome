# Generated by Django 3.1.4 on 2020-12-18 04:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201217_2352'),
    ]

    operations = [
        migrations.RenameField(
            model_name='interest',
            old_name='owner',
            new_name='subscriber',
        ),
    ]