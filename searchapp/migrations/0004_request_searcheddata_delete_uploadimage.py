# Generated by Django 4.0.5 on 2022-07-26 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('searchapp', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploadedFile', models.FileField(upload_to='UploadImg/%Y/%m/%d')),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('done', models.BooleanField(default=False)),
                ('request_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SearchedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('img', models.FileField(upload_to='SearchedImg/%Y/%m/%d')),
                ('request', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='searchapp.request')),
            ],
        ),
        migrations.DeleteModel(
            name='UploadImage',
        ),
    ]
