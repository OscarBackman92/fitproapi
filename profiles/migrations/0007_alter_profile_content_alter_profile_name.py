# Generated by Django 5.1.2 on 2024-12-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_remove_profile_id_alter_profile_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='content',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
