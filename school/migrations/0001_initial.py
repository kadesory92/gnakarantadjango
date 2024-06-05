# Generated by Django 5.0.3 on 2024-06-05 21:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('service', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Founder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('female', 'Féminin'), ('male', 'Masculin')], max_length=100)),
                ('phone', models.CharField(max_length=200)),
                ('bio', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='founders/photos')),
                ('document', models.FileField(blank=True, null=True, upload_to='founders/documents')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('public', 'Ecole Publique'), ('private', 'Ecole Privée')], max_length=200)),
                ('category', models.CharField(choices=[('primary_education', 'Enseignement primaire'), ('secondary_education', 'Enseignement Seconaire')], max_length=200)),
                ('level', models.CharField(choices=[('primary', 'Primaire'), ('college_cycle', 'Collège'), ('high_school_cycle', 'Lycée'), ('primary_college', 'Ecole Primaire et Collège'), ('college_high_school', 'Collège et lycée'), ('general_level', 'Tous les niveaux')], max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('address_email', models.EmailField(blank=True, max_length=200, null=True)),
                ('site_web', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='schools/images')),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direction_of_education', to='service.service')),
                ('founder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.founder')),
                ('ire', models.ForeignKey(choices=[('ire_boke', 'IRE BOKE'), ('ire_conakry', 'Conakry'), ('ire_faranah', 'IRE FARANAH'), ('ire_kankan', 'IRE KANKAN'), ('ire_kindia', 'IRE KINDIA'), ('ire_labe', 'IRE LABE'), ('ire_mamou', 'IRE MAMOU'), ('ire_nzerekore', "IRE N'ZEREKORE")], on_delete=django.db.models.deletion.CASCADE, related_name='inspection_regional', to='service.service')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=200)),
                ('firstname', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('female', 'Féminin'), ('male', 'Masculin')], max_length=200)),
                ('phone', models.CharField(max_length=200)),
                ('position', models.CharField(max_length=200)),
                ('formation', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='staffs/images')),
                ('certificate', models.FileField(blank=True, null=True, upload_to='staffs/documents')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
