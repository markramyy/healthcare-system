from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from decimal import Decimal

from healthcare_ms.users.models import User
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.appointment.models import AppointmentType, AppointmentSlot, Appointment
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription
from healthcare_ms.billing.models import Service, Invoice, InvoiceItem, Payment, InsuranceClaim


class Command(BaseCommand):
    help = 'Load mock data including users, patients, doctors, appointments, medical records, and billing data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to load mock data...')

        # Create superuser
        self._create_superuser()

        # Create users
        doctors = self._create_doctors()
        patients = self._create_patients()

        # Create patient profiles and related data
        self._create_patient_profiles(patients, doctors)

        # Create appointment types and slots
        appointment_types = self._create_appointment_types()
        self._create_appointment_slots(doctors)

        # Create appointments
        self._create_appointments(patients, doctors, appointment_types)

        # Create medical records and related data
        self._create_medical_records(patients, doctors)

        # Create billing data
        self._create_billing_data(patients, doctors)

        self.stdout.write(self.style.SUCCESS('Successfully loaded all mock data'))

    def _create_superuser(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@admin.com',
                password='1',
                user_type='admin'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))

    def _create_doctors(self):
        doctors = []
        doctor_data = [
            {'username': 'dr_smith', 'first_name': 'John', 'last_name': 'Smith', 'email': 'dr.smith@hospital.com'},
            {'username': 'dr_johnson', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'dr.johnson@hospital.com'},
            {'username': 'dr_williams', 'first_name': 'Michael', 'last_name': 'Williams', 'email': 'dr.williams@hospital.com'},
        ]

        for data in doctor_data:
            if not User.objects.filter(username=data['username']).exists():
                doctor = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='1',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    user_type='doctor',
                    is_verified=True
                )
                doctors.append(doctor)
                self.stdout.write(self.style.SUCCESS(f'Created doctor: {doctor.get_full_name()}'))

        return doctors

    def _create_patients(self):
        patients = []
        patient_data = [
            {'username': 'patient1', 'first_name': 'Emma', 'last_name': 'Wilson', 'email': 'emma.wilson@example.com'},
            {'username': 'patient2', 'first_name': 'James', 'last_name': 'Brown', 'email': 'james.brown@example.com'},
            {'username': 'patient3', 'first_name': 'Olivia', 'last_name': 'Davis', 'email': 'olivia.davis@example.com'},
        ]

        for data in patient_data:
            if not User.objects.filter(username=data['username']).exists():
                patient = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='1',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    user_type='patient',
                    is_verified=True
                )
                patients.append(patient)
                self.stdout.write(self.style.SUCCESS(f'Created patient: {patient.get_full_name()}'))

        return patients

    def _create_patient_profiles(self, patients, doctors):
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

        for patient in patients:
            if not hasattr(patient, 'patient_profile'):
                PatientProfile.objects.create(
                    user=patient,
                    blood_type=random.choice(blood_types),
                    height=Decimal(random.uniform(150, 190)),
                    weight=Decimal(random.uniform(50, 100)),
                    allergies='Pollen, Dust',
                    chronic_conditions='None',
                    primary_doctor=random.choice(doctors)
                )

                # Create insurance
                Insurance.objects.create(
                    patient=patient,
                    provider='Blue Cross Blue Shield',
                    policy_number=f'BCBS{random.randint(100000, 999999)}',
                    group_number=f'GRP{random.randint(1000, 9999)}',
                    coverage_start_date=timezone.now().date() - timedelta(days=365),
                    coverage_end_date=timezone.now().date() + timedelta(days=365),
                    is_active=True
                )

                # Create emergency contact
                EmergencyContact.objects.create(
                    patient=patient,
                    name=f'Emergency Contact for {patient.get_full_name()}',
                    relationship='Spouse',
                    phone_number=f'+1{random.randint(1000000000, 9999999999)}',
                    email=f'emergency.{patient.username}@example.com',
                    address='123 Emergency St, City, State',
                    is_primary=True
                )

                self.stdout.write(self.style.SUCCESS(f'Created patient profile for: {patient.get_full_name()}'))

    def _create_appointment_types(self):
        types = []
        type_data = [
            {'name': 'General Checkup', 'duration': 30, 'description': 'Routine health checkup'},
            {'name': 'Specialist Consultation', 'duration': 45, 'description': 'Consultation with a specialist'},
            {'name': 'Follow-up Visit', 'duration': 20, 'description': 'Follow-up appointment'},
        ]

        for data in type_data:
            type_obj, created = AppointmentType.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                types.append(type_obj)
                self.stdout.write(self.style.SUCCESS(f'Created appointment type: {type_obj.name}'))

        return types

    def _create_appointment_slots(self, doctors):
        today = timezone.now().date()
        for i in range(7):  # Create slots for next 7 days
            date = today + timedelta(days=i)
            for doctor in doctors:
                for hour in range(9, 17):  # 9 AM to 5 PM
                    if not AppointmentSlot.objects.filter(
                        doctor=doctor,
                        date=date,
                        start_time=f'{hour}:00'
                    ).exists():
                        AppointmentSlot.objects.create(
                            doctor=doctor,
                            date=date,
                            start_time=f'{hour}:00',
                            end_time=f'{hour + 1}:00',
                            is_available=True
                        )

    def _create_appointments(self, patients, doctors, appointment_types):
        slots = AppointmentSlot.objects.filter(is_available=True)
        for patient in patients:
            for _ in range(2):  # Create 2 appointments per patient
                if slots.exists():
                    slot = random.choice(slots)
                    Appointment.objects.create(
                        patient=patient,
                        doctor=slot.doctor,
                        appointment_type=random.choice(appointment_types),
                        slot=slot,
                        status='scheduled',
                        reason='Regular checkup'
                    )
                    slot.is_available = False
                    slot.save()

    def _create_medical_records(self, patients, doctors):
        for patient in patients:
            for _ in range(2):  # Create 2 medical records per patient
                record = MedicalRecord.objects.create(
                    patient=patient,
                    doctor=random.choice(doctors),
                    visit_date=timezone.now() - timedelta(days=random.randint(1, 30)),
                    symptoms='Fever, headache',
                    notes='Patient reported symptoms',
                    follow_up_date=timezone.now() + timedelta(days=30)
                )

                # Create diagnosis
                Diagnosis.objects.create(
                    medical_record=record,
                    diagnosis_code=f'ICD-{random.randint(1000, 9999)}',
                    description='Common cold',
                    severity=random.choice(['low', 'medium', 'high'])
                )

                # Create treatment
                Treatment.objects.create(
                    medical_record=record,
                    name='Rest and medication',
                    description='Take prescribed medication and rest',
                    start_date=record.visit_date,
                    end_date=record.visit_date + timedelta(days=7),
                    status='completed'
                )

                # Create prescription
                Prescription.objects.create(
                    medical_record=record,
                    medication_name='Acetaminophen',
                    dosage='500mg',
                    frequency='Every 6 hours',
                    duration='7 days',
                    instructions='Take with food',
                    is_active=True
                )

    def _create_billing_data(self, patients, doctors):
        # Create services
        services = []
        service_data = [
            {'code': 'CONSULT', 'name': 'Consultation', 'price': Decimal('100.00')},
            {'code': 'LABTEST', 'name': 'Laboratory Test', 'price': Decimal('150.00')},
            {'code': 'XRAY', 'name': 'X-Ray', 'price': Decimal('200.00')},
        ]

        for data in service_data:
            service, created = Service.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                services.append(service)

        # Create invoices and related data
        for patient in patients:
            for _ in range(2):  # Create 2 invoices per patient
                invoice = Invoice.objects.create(
                    patient=patient,
                    invoice_number=f'INV{random.randint(100000, 999999)}',
                    issue_date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                    due_date=timezone.now().date() + timedelta(days=30),
                    total_amount=Decimal('0.00'),
                    status='sent'
                )

                # Add invoice items
                for service in random.sample(services, 2):
                    quantity = random.randint(1, 3)
                    unit_price = service.price
                    total_price = unit_price * quantity

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        service=service,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        description=f'{service.name} service'
                    )

                    invoice.total_amount += total_price

                invoice.save()

                # Create payment
                if random.choice([True, False]):
                    Payment.objects.create(
                        invoice=invoice,
                        amount=invoice.total_amount,
                        payment_date=invoice.issue_date + timedelta(days=random.randint(1, 10)),
                        payment_method=random.choice(['cash', 'credit_card', 'insurance']),
                        transaction_id=f'TXN{random.randint(100000, 999999)}'
                    )
                    invoice.paid_amount = invoice.total_amount
                    invoice.status = 'paid'
                    invoice.save()

                # Create insurance claim
                if random.choice([True, False]):
                    InsuranceClaim.objects.create(
                        invoice=invoice,
                        insurance=patient.insurance_policies.first(),
                        claim_number=f'CLM{random.randint(100000, 999999)}',
                        claim_date=invoice.issue_date,
                        amount_claimed=invoice.total_amount,
                        status=random.choice(['submitted', 'processing', 'approved'])
                    )
