from django.db import migrations


def ensure_quiztest_created_by(apps, schema_editor):
    table_names = schema_editor.connection.introspection.table_names()
    if 'QuizTest' not in table_names:
        return

    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(cursor, 'QuizTest')
        }
        if 'created_by_id' not in columns:
            cursor.execute('ALTER TABLE "QuizTest" ADD COLUMN "created_by_id" bigint NULL')


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0011_ensure_fee_and_counselor_announcement_tables'),
    ]

    operations = [
        migrations.RunPython(ensure_quiztest_created_by, migrations.RunPython.noop),
    ]
