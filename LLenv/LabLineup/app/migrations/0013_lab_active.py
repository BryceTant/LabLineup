# Generated by Django 2.2.7 on 2020-01-24 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_emailconfirmation'),
    ]

    operations = [
        migrations.AddField(
            model_name='lab',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]