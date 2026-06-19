from django.db import migrations
from django.db.utils import OperationalError, ProgrammingError


def ensure_missing_tables(apps, schema_editor):
    existing_tables = set(schema_editor.connection.introspection.table_names())

    for model_name in ('FeePayment', 'FeeTransaction', 'FeePaymentRequest', 'CounselorAnnouncement'):
        model = apps.get_model('connect', model_name)
        if model._meta.db_table in existing_tables:
            continue
        try:
            schema_editor.create_model(model)
            existing_tables = set(schema_editor.connection.introspection.table_names())
        except (OperationalError, ProgrammingError) as exc:
            if 'already exists' not in str(exc).lower():
                raise


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0010_ensure_student_transfer_columns'),
    ]

    operations = [
        migrations.RunPython(ensure_missing_tables, migrations.RunPython.noop),
    ]
