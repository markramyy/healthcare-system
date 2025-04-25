import random
from datetime import timedelta
from django.utils import timezone

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from healthcare_ms.users.models import User
from healthcare_ms.appointment.models import AppointmentType, AppointmentSlot, Appointment


fake = Faker()


class Command(BaseCommand):
    help = 'Creates mock data for appointment types, slots, and appointments'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old appointment data...")
        # Delete objects in reverse order to avoid FK issues
        Appointment.objects.all().delete()
        AppointmentSlot.objects.all().delete()
        AppointmentType.objects.all().delete()
        self.stdout.write("Deleted old appointment data.")

        # Get all doctors and patients
        doctors = User.objects.filter(user_type='doctor')
        patients = User.objects.filter(user_type='patient')

        if not doctors.exists() or not patients.exists():
            self.stdout.write(self.style.ERROR("No doctors or patients found. Please run load_mock.py first."))
            return

        self.stdout.write("Creating mock appointment types...")
        # Create appointment types
        appointment_types = []
        type_names = [
            ('General Checkup', 30),
            ('Follow-up Visit', 20),
            ('Consultation', 45),
            ('Emergency Visit', 60),
            ('Vaccination', 15),
            ('Physical Examination', 40),
            ('Specialist Consultation', 50)
        ]
        for name, duration in type_names:
            appointment_type = AppointmentType.objects.create(
                name=name,
                description=fake.text(max_nb_chars=200),
                duration=duration,
                is_active=True
            )
            appointment_types.append(appointment_type)
            self.stdout.write(f"Created appointment type: {name}")

        self.stdout.write("Creating mock appointment slots...")
        # Create appointment slots for the next 30 days
        today = timezone.now().date()
        for doctor in doctors:
            # Create 2-4 slots per day for each doctor
            for day in range(30):
                date = today + timedelta(days=day)
                num_slots = random.randint(2, 4)

                # Generate unique time slots for this doctor and date
                used_times = set()
                for _ in range(num_slots):
                    # Try to find an unused time slot
                    max_attempts = 10
                    for _ in range(max_attempts):
                        hour = random.randint(9, 16)
                        minute = random.choice([0, 15, 30, 45])
                        time_str = f"{hour:02d}:{minute:02d}"

                        if time_str not in used_times:
                            used_times.add(time_str)
                            start_time = timezone.datetime.strptime(time_str, "%H:%M").time()
                            end_time = timezone.datetime.strptime(time_str, "%H:%M").time()

                            try:
                                AppointmentSlot.objects.create(
                                    doctor=doctor,
                                    date=date,
                                    start_time=start_time,
                                    end_time=end_time,
                                    is_available=random.choice([True, False])
                                )
                                break
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"Failed to create slot: {e}"))
                                continue

                self.stdout.write(f"Created slots for {doctor.username} on {date}")

        self.stdout.write("Creating mock appointments...")
        # Create appointments for each patient
        for patient in patients:
            # Create 1-3 appointments per patient
            num_appointments = random.randint(1, 3)
            for _ in range(num_appointments):
                # Get a random available slot
                available_slots = AppointmentSlot.objects.filter(
                    is_available=True,
                    date__gte=today
                )
                if not available_slots.exists():
                    continue

                slot = random.choice(available_slots)
                appointment_type = random.choice(appointment_types)
                doctor = slot.doctor

                # Create the appointment
                Appointment.objects.create(
                    patient=patient,
                    doctor=doctor,
                    appointment_type=appointment_type,
                    slot=slot,
                    appointment_status=random.choice(['scheduled', 'confirmed', 'completed']),
                    reason=fake.text(max_nb_chars=200),
                    notes=fake.text(max_nb_chars=200) if random.random() > 0.5 else ''
                )

                # Mark the slot as unavailable
                slot.is_available = False
                slot.save()

                self.stdout.write(f"Created appointment for {patient.username} with {doctor.username}")

        self.stdout.write(self.style.SUCCESS('Successfully created mock appointment data.'))