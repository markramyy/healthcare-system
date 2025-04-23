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
        self._create_staff()
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
                user_type='admin',
                is_verified=True,
                phone_number='+1234567890',
                date_of_birth='1980-01-01',
                address='123 Admin Street'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created superuser'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))

    def _create_doctors(self):
        doctors = []
        doctor_data = [
            {
                'username': 'dr_smith',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'dr.smith@hospital.com',
                'phone_number': '+1234567891',
                'date_of_birth': '1975-05-15',
                'address': '456 Doctor Lane'
            },
            {
                'username': 'dr_johnson',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'dr.johnson@hospital.com',
                'phone_number': '+1234567892',
                'date_of_birth': '1980-08-20',
                'address': '789 Medical Avenue'
            },
            {
                'username': 'dr_williams',
                'first_name': 'Michael',
                'last_name': 'Williams',
                'email': 'dr.williams@hospital.com',
                'phone_number': '+1234567893',
                'date_of_birth': '1978-03-10',
                'address': '321 Health Street'
            },
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
                    is_verified=True,
                    phone_number=data['phone_number'],
                    date_of_birth=data['date_of_birth'],
                    address=data['address']
                )
                doctors.append(doctor)
                self.stdout.write(self.style.SUCCESS(f'Created doctor: {doctor.get_full_name()}'))

        return doctors

    def _create_staff(self):
        staff = []
        staff_data = [
            {
                'username': 'staff_miller',
                'first_name': 'Robert',
                'last_name': 'Miller',
                'email': 'staff.miller@hospital.com',
                'phone_number': '+1234567896',
                'date_of_birth': '1990-04-05',
                'address': '741 Staff Avenue'
            },
            {
                'username': 'staff_anderson',
                'first_name': 'Jennifer',
                'last_name': 'Anderson',
                'email': 'staff.anderson@hospital.com',
                'phone_number': '+1234567897',
                'date_of_birth': '1992-09-30',
                'address': '852 Office Street'
            },
            {
                'username': 'staff_wilson',
                'first_name': 'David',
                'last_name': 'Wilson',
                'email': 'staff.wilson@hospital.com',
                'phone_number': '+1234567898',
                'date_of_birth': '1988-11-15',
                'address': '963 Admin Street'
            },
            {
                'username': 'staff_brown',
                'first_name': 'Sarah',
                'last_name': 'Brown',
                'email': 'staff.brown@hospital.com',
                'phone_number': '+1234567899',
                'date_of_birth': '1991-07-22',
                'address': '147 Staff Lane'
            },
            {
                'username': 'staff_davis',
                'first_name': 'Michael',
                'last_name': 'Davis',
                'email': 'staff.davis@hospital.com',
                'phone_number': '+1234567800',
                'date_of_birth': '1989-03-18',
                'address': '258 Office Avenue'
            }
        ]

        for data in staff_data:
            if not User.objects.filter(username=data['username']).exists():
                staff_member = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password='1',
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    user_type='staff',
                    is_verified=True,
                    phone_number=data['phone_number'],
                    date_of_birth=data['date_of_birth'],
                    address=data['address']
                )
                staff.append(staff_member)
                self.stdout.write(self.style.SUCCESS(f'Created staff: {staff_member.get_full_name()}'))

        return staff

    def _create_patients(self):
        patients = []
        patient_data = [
            {
                'username': 'patient1',
                'first_name': 'Emma',
                'last_name': 'Wilson',
                'email': 'emma.wilson@example.com',
                'phone_number': '+1234567898',
                'date_of_birth': '1995-02-15',
                'address': '159 Patient Street'
            },
            {
                'username': 'patient2',
                'first_name': 'James',
                'last_name': 'Brown',
                'email': 'james.brown@example.com',
                'phone_number': '+1234567899',
                'date_of_birth': '1988-07-20',
                'address': '357 Health Lane'
            },
            {
                'username': 'patient3',
                'first_name': 'Olivia',
                'last_name': 'Davis',
                'email': 'olivia.davis@example.com',
                'phone_number': '+1234567800',
                'date_of_birth': '1992-11-05',
                'address': '456 Wellness Avenue'
            },
            {
                'username': 'patient4',
                'first_name': 'Michael',
                'last_name': 'Johnson',
                'email': 'michael.johnson@example.com',
                'phone_number': '+1234567801',
                'date_of_birth': '1985-03-25',
                'address': '789 Health Street'
            },
            {
                'username': 'patient5',
                'first_name': 'Sophia',
                'last_name': 'Martinez',
                'email': 'sophia.martinez@example.com',
                'phone_number': '+1234567802',
                'date_of_birth': '1990-09-12',
                'address': '321 Wellness Lane'
            },
            {
                'username': 'patient6',
                'first_name': 'William',
                'last_name': 'Taylor',
                'email': 'william.taylor@example.com',
                'phone_number': '+1234567803',
                'date_of_birth': '1982-06-18',
                'address': '654 Medical Avenue'
            },
            {
                'username': 'patient7',
                'first_name': 'Isabella',
                'last_name': 'Anderson',
                'email': 'isabella.anderson@example.com',
                'phone_number': '+1234567804',
                'date_of_birth': '1993-04-30',
                'address': '987 Care Street'
            },
            {
                'username': 'patient8',
                'first_name': 'David',
                'last_name': 'Thomas',
                'email': 'david.thomas@example.com',
                'phone_number': '+1234567805',
                'date_of_birth': '1979-12-08',
                'address': '147 Health Avenue'
            },
            {
                'username': 'patient9',
                'first_name': 'Mia',
                'last_name': 'Jackson',
                'email': 'mia.jackson@example.com',
                'phone_number': '+1234567806',
                'date_of_birth': '1991-07-22',
                'address': '258 Wellness Road'
            },
            {
                'username': 'patient10',
                'first_name': 'Daniel',
                'last_name': 'White',
                'email': 'daniel.white@example.com',
                'phone_number': '+1234567807',
                'date_of_birth': '1987-01-14',
                'address': '369 Medical Lane'
            }
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
                    is_verified=True,
                    phone_number=data['phone_number'],
                    date_of_birth=data['date_of_birth'],
                    address=data['address']
                )
                patients.append(patient)
                self.stdout.write(self.style.SUCCESS(f'Created patient: {patient.get_full_name()}'))

        return patients

    def _create_patient_profiles(self, patients, doctors):
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        allergies = [
            'Pollen, Dust',
            'Penicillin, Shellfish',
            'Latex, Peanuts',
            'No known allergies',
            'Aspirin, Iodine'
        ]
        chronic_conditions = [
            'None',
            'Hypertension',
            'Diabetes Type 2',
            'Asthma',
            'Arthritis',
            'High Cholesterol'
        ]

        # Create a balanced distribution of genders
        genders = ['male', 'female']
        gender_distribution = {gender: 0 for gender in genders}

        # Distribute patients among doctors
        # Each doctor will have 3-4 patients
        patients_per_doctor = len(patients) // len(doctors)
        remaining_patients = len(patients) % len(doctors)

        for i, doctor in enumerate(doctors):
            # Calculate how many patients this doctor should have
            num_patients = patients_per_doctor + (1 if i < remaining_patients else 0)

            # Get the patients for this doctor
            start_idx = i * patients_per_doctor + min(i, remaining_patients)
            end_idx = start_idx + num_patients
            doctor_patients = patients[start_idx:end_idx]

            for patient in doctor_patients:
                if not hasattr(patient, 'patient_profile'):
                    # Ensure balanced gender distribution
                    gender = min(gender_distribution.items(), key=lambda x: x[1])[0]
                    gender_distribution[gender] += 1

                    # Create patient profile
                    PatientProfile.objects.create(
                        user=patient,
                        gender=gender,
                        blood_type=random.choice(blood_types),
                        height=Decimal(random.uniform(150, 190)),
                        weight=Decimal(random.uniform(50, 100)),
                        allergies=random.choice(allergies),
                        chronic_conditions=random.choice(chronic_conditions),
                        primary_doctor=doctor  # Assign this doctor as primary
                    )

                    # Create insurance policies (1-2 per patient)
                    insurance_providers = [
                        'Blue Cross Blue Shield',
                        'Aetna',
                        'UnitedHealthcare',
                        'Cigna',
                        'Humana'
                    ]
                    for _ in range(random.randint(1, 2)):
                        Insurance.objects.create(
                            patient=patient,
                            provider=random.choice(insurance_providers),
                            policy_number=f'POL{random.randint(100000, 999999)}',
                            group_number=f'GRP{random.randint(1000, 9999)}',
                            coverage_start_date=timezone.now().date() - timedelta(days=random.randint(30, 365)),
                            coverage_end_date=timezone.now().date() + timedelta(days=random.randint(180, 365)),
                            is_active=random.choice([True, False])
                        )

                    # Create emergency contacts (1-3 per patient)
                    relationships = ['Spouse', 'Parent', 'Sibling', 'Child', 'Friend']
                    for i in range(random.randint(1, 3)):
                        EmergencyContact.objects.create(
                            patient=patient,
                            name=f'Emergency Contact {i + 1} for {patient.get_full_name()}',
                            relationship=random.choice(relationships),
                            phone_number=f'+1{random.randint(1000000000, 9999999999)}',
                            email=f'emergency{i + 1}.{patient.username}@example.com',
                            address=f'{random.randint(1, 999)} Emergency St, City, State',
                            is_primary=(i == 0)  # First contact is primary
                        )

                    self.stdout.write(self.style.SUCCESS(
                        f'Created patient profile for: {patient.get_full_name()} with doctor: {doctor.get_full_name()}'
                    ))

    def _create_appointment_types(self):
        types = []
        type_data = [
            {
                'name': 'General Checkup',
                'duration': 30,
                'description': 'Routine health checkup'
            },
            {
                'name': 'Specialist Consultation',
                'duration': 45,
                'description': 'Consultation with a specialist'
            },
            {
                'name': 'Follow-up Visit',
                'duration': 20,
                'description': 'Follow-up appointment'
            },
            {
                'name': 'Emergency Visit',
                'duration': 60,
                'description': 'Emergency medical attention'
            },
            {
                'name': 'Vaccination',
                'duration': 15,
                'description': 'Vaccination appointment'
            },
            {
                'name': 'Physical Therapy',
                'duration': 45,
                'description': 'Physical therapy session'
            }
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
        for i in range(14):  # Create slots for next 14 days
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
                            is_available=random.choice([True, False])  # Random availability
                        )

    def _create_appointments(self, patients, doctors, appointment_types):
        slots = AppointmentSlot.objects.filter(is_available=True)
        appointment_statuses = ['scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show']
        reasons = [
            'Regular checkup',
            'Follow-up for previous condition',
            'New symptoms',
            'Medication review',
            'Test results discussion',
            'Emergency consultation'
        ]

        # Create a balanced distribution of appointment statuses
        status_distribution = {status: 0 for status in appointment_statuses}
        target_distribution = {
            'scheduled': 0.2,  # 20%
            'confirmed': 0.2,  # 20%
            'in_progress': 0.1,  # 10%
            'completed': 0.3,  # 30%
            'cancelled': 0.1,  # 10%
            'no_show': 0.1  # 10%
        }

        for patient in patients:
            for _ in range(random.randint(1, 3)):  # 1-3 appointments per patient
                if slots.exists():
                    slot = random.choice(slots)

                    # Choose status based on distribution
                    available_statuses = [
                        s for s in appointment_statuses
                        if status_distribution[s] < target_distribution[s] * len(patients) * 3
                    ]
                    if not available_statuses:
                        available_statuses = appointment_statuses
                    status = random.choice(available_statuses)
                    status_distribution[status] += 1

                    Appointment.objects.create(
                        patient=patient,
                        doctor=slot.doctor,
                        appointment_type=random.choice(appointment_types),
                        slot=slot,
                        appointment_status=status,
                        reason=random.choice(reasons),
                        notes=f'Patient notes for {patient.get_full_name()}'
                    )
                    slot.is_available = False
                    slot.save()

    def _create_medical_records(self, patients, doctors):
        symptoms_list = [
            'Fever, headache, fatigue',
            'Cough, shortness of breath',
            'Abdominal pain, nausea',
            'Joint pain, swelling',
            'Chest pain, dizziness',
            'Rash, itching',
            'Back pain, limited mobility'
        ]
        diagnosis_codes = [
            'J06.9',  # Upper respiratory infection
            'E11.9',  # Type 2 diabetes
            'I10',    # Essential hypertension
            'M54.5',  # Low back pain
            'J45.909'  # Asthma
        ]
        diagnosis_descriptions = [
            'Upper respiratory infection',
            'Type 2 diabetes mellitus',
            'Essential hypertension',
            'Chronic low back pain',
            'Asthma, unspecified'
        ]
        medications = [
            {'name': 'Acetaminophen', 'dosage': '500mg', 'frequency': 'Every 6 hours'},
            {'name': 'Ibuprofen', 'dosage': '400mg', 'frequency': 'Every 8 hours'},
            {'name': 'Amoxicillin', 'dosage': '500mg', 'frequency': 'Every 12 hours'},
            {'name': 'Lisinopril', 'dosage': '10mg', 'frequency': 'Once daily'},
            {'name': 'Metformin', 'dosage': '1000mg', 'frequency': 'Twice daily'}
        ]

        treatment_statuses = ['planned', 'in_progress', 'completed', 'cancelled']
        treatment_status_distribution = {status: 0 for status in treatment_statuses}
        target_treatment_distribution = {
            'planned': 0.2,  # 20%
            'in_progress': 0.3,  # 30%
            'completed': 0.4,  # 40%
            'cancelled': 0.1  # 10%
        }

        for patient in patients:
            for _ in range(random.randint(1, 3)):  # 1-3 medical records per patient
                visit_date = timezone.now() - timedelta(days=random.randint(1, 90))
                record = MedicalRecord.objects.create(
                    patient=patient,
                    doctor=random.choice(doctors),
                    visit_date=visit_date,
                    symptoms=random.choice(symptoms_list),
                    notes=f'Detailed notes for {patient.get_full_name()}\'s visit',
                    follow_up_date=visit_date + timedelta(days=random.randint(7, 30))
                )

                # Create diagnosis
                Diagnosis.objects.create(
                    medical_record=record,
                    diagnosis_code=random.choice(diagnosis_codes),
                    description=random.choice(diagnosis_descriptions),
                    severity=random.choice(['low', 'medium', 'high', 'critical'])
                )

                # Create treatment with balanced status distribution
                available_statuses = [
                    s for s in treatment_statuses
                    if treatment_status_distribution[s] < target_treatment_distribution[s] * len(patients) * 3
                ]
                if not available_statuses:
                    available_statuses = treatment_statuses
                treatment_status = random.choice(available_statuses)
                treatment_status_distribution[treatment_status] += 1

                Treatment.objects.create(
                    medical_record=record,
                    name=f'Treatment for {record.symptoms.split(",")[0]}',
                    description='Follow prescribed medication and lifestyle changes',
                    start_date=record.visit_date,
                    end_date=record.visit_date + timedelta(days=random.randint(7, 30)),
                    treatment_status=treatment_status
                )

                # Create prescription
                medication = random.choice(medications)
                Prescription.objects.create(
                    medical_record=record,
                    medication_name=medication['name'],
                    dosage=medication['dosage'],
                    frequency=medication['frequency'],
                    duration=f'{random.randint(7, 30)} days',
                    instructions='Take with food and plenty of water',
                    is_active=random.choice([True, False])
                )

    def _create_billing_data(self, patients, doctors):
        # Create services
        services = []
        service_data = [
            {'code': 'CONSULT', 'name': 'Consultation', 'price': Decimal('100.00')},
            {'code': 'LABTEST', 'name': 'Laboratory Test', 'price': Decimal('150.00')},
            {'code': 'XRAY', 'name': 'X-Ray', 'price': Decimal('200.00')},
            {'code': 'MRI', 'name': 'MRI Scan', 'price': Decimal('500.00')},
            {'code': 'PHYSIO', 'name': 'Physical Therapy', 'price': Decimal('120.00')},
            {'code': 'VACCINE', 'name': 'Vaccination', 'price': Decimal('80.00')}
        ]

        for data in service_data:
            service, created = Service.objects.get_or_create(
                code=data['code'],
                defaults=data
            )
            if created:
                services.append(service)

        # Create invoices and related data
        invoice_statuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled']
        invoice_status_distribution = {status: 0 for status in invoice_statuses}
        target_invoice_distribution = {
            'draft': 0.2,  # 20%
            'sent': 0.2,  # 20%
            'paid': 0.3,  # 30%
            'overdue': 0.2,  # 20%
            'cancelled': 0.1  # 10%
        }

        claim_statuses = ['submitted', 'processing', 'approved', 'rejected', 'paid']
        claim_status_distribution = {status: 0 for status in claim_statuses}
        target_claim_distribution = {
            'submitted': 0.2,  # 20%
            'processing': 0.2,  # 20%
            'approved': 0.2,  # 20%
            'rejected': 0.2,  # 20%
            'paid': 0.2  # 20%
        }

        for patient in patients:
            for _ in range(random.randint(1, 3)):  # 1-3 invoices per patient
                # Choose invoice status based on distribution
                available_statuses = [
                    s for s in invoice_statuses
                    if invoice_status_distribution[s] < target_invoice_distribution[s] * len(patients) * 3
                ]
                if not available_statuses:
                    available_statuses = invoice_statuses
                invoice_status = random.choice(available_statuses)
                invoice_status_distribution[invoice_status] += 1

                invoice = Invoice.objects.create(
                    patient=patient,
                    invoice_number=f'INV{random.randint(100000, 999999)}',
                    issue_date=timezone.now().date() - timedelta(days=random.randint(1, 30)),
                    due_date=timezone.now().date() + timedelta(days=random.randint(7, 30)),
                    total_amount=Decimal('0.00'),
                    invoice_status=invoice_status,
                    notes=f'Invoice notes for {patient.get_full_name()}'
                )

                # Add invoice items
                for service in random.sample(services, random.randint(1, 3)):
                    quantity = random.randint(1, 3)
                    unit_price = service.price
                    total_price = unit_price * quantity

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        service=service,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        description=f'{service.name} service for {patient.get_full_name()}'
                    )

                    invoice.total_amount += total_price

                invoice.save()

                # Create payment if invoice is paid
                payment_methods = ['cash', 'credit_card', 'debit_card', 'bank_transfer', 'insurance']
                if invoice.invoice_status == 'paid':
                    Payment.objects.create(
                        invoice=invoice,
                        amount=invoice.total_amount,
                        payment_date=invoice.issue_date + timedelta(days=random.randint(1, 10)),
                        payment_method=random.choice(payment_methods),
                        transaction_id=f'TXN{random.randint(100000, 999999)}',
                        notes=f'Payment notes for invoice {invoice.invoice_number}'
                    )
                    invoice.paid_amount = invoice.total_amount
                    invoice.save()

                # Create insurance claim
                insurance = patient.insurance_policies.first()
                if insurance and random.choice([True, False]):
                    # Choose claim status based on distribution
                    available_statuses = [
                        s for s in claim_statuses
                        if claim_status_distribution[s] < target_claim_distribution[s] * len(patients) * 3
                    ]
                    if not available_statuses:
                        available_statuses = claim_statuses
                    claim_status = random.choice(available_statuses)
                    claim_status_distribution[claim_status] += 1

                    InsuranceClaim.objects.create(
                        invoice=invoice,
                        insurance=insurance,
                        claim_number=f'CLM{random.randint(100000, 999999)}',
                        claim_date=invoice.issue_date,
                        amount_claimed=invoice.total_amount,
                        amount_approved=invoice.total_amount * Decimal('0.8'),  # 80% coverage
                        insurance_status=claim_status,
                        notes=f'Insurance claim notes for {patient.get_full_name()}'
                    )
