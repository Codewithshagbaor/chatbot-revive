# Generated by Django 5.0.1 on 2024-02-07 06:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0002_faq_qid'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.CharField(default='UID5304866270', max_length=13)),
                ('name', models.CharField(max_length=255)),
                ('profile_pic', models.ImageField(default='/user_profile_pics/3.jpg', upload_to='user_profile_pics')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Offline', 'Offline')], max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]