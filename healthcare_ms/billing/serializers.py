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


class ServiceCreateUpdateSerializer(BaseSerializer):
    class Meta:
        model = Service
        fields = (
            'guid', 'code', 'name', 'description', 'price'
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


class InvoiceItemCreateUpdateSerializer(BaseSerializer):
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
            'total_amount', 'paid_amount', 'status',
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
            'total_amount', 'paid_amount', 'status',
            'notes', 'items', 'is_active', 'created', 'modified'
        )


class InvoiceCreateUpdateSerializer(BaseSerializer):
    class Meta:
        model = Invoice
        fields = (
            'guid', 'patient', 'appointment',
            'invoice_number', 'issue_date', 'due_date',
            'total_amount', 'status', 'notes'
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


class PaymentCreateUpdateSerializer(BaseSerializer):
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
            'amount_approved', 'status', 'created', 'modified'
        )


class InsuranceClaimDetailSerializer(BaseSerializer):
    invoice = InvoiceListSerializer(read_only=True)
    insurance = InsuranceListSerializer(read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = (
            'guid', 'invoice', 'insurance',
            'claim_number', 'claim_date', 'amount_claimed',
            'amount_approved', 'status', 'notes',
            'created', 'modified'
        )


class InsuranceClaimCreateUpdateSerializer(BaseSerializer):
    class Meta:
        model = InsuranceClaim
        fields = (
            'guid', 'invoice', 'insurance',
            'claim_number', 'claim_date', 'amount_claimed',
            'status', 'notes'
        )
