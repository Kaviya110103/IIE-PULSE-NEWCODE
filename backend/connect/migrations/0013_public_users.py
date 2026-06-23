from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0012_ensure_quiztest_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('qualification', models.CharField(blank=True, max_length=120, null=True)),
                ('location', models.CharField(blank=True, max_length=160, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('username', models.CharField(max_length=120, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'public_users',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PublicUserActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('logout_time', models.DateTimeField(blank=True, null=True)),
                ('last_seen', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('public_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_logs', to='connect.publicuser')),
            ],
            options={
                'db_table': 'public_user_activity',
                'ordering': ['-login_time'],
            },
        ),
        migrations.CreateModel(
            name='PublicPracticeResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120)),
                ('quiz_id', models.IntegerField()),
                ('quiz_title', models.CharField(max_length=255)),
                ('score', models.FloatField(default=0)),
                ('total_marks', models.FloatField(default=0)),
                ('percentage', models.FloatField(default=0)),
                ('is_passed', models.BooleanField(default=False)),
                ('correct_count', models.IntegerField(default=0)),
                ('wrong_count', models.IntegerField(default=0)),
                ('attempted_count', models.IntegerField(default=0)),
                ('total_questions', models.IntegerField(default=0)),
                ('completed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('public_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='practice_results', to='connect.publicuser')),
            ],
            options={
                'db_table': 'public_practice_results',
                'ordering': ['-completed_at'],
            },
        ),
    ]
