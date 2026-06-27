from django.db import migrations, models


def normalize_employee_branch(apps, schema_editor):
    Employee = apps.get_model('connect', 'Employee')
    Employee.objects.filter(branch='kunniyamuthur').update(branch='kuniyamuthur')


def restore_employee_branch(apps, schema_editor):
    Employee = apps.get_model('connect', 'Employee')
    Employee.objects.filter(branch='kuniyamuthur').update(branch='kunniyamuthur')


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0013_public_users'),
    ]

    operations = [
        migrations.RunPython(normalize_employee_branch, restore_employee_branch),
        migrations.AlterField(
            model_name='employee',
            name='branch',
            field=models.CharField(
                choices=[
                    ('100ft', '100ft Road'),
                    ('hopes', 'Hopes College'),
                    ('kuniyamuthur', 'Kuniyamuthur'),
                    ('other', 'Other Branch'),
                ],
                max_length=50,
            ),
        ),
    ]
