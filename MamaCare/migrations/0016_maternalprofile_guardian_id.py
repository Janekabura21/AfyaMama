# Generated by Django 5.1.7 on 2025-03-27 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MamaCare', '0015_childprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='maternalprofile',
            name='guardian_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
