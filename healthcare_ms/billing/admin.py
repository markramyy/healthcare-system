from django.contrib import admin
from healthcare_ms.billing.models import Service, Invoice, InvoiceItem, Payment, InsuranceClaim


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code', 'name', 'description')


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    raw_id_fields = ('service',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'patient', 'issue_date', 'due_date', 'total_amount', 'paid_amount', 'status')
    list_filter = ('status', 'issue_date', 'due_date')
    search_fields = ('invoice_number', 'patient__username', 'patient__first_name', 'patient__last_name')
    date_hierarchy = 'issue_date'
    raw_id_fields = ('patient', 'appointment')
    inlines = [InvoiceItemInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'amount', 'payment_date', 'payment_method', 'transaction_id')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('transaction_id', 'invoice__invoice_number', 'invoice__patient__username')
    date_hierarchy = 'payment_date'
    raw_id_fields = ('invoice',)


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ('claim_number', 'invoice', 'insurance', 'claim_date', 'amount_claimed', 'amount_approved', 'status')
    list_filter = ('status', 'claim_date')
    search_fields = ('claim_number', 'invoice__invoice_number', 'insurance__provider')
    date_hierarchy = 'claim_date'
    raw_id_fields = ('invoice', 'insurance')
