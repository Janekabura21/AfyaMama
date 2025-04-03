# Generated by Django 5.1.7 on 2025-04-02 19:15

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildProfile',
            fields=[
                ('id', models.CharField(help_text='Unique identification number of the mother', max_length=20, primary_key=True, serialize=False, verbose_name="Mother's ID Number")),
                ('name', models.CharField(max_length=100)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('date_of_birth', models.DateField(default=datetime.date.today)),
                ('gestation_at_birth', models.PositiveIntegerField(blank=True, null=True)),
                ('birth_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('birth_length', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('birth_order', models.PositiveIntegerField(blank=True, null=True)),
                ('date_first_seen', models.DateField(default=datetime.date.today)),
                ('place_of_birth', models.CharField(choices=[('Home', 'Home'), ('Hospital', 'Hospital'), ('Other', 'Other')], max_length=20)),
                ('health_facility_name', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_notification_no', models.CharField(blank=True, max_length=20, null=True)),
                ('immunization_registration_no', models.CharField(blank=True, max_length=20, null=True)),
                ('child_welfare_clinic_no', models.CharField(blank=True, max_length=20, null=True)),
                ('master_facility_code', models.CharField(blank=True, max_length=20, null=True)),
                ('birth_certificate_no', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_registration', models.DateField(blank=True, null=True)),
                ('place_of_registration', models.CharField(blank=True, max_length=100, null=True)),
                ('fathers_name', models.CharField(blank=True, max_length=100, null=True)),
                ('fathers_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('mothers_phone', models.CharField(max_length=20)),
                ('guardian_name', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('residence', models.CharField(max_length=100)),
                ('county', models.CharField(max_length=100)),
                ('division', models.CharField(blank=True, max_length=100, null=True)),
                ('sub_county', models.CharField(blank=True, max_length=100, null=True)),
                ('town', models.CharField(blank=True, max_length=100, null=True)),
                ('estate_village', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_address', models.CharField(blank=True, max_length=100, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Child Profile',
                'verbose_name_plural': 'Child Profiles',
                'ordering': ['date_of_birth'],
            },
        ),
        migrations.CreateModel(
            name='MaternalProfile',
            fields=[
                ('identification_number', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Mother ID/National ID')),
                ('name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gravida', models.IntegerField()),
                ('parity', models.IntegerField()),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField()),
                ('lmp', models.DateField()),
                ('edd', models.DateField()),
                ('marital_status', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')], max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('subcounty', models.CharField(blank=True, max_length=50, null=True)),
                ('ward', models.CharField(blank=True, max_length=50, null=True)),
                ('town_village', models.CharField(blank=True, max_length=100, null=True)),
                ('physical_address', models.CharField(blank=True, max_length=100, null=True)),
                ('telephone', models.CharField(max_length=15)),
                ('guardian_id', models.CharField(blank=True, max_length=20, null=True)),
                ('huduma_number', models.CharField(blank=True, max_length=20, null=True)),
                ('education_level', models.CharField(blank=True, max_length=50, null=True)),
                ('next_of_kin_name', models.CharField(max_length=100)),
                ('next_of_kin_relationship', models.CharField(max_length=50)),
                ('next_of_kin_phone', models.CharField(max_length=15)),
                ('surgical_operation', models.BooleanField(default=False)),
                ('diabetes', models.BooleanField(default=False)),
                ('hypertension', models.BooleanField(default=False)),
                ('blood_transfusion', models.BooleanField(default=False)),
                ('drug_allergy', models.BooleanField(default=False)),
                ('other_allergies', models.TextField(blank=True, null=True)),
                ('family_history_twins', models.BooleanField(default=False)),
                ('family_history_tb', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MotherChildRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalExamination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_pressure', models.CharField(help_text='e.g., 118/65 mmHg', max_length=10)),
                ('pulse_rate', models.PositiveIntegerField(help_text='Beats per minute')),
                ('cvs', models.TextField(blank=True, null=True)),
                ('respiratory_system', models.TextField(blank=True, null=True)),
                ('breasts', models.TextField(blank=True, null=True)),
                ('abdomen', models.TextField(blank=True, null=True)),
                ('genital_examination', models.TextField(blank=True, null=True)),
                ('discharge_or_ulcer', models.BooleanField(default=False, help_text='Check if present')),
                ('hemoglobin', models.FloatField(help_text='g/dl')),
                ('blood_group', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=3)),
                ('rhesus_factor', models.CharField(choices=[('TR+', 'TR+'), ('TR-', 'TR-')], max_length=5)),
                ('urinalysis', models.CharField(blank=True, max_length=50, null=True)),
                ('blood_rbs', models.FloatField(blank=True, help_text='Random blood sugar', null=True)),
                ('tb_screening_outcome', models.BooleanField(default=False, help_text='True = Positive, False = Negative')),
                ('ipt_given_date', models.DateField(blank=True, null=True)),
                ('ipt_next_visit', models.DateField(blank=True, null=True)),
                ('scan_first_date', models.DateField(blank=True, help_text='Before 24 weeks', null=True)),
                ('scan_second_date', models.DateField(blank=True, help_text='Third trimester', null=True)),
                ('hiv_status', models.CharField(choices=[('Reactive', 'Reactive'), ('Non-Reactive', 'Non-Reactive'), ('Not Tested', 'Not Tested')], default='Not Tested', max_length=20)),
                ('syphilis_status', models.CharField(choices=[('Reactive', 'Reactive'), ('Non-Reactive', 'Non-Reactive'), ('Not Tested', 'Not Tested')], default='Not Tested', max_length=20)),
                ('hepatitis_b_status', models.CharField(choices=[('Reactive', 'Reactive'), ('Non-Reactive', 'Non-Reactive'), ('Not Tested', 'Not Tested')], default='Not Tested', max_length=20)),
                ('couple_testing_done', models.BooleanField(default=False)),
                ('partner_hiv_status', models.CharField(choices=[('Reactive', 'Reactive'), ('Non-Reactive', 'Non-Reactive'), ('Not Tested', 'Not Tested')], default='Not Tested', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.CharField(choices=[('ANC, Childbirth and Postnatal Care', 'ANC, Childbirth and Postnatal Care'), ('Maternal Profile', 'Maternal Profile'), ('Medical & Surgical History', 'Medical & Surgical History'), ('Previous Pregnancy', 'Previous Pregnancy'), ('Antenatal Profile', 'Antenatal Profile'), ('Weight Monitoring Chart', 'Weight Monitoring Chart'), ('Clinical Notes', 'Clinical Notes'), ('Malaria Prophylaxis', 'Malaria Prophylaxis'), ('Maternal Serology Testing', 'Maternal Serology Testing'), ('Infant Feeding', 'Infant Feeding'), ('Danger Signs During Pregnancy', 'Danger Signs During Pregnancy'), ('Positioning for Breastfeeding', 'Positioning for Breastfeeding'), ('Child Health Monitoring', 'Child Health Monitoring'), ('Developmental Milestones', 'Developmental Milestones'), ('Growth Monitoring', 'Growth Monitoring'), ('Immunization', 'Immunization'), ('Vitamin A Supplementation', 'Vitamin A Supplementation'), ('Deworming', 'Deworming'), ('PMTCT of HIV/Syphilis/Hepatitis B', 'PMTCT of HIV/Syphilis/Hepatitis B'), ('Recommendations for Child Care', 'Recommendations for Child Care')], max_length=255)),
                ('details', models.TextField(blank=True)),
                ('child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='MamaCare.childprofile')),
                ('mother', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='health_records', to='MamaCare.maternalprofile')),
            ],
        ),
        migrations.AddField(
            model_name='childprofile',
            name='mothers_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='MamaCare.maternalprofile'),
        ),
        migrations.CreateModel(
            name='PreviousPregnancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregnancy_order', models.IntegerField()),
                ('year', models.IntegerField()),
                ('anc_visits', models.IntegerField()),
                ('place_of_birth', models.CharField(max_length=255)),
                ('gestation_weeks', models.IntegerField()),
                ('labour_duration', models.CharField(max_length=50)),
                ('mode_of_delivery', models.CharField(max_length=50)),
                ('birth_weight', models.IntegerField()),
                ('sex', models.CharField(max_length=10)),
                ('outcome', models.CharField(max_length=50)),
                ('puerperium', models.CharField(max_length=50)),
                ('mother', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_pregnancies', to='MamaCare.maternalprofile')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('hospital_name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('role', models.CharField(choices=[('Doctor', 'Doctor'), ('Nurse', 'Nurse'), ('Admin', 'Admin')], max_length=10)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('contact_number', models.CharField(max_length=15)),
                ('medical_history', models.TextField(blank=True, null=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=255)),
                ('experience_years', models.IntegerField()),
                ('qualifications', models.TextField()),
                ('availability', models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Consultant', 'Consultant')], default='Full-time', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Cancelled', 'Cancelled'), ('Completed', 'Completed')], default='Pending', max_length=20)),
                ('attended', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
                ('maternal_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='appointments', to='MamaCare.maternalprofile')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='MamaCare.patient')),
                ('doctor', models.ForeignKey(blank=True, limit_choices_to={'role': 'Doctor'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to=settings.AUTH_USER_MODEL)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
