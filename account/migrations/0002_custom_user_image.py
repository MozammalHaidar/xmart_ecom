# Generated by Django 5.2 on 2025-05-09 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='custom_user',
            name='image',
            field=models.ImageField(blank=True, default='def.png', null=True, upload_to='profile_fics/'),
        ),
    ]
