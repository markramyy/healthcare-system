from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta

from healthcare_ms.billing.models import Service, Invoice, InvoiceItem, Payment, InsuranceClaim
from healthcare_ms.users.models import User
from healthcare_ms.appointment.models import Appointment
from healthcare_ms.patient.models import Insurance


class Command(BaseCommand):
    help = 'Generates mock data for billing section'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating mock billing data...')

        # Create Services
        services = [
            {
                'code': 'CONS-001',
                'name': 'General Consultation',
                'description': 'Standard doctor consultation',
                'price': Decimal('150.00')
            },
            {
                'code': 'SPEC-001',
                'name': 'Specialist Consultation',
                'description': 'Specialist doctor consultation',
                'price': Decimal('250.00')
            },
            {
                'code': 'LAB-001',
                'name': 'Blood Test',
                'description': 'Complete blood count test',
                'price': Decimal('100.00')
            },
            {
                'code': 'XRAY-001',
                'name': 'Chest X-Ray',
                'description': 'Standard chest x-ray',
                'price': Decimal('200.00')
            },
            {
                'code': 'MRI-001',
                'name': 'MRI Scan',
                'description': 'Full body MRI scan',
                'price': Decimal('800.00')
            },
            {
                'code': 'PHYS-001',
                'name': 'Physical Therapy',
                'description': 'One hour physical therapy session',
                'price': Decimal('120.00')
            },
            {
                'code': 'VACC-001',
                'name': 'Vaccination',
                'description': 'Standard vaccination',
                'price': Decimal('75.00')
            },
            {
                'code': 'EMER-001',
                'name': 'Emergency Room Visit',
                'description': 'Emergency room consultation and treatment',
                'price': Decimal('500.00')
            }
        ]

        created_services = []
        for service_data in services:
            service, created = Service.objects.get_or_create(
                code=service_data['code'],
                defaults=service_data
            )
            created_services.append(service)
            if created:
                self.stdout.write(f'Created service: {service}')

        # Get some patients and appointments
        patients = User.objects.filter(user_type='patient')[:5]
        appointments = Appointment.objects.all()[:10]
        insurances = Insurance.objects.all()[:3]

        if not patients.exists():
            self.stdout.write(self.style.ERROR('No patients found. Please create patients first.'))
            return

        if not appointments.exists():
            self.stdout.write(self.style.ERROR('No appointments found. Please create appointments first.'))
            return

        if not insurances.exists():
            self.stdout.write(self.style.ERROR('No insurance records found. Please create insurance records first.'))
            return

        # Create Invoices
        for patient in patients:
            # Create 2-3 invoices per patient
            for invoice_count in range(random.randint(2, 3)):
                appointment = random.choice(appointments)
                issue_date = timezone.now().date() - timedelta(days=random.randint(1, 30))
                due_date = issue_date + timedelta(days=30)

                invoice = Invoice.objects.create(
                    patient=patient,
                    appointment=appointment,
                    invoice_number=f'INV-{random.randint(10000, 99999)}',
                    issue_date=issue_date,
                    due_date=due_date,
                    total_amount=Decimal('0.00'),
                    paid_amount=Decimal('0.00'),
                    invoice_status=random.choice(['draft', 'sent', 'paid', 'overdue']),
                    notes=f'Invoice for appointment on {appointment.slot.date} at {appointment.slot.start_time}'
                )

                # Create 2-4 items per invoice
                total_amount = Decimal('0.00')
                for item_count in range(random.randint(2, 4)):
                    service = random.choice(created_services)
                    quantity = random.randint(1, 3)
                    unit_price = service.price
                    total_price = unit_price * quantity
                    total_amount += total_price

                    InvoiceItem.objects.create(
                        invoice=invoice,
                        service=service,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        description=f'{service.name} - {quantity} session(s)'
                    )

                # Update invoice total
                invoice.total_amount = total_amount

                # Create payment if invoice is paid
                if invoice.invoice_status == 'paid':
                    payment_amount = total_amount
                    invoice.paid_amount = payment_amount

                    Payment.objects.create(
                        invoice=invoice,
                        amount=payment_amount,
                        payment_date=issue_date + timedelta(days=random.randint(1, 5)),
                        payment_method=random.choice(['cash', 'credit_card', 'debit_card', 'bank_transfer']),
                        transaction_id=f'TRX-{random.randint(100000, 999999)}',
                        notes='Payment received'
                    )

                    # Create insurance claim for some paid invoices
                    if random.choice([True, False]):
                        insurance = random.choice(insurances)
                        InsuranceClaim.objects.create(
                            invoice=invoice,
                            insurance=insurance,
                            claim_number=f'CLM-{random.randint(10000, 99999)}',
                            claim_date=issue_date + timedelta(days=random.randint(1, 3)),
                            amount_claimed=total_amount * Decimal('0.8'),  # Insurance covers 80%
                            amount_approved=total_amount * Decimal('0.8'),
                            insurance_status='paid',
                            notes='Insurance claim processed and paid'
                        )

                invoice.save()

        self.stdout.write(self.style.SUCCESS('Successfully generated mock billing data'))