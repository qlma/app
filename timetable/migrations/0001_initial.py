from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('subject_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='timetable.Subject')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='timetable.Course')),
                ('group_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('weekday', models.CharField(max_length=1)),
                ('starts_at', models.TimeField()),
                ('ends_at', models.TimeField()),
            ],
        )
    ]
