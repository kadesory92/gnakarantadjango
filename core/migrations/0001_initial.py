# Generated by Django 5.0.3 on 2024-05-22 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('school', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StudyClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('coefficient', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_course', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.classroom')),
                ('study_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.studyclass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('female', 'Féminin'), ('male', 'Masculin')], max_length=10)),
                ('phone', models.CharField(max_length=200)),
                ('job', models.CharField(max_length=200, null=True)),
                ('position', models.CharField(max_length=200, null=True)),
                ('formation', models.CharField(max_length=200, null=True)),
                ('address', models.TextField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='parents/photos')),
                ('study_level', models.CharField(max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('description', models.TextField()),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('female', 'Féminin'), ('male', 'Masculin')], max_length=10)),
                ('phone', models.CharField(max_length=200)),
                ('birth_certificate', models.FileField(blank=True, null=True, upload_to='')),
                ('document', models.FileField(blank=True, null=True, upload_to='students/documents')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='students/photo')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
            ],
        ),
        migrations.CreateModel(
            name='Parenting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_bond', models.CharField(choices=[('mother', 'Mère'), ('father', 'Père'), ('sister', 'Soeur'), ('brother', 'Frère'), ('aunt', 'Tante'), ('uncle', 'Oncle')], max_length=200)),
                ('tutor', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.parent')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrollment', models.DateField()),
                ('last_school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_school', to='school.school')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_school', to='school.school')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
                ('last_study_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_class', to='core.studyclass')),
                ('study_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_class', to='core.studyclass')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=200)),
                ('type_exam', models.CharField(choices=[('MONTHLY', 'Mensuel'), ('QUARTERLY', 'Trimestriel'), ('SEMI_ANNUAL', 'Semestriel'), ('ANNUAL', 'Annuel')], max_length=200)),
                ('date_exam', models.DateField()),
                ('coefficient', models.IntegerField()),
                ('students', models.ManyToManyField(to='core.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('female', 'Féminin'), ('male', 'Masculin')], max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('status', models.CharField(choices=[('stat_official', 'Fonctionnaire'), ('private', 'Privé')], max_length=200)),
                ('form_level', models.CharField(max_length=100)),
                ('certificate', models.FileField(blank=True, null=True, upload_to='teachers/documents')),
                ('address', models.TextField(max_length=200)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='teachers/photos')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_commitment', models.DateField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teacher'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('student', 'Elève'), ('teacher', 'Professeur')], max_length=10)),
                ('status', models.CharField(choices=[('present', 'Présent'), ('absent', 'Absent')], max_length=10)),
                ('date', models.DateField()),
                ('justified', models.CharField(choices=[('yes', 'Oui'), ('no', 'Non')], max_length=3)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.student')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Teaching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_hours', models.IntegerField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.teacher')),
            ],
        ),
    ]
