# Generated by Django 5.1.2 on 2024-12-08 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_assignment_people_involved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
