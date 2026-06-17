from django.db import migrations, models
import django.db.models.deletion


def backfill_existing_material_assignments(apps, schema_editor):
    StudyMaterial = apps.get_model('connect', 'StudyMaterial')
    StudyMaterialAssignment = apps.get_model('connect', 'StudyMaterialAssignment')

    for material in StudyMaterial.objects.exclude(batch_id=None):
        StudyMaterialAssignment.objects.get_or_create(
            material_id=material.id,
            batch_id=material.batch_id,
            defaults={'assigned_by_id': material.uploaded_by_id},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0004_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studymaterial',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='connect.batches'),
        ),
        migrations.AddField(
            model_name='studymaterial',
            name='is_library',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='StudyMaterialAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='material_assignments_created', to='connect.employee')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material_assignments', to='connect.batches')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='connect.studymaterial')),
            ],
            options={
                'db_table': 'study_material_assignments',
                'ordering': ['-assigned_at'],
                'unique_together': {('material', 'batch')},
            },
        ),
        migrations.RunPython(backfill_existing_material_assignments, migrations.RunPython.noop),
    ]
