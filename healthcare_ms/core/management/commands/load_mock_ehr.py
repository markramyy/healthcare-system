import random
from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from healthcare_ms.users.models import User
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription


fake = Faker()


class Command(BaseCommand):
    help = 'Creates mock data for medical records, diagnoses, treatments, and prescriptions'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old EHR data...")
        Prescription.objects.all().delete()
        Treatment.objects.all().delete()
        Diagnosis.objects.all().delete()
        MedicalRecord.objects.all().delete()
        self.stdout.write("Deleted old EHR data.")

        doctors = User.objects.filter(user_type='doctor')
        patients = User.objects.filter(user_type='patient')

        if not doctors.exists() or not patients.exists():
            self.stdout.write(self.style.ERROR("No doctors or patients found. Please run load_mock.py first."))
            return

        self.stdout.write("Creating mock medical records and related data...")

        for patient in patients:
            num_records = random.randint(2, 5)
            for _ in range(num_records):
                doctor = random.choice(doctors)

                visit_date = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())
                record = MedicalRecord.objects.create(
                    patient=patient,
                    doctor=doctor,
                    visit_date=visit_date,
                    symptoms=fake.text(max_nb_chars=200),
                    notes=fake.text(max_nb_chars=500),
                    follow_up_date=visit_date + timedelta(days=random.randint(7, 30)) if random.random() > 0.3 else None
                )
                self.stdout.write(f"Created medical record for {patient.username}")

                for _ in range(random.randint(1, 3)):
                    Diagnosis.objects.create(
                        medical_record=record,
                        diagnosis_code=fake.bothify(text='ICD-10-####'),
                        description=fake.text(max_nb_chars=200),
                        severity=random.choice(['low', 'medium', 'high', 'critical'])
                    )
                self.stdout.write(f"  - Created diagnoses for record {record.id}")

                for _ in range(random.randint(1, 2)):
                    start_date = record.visit_date
                    end_date = start_date + timedelta(days=random.randint(7, 90)) if random.random() > 0.2 else None
                    Treatment.objects.create(
                        medical_record=record,
                        name=fake.word().capitalize() + ' ' + fake.word(),
                        description=fake.text(max_nb_chars=200),
                        start_date=start_date,
                        end_date=end_date,
                        treatment_status=random.choice(['planned', 'in_progress', 'completed', 'cancelled'])
                    )
                self.stdout.write(f"  - Created treatments for record {record.id}")

                for _ in range(random.randint(1, 3)):
                    Prescription.objects.create(
                        medical_record=record,
                        medication_name=fake.word().capitalize() + ' ' + fake.word(),
                        dosage=fake.bothify(text='###mg'),
                        frequency=fake.random_element(['Once daily', 'Twice daily', 'Three times daily', 'Every 6 hours']),
                        duration=fake.random_element(['7 days', '14 days', '30 days', 'As needed']),
                        instructions=fake.text(max_nb_chars=200),
                        is_active=random.choice([True, False])
                    )
                self.stdout.write(f"  - Created prescriptions for record {record.id}")

        self.stdout.write(self.style.SUCCESS('Successfully created mock EHR data.'))
