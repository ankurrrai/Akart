# Generated by Django 3.1 on 2025-01-11 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_ratingreview_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ratingreview',
            name='ip',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
