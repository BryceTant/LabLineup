# Generated by Django 2.2.7 on 2019-11-15 03:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_labcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labcode',
            name='code',
            field=models.CharField(default=uuid.uuid4, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
