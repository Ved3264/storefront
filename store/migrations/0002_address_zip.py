# Generated by Django 4.2.19 on 2025-03-04 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.IntegerField(default=0, max_length=6),
            preserve_default=False,
        ),
    ]
