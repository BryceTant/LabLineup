# Generated by Django 2.2.7 on 2019-11-22 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0008_auto_20191114_2259'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notifyNew', models.BooleanField(default=False)),
                ('notifyThreshold', models.IntegerField(blank=True, null=True)),
                ('lid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Lab')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]