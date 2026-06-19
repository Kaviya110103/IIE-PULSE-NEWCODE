from django.db import migrations
from django.db.utils import OperationalError, ProgrammingError


def ensure_student_transfer_columns(apps, schema_editor):
    Students = apps.get_model('connect', 'Students')
    table_name = Students._meta.db_table
    quote_name = schema_editor.quote_name

    def existing_columns():
        with schema_editor.connection.cursor() as cursor:
            return {
                column.name
                for column in schema_editor.connection.introspection.get_table_description(cursor, table_name)
            }

    def add_column_if_missing(column_name, definition):
        if column_name in existing_columns():
            return
        try:
            schema_editor.execute(
                f'ALTER TABLE {quote_name(table_name)} ADD COLUMN {quote_name(column_name)} {definition}'
            )
        except (OperationalError, ProgrammingError) as exc:
            if 'duplicate column' not in str(exc).lower():
                raise

    add_column_if_missing('is_transferred', 'bool NOT NULL DEFAULT 0')
    add_column_if_missing('previous_trainer_id', 'bigint NULL')
    add_column_if_missing('previous_batch_id', 'bigint NULL')
    add_column_if_missing('transfer_date', 'datetime NULL')


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0009_ensure_course_type_table'),
    ]

    operations = [
        migrations.RunPython(ensure_student_transfer_columns, migrations.RunPython.noop),
    ]
