# Generated by Django 5.0.6 on 2024-10-24 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_thesis_abstract_pdf_thesis_water_pdf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thesis',
            old_name='water_pdf',
            new_name='watermark_pdf',
        ),
    ]
