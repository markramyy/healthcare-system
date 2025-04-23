from healthcare_ms.core.base_serializer import BaseSerializer

from healthcare_ms.billing.models import Service, Invoice, InvoiceItem, Payment, InsuranceClaim
from healthcare_ms.users.serializers import ListUserAdminSerializer
from healthcare_ms.appointment.serializers import AppointmentListSerializer
from healthcare_ms.patient.serializers import InsuranceListSerializer


class ServiceListSerializer(BaseSerializer):
    class Meta:
        model = Service
        fields = (
            'guid', 'code', 'name',
            'price', 'is_active', 'created', 'modified'
        )


class ServiceDetailSerializer(BaseSerializer):
    class Meta:
        model = Service
        fields = (
            'guid', 'code', 'name',
            'description', 'price', 'is_active',
            'created', 'modified'
        )


class ServiceCreateSerializer(BaseSerializer):
    class Meta:
        model = Service
        fields = (
            'guid', 'code', 'name', 'description', 'price'
        )


class ServiceUpdateSerializer(BaseSerializer):
    class Meta:
        model = Service
        fields = (
            'guid', 'code', 'name', 'description', 'price', 'is_active'
        )


class InvoiceItemListSerializer(BaseSerializer):
    service = ServiceListSerializer(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = (
            'guid', 'service', 'quantity',
            'unit_price', 'total_price', 'created', 'modified'
        )


class InvoiceItemDetailSerializer(BaseSerializer):
    service = ServiceListSerializer(read_only=True)

    class Meta:
        model = InvoiceItem
        fields = (
            'guid', 'service', 'quantity',
            'unit_price', 'total_price', 'description',
            'created', 'modified'
        )


class InvoiceItemCreateSerializer(BaseSerializer):
    class Meta:
        model = InvoiceItem
        fields = (
            'guid', 'service', 'quantity',
            'unit_price', 'total_price', 'description'
        )


class InvoiceItemUpdateSerializer(BaseSerializer):
    class Meta:
        model = InvoiceItem
        fields = (
            'guid', 'service', 'quantity',
            'unit_price', 'total_price', 'description'
        )


class InvoiceListSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)
    appointment = AppointmentListSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            'guid', 'patient', 'appointment',
            'invoice_number', 'issue_date', 'due_date',
            'total_amount', 'paid_amount', 'invoice_status',
            'is_active', 'created', 'modified'
        )


class InvoiceDetailSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)
    appointment = AppointmentListSerializer(read_only=True)
    items = InvoiceItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = (
            'guid', 'patient', 'appointment',
            'invoice_number', 'issue_date', 'due_date',
            'total_amount', 'paid_amount', 'invoice_status',
            'notes', 'items', 'is_active', 'created', 'modified'
        )


class InvoiceCreateSerializer(BaseSerializer):
    class Meta:
        model = Invoice
        fields = (
            'guid', 'patient', 'appointment',
            'invoice_number', 'issue_date', 'due_date',
            'total_amount', 'invoice_status', 'notes'
        )


class InvoiceUpdateSerializer(BaseSerializer):
    class Meta:
        model = Invoice
        fields = (
            'guid', 'patient', 'appointment',
            'invoice_number', 'issue_date', 'due_date',
            'total_amount', 'invoice_status', 'notes', 'is_active'
        )


class PaymentListSerializer(BaseSerializer):
    invoice = InvoiceListSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'guid', 'invoice', 'amount',
            'payment_date', 'payment_method',
            'created', 'modified'
        )


class PaymentDetailSerializer(BaseSerializer):
    invoice = InvoiceListSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            'guid', 'invoice', 'amount',
            'payment_date', 'payment_method',
            'transaction_id', 'notes',
            'created', 'modified'
        )


class PaymentCreateSerializer(BaseSerializer):
    class Meta:
        model = Payment
        fields = (
            'guid', 'invoice', 'amount',
            'payment_date', 'payment_method',
            'transaction_id', 'notes'
        )


class PaymentUpdateSerializer(BaseSerializer):
    class Meta:
        model = Payment
        fields = (
            'guid', 'invoice', 'amount',
            'payment_date', 'payment_method',
            'transaction_id', 'notes'
        )


class InsuranceClaimListSerializer(BaseSerializer):
    invoice = InvoiceListSerializer(read_only=True)
    insurance = InsuranceListSerializer(read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = (
            'guid', 'invoice', 'insurance',
            'claim_number', 'claim_date', 'amount_claimed',
            'amount_approved', 'insurance_status', 'created', 'modified'
        )


class InsuranceClaimDetailSerializer(BaseSerializer):
    invoice = InvoiceListSerializer(read_only=True)
    insurance = InsuranceListSerializer(read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = (
            'guid', 'invoice', 'insurance',
            'claim_number', 'claim_date', 'amount_claimed',
            'amount_approved', 'insurance_status', 'notes',
            'created', 'modified'
        )


class InsuranceClaimCreateSerializer(BaseSerializer):
    class Meta:
        model = InsuranceClaim
        fields = (
            'guid', 'invoice', 'insurance',
            'claim_number', 'claim_date', 'amount_claimed',
            'insurance_status', 'notes'
        )


class InsuranceClaimUpdateSerializer(BaseSerializer):
    class Meta:
        model = InsuranceClaim
        fields = (
            'guid', 'invoice', 'insurance',
            'claim_number', 'claim_date', 'amount_claimed',
            'amount_approved', 'insurance_status', 'notes'
        )
