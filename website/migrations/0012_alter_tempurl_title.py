# Generated by Django 5.0.6 on 2024-11-10 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_tempurl_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempurl',
            name='title',
            field=models.TextField(max_length=255),
        ),
    ]
