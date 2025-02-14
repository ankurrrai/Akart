# Generated by Django 3.1 on 2025-01-09 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='phone',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='city',
            new_name='pin_code',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[['new', 'new'], ['new', 'new'], ['new', 'new'], ['new', 'new']], default='New', max_length=100),
        ),
    ]
