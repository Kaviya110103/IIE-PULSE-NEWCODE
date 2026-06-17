from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedstudent',
            name='completion_type',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('partial', 'Partial Completion - Reassigned'),
                    ('full', 'Full Completion - Graduated'),
                ],
                default='full',
            ),
        ),
    ]
