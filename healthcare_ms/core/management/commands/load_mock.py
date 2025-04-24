import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from healthcare_ms.users.models import User
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact


fake = Faker()


class Command(BaseCommand):
    help = 'Creates mock data for patients, insurance, and emergency contacts'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old patient-related data...")
        # Delete objects related to patients first to avoid potential FK issues
        ins_del_count, _ = Insurance.objects.filter(patient__user_type='patient').delete()
        ec_del_count, _ = EmergencyContact.objects.filter(patient__user_type='patient').delete()
        prof_del_count, _ = PatientProfile.objects.all().delete()  # Delete all profiles
        # Now delete the patient and doctor users
        patient_del_count, _ = User.objects.filter(user_type='patient').delete()
        doctor_del_count, _ = User.objects.filter(user_type='doctor').delete()  # Delete old doctors too for linking
        self.stdout.write(f"Deleted: {ins_del_count} insurances, {ec_del_count} contacts, {prof_del_count} profiles, {patient_del_count} patients, {doctor_del_count} doctors.")

        # Verify deletion
        if PatientProfile.objects.exists():
            self.stdout.write(self.style.WARNING("Warning: Patient profiles still exist after deletion attempt!"))
        if User.objects.filter(user_type='patient').exists():
            self.stdout.write(self.style.WARNING("Warning: Patient users still exist after deletion attempt!"))

        self.stdout.write("Creating mock doctors...")
        doctors = []
        for i in range(3):
            doctor_username = f'doctor{i + 1}'
            doctor_email = f'doctor{i + 1}@clinic.com'
            if not User.objects.filter(username=doctor_username).exists():
                doctor = User.objects.create_user(
                    username=doctor_username,
                    email=doctor_email,
                    password='password123',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    user_type='doctor',
                    is_verified=True
                )
                doctors.append(doctor)
                self.stdout.write(f"Created doctor: {doctor.username}")
            else:
                doctors.append(User.objects.get(username=doctor_username))
                self.stdout.write(f"Doctor {doctor_username} already exists.")

        self.stdout.write("Creating mock patients and related data...")
        num_patients = 15
        for i in range(num_patients):
            # Create Patient User
            patient_username = f'patient{i + 1}'
            patient_email = f'patient{i + 1}@example.com'
            if User.objects.filter(username=patient_username).exists():
                self.stdout.write(f"Patient {patient_username} already exists. Skipping...")
                continue

            patient_user = User.objects.create_user(
                username=patient_username,
                email=patient_email,
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:15],
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                address=fake.address(),
                user_type='patient',
                is_verified=True
            )
            self.stdout.write(f"Created patient user: {patient_user.username}")

            # Create Patient Profile only if it doesn't exist (Safeguard)
            if not PatientProfile.objects.filter(user=patient_user).exists():
                PatientProfile.objects.create(
                    user=patient_user,
                    gender=random.choice(['male', 'female']),
                    blood_type=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                    height=random.uniform(150, 200),
                    weight=random.uniform(50, 120),
                    allergies=fake.sentence() if random.random() > 0.5 else '',
                    chronic_conditions=fake.sentence() if random.random() > 0.5 else '',
                    primary_doctor=random.choice(doctors) if doctors else None
                )
                self.stdout.write(f"  - Created profile for {patient_user.username}")
            else:
                self.stdout.write(self.style.WARNING(f"  - Profile for {patient_user.username} (ID: {patient_user.id}) already exists. Skipping creation."))

            # Create Insurance (1-2 per patient)
            for _ in range(random.randint(1, 2)):
                start_date = fake.date_between(start_date='-2y', end_date='today')
                end_date = start_date + timedelta(days=365) if random.random() > 0.2 else None
                Insurance.objects.create(
                    patient=patient_user,
                    provider=fake.company() + ' Insurance',
                    policy_number=fake.bothify(text='POL#########'),
                    group_number=fake.bothify(text='GRP####'),
                    coverage_start_date=start_date,
                    coverage_end_date=end_date,
                    is_active=end_date is None or end_date >= date.today()
                )
            self.stdout.write(f"  - Created insurance for {patient_user.username}")

            # Create Emergency Contacts (1-3 per patient)
            is_primary_set = False
            for j in range(random.randint(1, 3)):
                is_primary = False
                if not is_primary_set and j == 0:  # Ensure at least one primary if possible
                    is_primary = True
                    is_primary_set = True

                EmergencyContact.objects.create(
                    patient=patient_user,
                    name=fake.name(),
                    relationship=random.choice(['Spouse', 'Parent', 'Sibling', 'Friend', 'Child']),
                    phone_number=fake.phone_number()[:15],
                    email=fake.email(),
                    address=fake.address(),
                    is_primary=is_primary
                )
            self.stdout.write(f"  - Created emergency contacts for {patient_user.username}")

        self.stdout.write(self.style.SUCCESS('Successfully created mock patient data.'))
