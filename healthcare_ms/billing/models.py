from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from healthcare_ms.core.models import DBBase
from healthcare_ms.users.models import User
from healthcare_ms.appointment.models import Appointment
from healthcare_ms.patient.models import Insurance


class Service(DBBase):
    code = models.CharField(max_length=20, unique=True, verbose_name=_('Service Code'))
    name = models.CharField(max_length=255, verbose_name=_('Service Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return f"{self.code} - {self.name}"


class Invoice(DBBase):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='invoices',
        limit_choices_to={'user_type': 'patient'},
        verbose_name=_('Patient')
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invoices',
        verbose_name=_('Appointment')
    )
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Invoice Number')
    )
    issue_date = models.DateField(verbose_name=_('Issue Date'))
    due_date = models.DateField(verbose_name=_('Due Date'))
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('Total Amount')
    )
    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name=_('Paid Amount')
    )
    invoice_status = models.CharField(
        max_length=20,
        choices=(
            ('draft', _('Draft')),
            ('sent', _('Sent')),
            ('paid', _('Paid')),
            ('overdue', _('Overdue')),
            ('cancelled', _('Cancelled')),
        ),
        default='draft',
        verbose_name=_('Status')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')
        ordering = ['-issue_date']

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.patient.get_full_name()}"

    @property
    def remaining_amount(self):
        return self.total_amount - self.paid_amount


class InvoiceItem(DBBase):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('Invoice')
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name='invoice_items',
        verbose_name=_('Service')
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Unit Price')
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Total Price')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Invoice Item')
        verbose_name_plural = _('Invoice Items')

    def __str__(self):
        return f"{self.service.name} - {self.quantity} x {self.unit_price}"


class Payment(DBBase):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name=_('Invoice')
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Amount')
    )
    payment_date = models.DateField(verbose_name=_('Payment Date'))
    payment_method = models.CharField(
        max_length=20,
        choices=(
            ('cash', _('Cash')),
            ('credit_card', _('Credit Card')),
            ('debit_card', _('Debit Card')),
            ('bank_transfer', _('Bank Transfer')),
            ('insurance', _('Insurance')),
        ),
        verbose_name=_('Payment Method')
    )
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Transaction ID')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payment of {self.amount} for Invoice {self.invoice.invoice_number}"


class InsuranceClaim(DBBase):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='insurance_claims',
        verbose_name=_('Invoice')
    )
    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.CASCADE,
        related_name='claims',
        verbose_name=_('Insurance')
    )
    claim_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Claim Number')
    )
    claim_date = models.DateField(verbose_name=_('Claim Date'))
    amount_claimed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Amount Claimed')
    )
    amount_approved = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Amount Approved')
    )
    insurance_status = models.CharField(
        max_length=20,
        choices=(
            ('submitted', _('Submitted')),
            ('processing', _('Processing')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
            ('paid', _('Paid')),
        ),
        default='submitted',
        verbose_name=_('Status')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta:
        verbose_name = _('Insurance Claim')
        verbose_name_plural = _('Insurance Claims')
        ordering = ['-claim_date']

    def __str__(self):
        return f"Claim {self.claim_number} - {self.insurance.provider}"
