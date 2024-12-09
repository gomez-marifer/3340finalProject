# Generated by Django 5.1.2 on 2024-12-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_assignment_collaborators_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='status',
            field=models.CharField(choices=[('Assigned', 'Assigned'), ('Pending', 'Pending'), ('Completed', 'Completed'), ('Unable to Complete', 'Unable to Complete')], default='Assigned', max_length=20),
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
