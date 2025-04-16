from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from healthcare_ms.billing.models import Service, Invoice, InvoiceItem, Payment, InsuranceClaim
from healthcare_ms.billing.serializers import (
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceCreateSerializer,
    ServiceUpdateSerializer,
    InvoiceListSerializer,
    InvoiceDetailSerializer,
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    InvoiceItemListSerializer,
    InvoiceItemDetailSerializer,
    InvoiceItemCreateSerializer,
    InvoiceItemUpdateSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentCreateSerializer,
    PaymentUpdateSerializer,
    InsuranceClaimListSerializer,
    InsuranceClaimDetailSerializer,
    InsuranceClaimCreateSerializer,
    InsuranceClaimUpdateSerializer
)


@login_required
def service_list(request):
    services = Service.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        services = services.filter(
            Q(code__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(services, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = ServiceListSerializer(page_obj, many=True)

    return render(request, 'billing/service_list.html', {
        'services': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def service_detail(request, guid):
    service = get_object_or_404(Service, guid=guid)
    serializer = ServiceDetailSerializer(service)
    return render(request, 'billing/service_detail.html', {
        'service': service,
        'serialized_data': serializer.data
    })


@login_required
def service_create(request):
    if request.method == 'POST':
        serializer = ServiceCreateSerializer(data=request.POST)
        if serializer.is_valid():
            service = serializer.save()
            messages.success(request, 'Service created successfully.')
            return redirect('billing:service-detail', guid=service.guid)
        else:
            messages.error(request, 'Failed to create service.')
    else:
        serializer = ServiceCreateSerializer()

    return render(request, 'billing/service_form.html', {
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def service_update(request, guid):
    service = get_object_or_404(Service, guid=guid)

    if request.method == 'POST':
        serializer = ServiceUpdateSerializer(service, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Service updated successfully.')
            return redirect('billing:service-detail', guid=service.guid)
        else:
            messages.error(request, 'Failed to update service.')
    else:
        serializer = ServiceUpdateSerializer(service)

    return render(request, 'billing/service_form.html', {
        'service': service,
        'serialized_data': serializer.data
    })


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        invoices = invoices.filter(
            Q(patient__username__icontains=search_query) |
            Q(invoice_number__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = InvoiceListSerializer(page_obj, many=True)

    return render(request, 'billing/invoice_list.html', {
        'invoices': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def invoice_detail(request, guid):
    invoice = get_object_or_404(Invoice, guid=guid)
    serializer = InvoiceDetailSerializer(invoice)
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
        'serialized_data': serializer.data
    })


@login_required
def invoice_create(request):
    if request.method == 'POST':
        serializer = InvoiceCreateSerializer(data=request.POST)
        if serializer.is_valid():
            invoice = serializer.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('billing:invoice-detail', guid=invoice.guid)
        else:
            messages.error(request, 'Failed to create invoice.')
    else:
        serializer = InvoiceCreateSerializer()

    return render(request, 'billing/invoice_form.html', {
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def invoice_update(request, guid):
    invoice = get_object_or_404(Invoice, guid=guid)

    if request.method == 'POST':
        serializer = InvoiceUpdateSerializer(invoice, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Invoice updated successfully.')
            return redirect('billing:invoice-detail', guid=invoice.guid)
        else:
            messages.error(request, 'Failed to update invoice.')
    else:
        serializer = InvoiceUpdateSerializer(invoice)

    return render(request, 'billing/invoice_form.html', {
        'invoice': invoice,
        'serialized_data': serializer.data
    })


@login_required
def payment_list(request):
    payments = Payment.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        payments = payments.filter(
            Q(invoice__invoice_number__icontains=search_query) |
            Q(transaction_id__icontains=search_query) |
            Q(payment_method__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(payments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = PaymentListSerializer(page_obj, many=True)

    return render(request, 'billing/payment_list.html', {
        'payments': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def payment_detail(request, guid):
    payment = get_object_or_404(Payment, guid=guid)
    serializer = PaymentDetailSerializer(payment)
    return render(request, 'billing/payment_detail.html', {
        'payment': payment,
        'serialized_data': serializer.data
    })


@login_required
def payment_create(request):
    if request.method == 'POST':
        serializer = PaymentCreateSerializer(data=request.POST)
        if serializer.is_valid():
            payment = serializer.save()
            messages.success(request, 'Payment created successfully.')
            return redirect('billing:payment-detail', guid=payment.guid)
        else:
            messages.error(request, 'Failed to create payment.')
    else:
        serializer = PaymentCreateSerializer()

    return render(request, 'billing/payment_form.html', {
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def payment_update(request, guid):
    payment = get_object_or_404(Payment, guid=guid)

    if request.method == 'POST':
        serializer = PaymentUpdateSerializer(payment, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Payment updated successfully.')
            return redirect('billing:payment-detail', guid=payment.guid)
        else:
            messages.error(request, 'Failed to update payment.')
    else:
        serializer = PaymentUpdateSerializer(payment)

    return render(request, 'billing/payment_form.html', {
        'payment': payment,
        'serialized_data': serializer.data
    })


@login_required
def insurance_claim_list(request):
    claims = InsuranceClaim.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        claims = claims.filter(
            Q(claim_number__icontains=search_query) |
            Q(insurance__provider__icontains=search_query) |
            Q(status__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(claims, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = InsuranceClaimListSerializer(page_obj, many=True)

    return render(request, 'billing/insurance_claim_list.html', {
        'claims': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def insurance_claim_detail(request, guid):
    claim = get_object_or_404(InsuranceClaim, guid=guid)
    serializer = InsuranceClaimDetailSerializer(claim)
    return render(request, 'billing/insurance_claim_detail.html', {
        'claim': claim,
        'serialized_data': serializer.data
    })


@login_required
def insurance_claim_create(request):
    if request.method == 'POST':
        serializer = InsuranceClaimCreateSerializer(data=request.POST)
        if serializer.is_valid():
            claim = serializer.save()
            messages.success(request, 'Insurance claim created successfully.')
            return redirect('billing:insurance-claim-detail', guid=claim.guid)
        else:
            messages.error(request, 'Failed to create insurance claim.')
    else:
        serializer = InsuranceClaimCreateSerializer()

    return render(request, 'billing/insurance_claim_form.html', {
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def insurance_claim_update(request, guid):
    claim = get_object_or_404(InsuranceClaim, guid=guid)

    if request.method == 'POST':
        serializer = InsuranceClaimUpdateSerializer(claim, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Insurance claim updated successfully.')
            return redirect('billing:insurance-claim-detail', guid=claim.guid)
        else:
            messages.error(request, 'Failed to update insurance claim.')
    else:
        serializer = InsuranceClaimUpdateSerializer(claim)

    return render(request, 'billing/insurance_claim_form.html', {
        'claim': claim,
        'serialized_data': serializer.data
    })


@login_required
def invoice_item_list(request):
    items = InvoiceItem.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        items = items.filter(
            Q(invoice__invoice_number__icontains=search_query) |
            Q(service__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = InvoiceItemListSerializer(page_obj, many=True)

    return render(request, 'billing/invoice_item_list.html', {
        'items': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def invoice_item_detail(request, guid):
    item = get_object_or_404(InvoiceItem, guid=guid)
    serializer = InvoiceItemDetailSerializer(item)
    return render(request, 'billing/invoice_item_detail.html', {
        'item': item,
        'serialized_data': serializer.data
    })


@login_required
def invoice_item_create(request):
    if request.method == 'POST':
        serializer = InvoiceItemCreateSerializer(data=request.POST)
        if serializer.is_valid():
            item = serializer.save()
            messages.success(request, 'Invoice item created successfully.')
            return redirect('billing:invoice-item-detail', guid=item.guid)
        else:
            messages.error(request, 'Failed to create invoice item.')
    else:
        serializer = InvoiceItemCreateSerializer()

    return render(request, 'billing/invoice_item_form.html', {
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def invoice_item_update(request, guid):
    item = get_object_or_404(InvoiceItem, guid=guid)

    if request.method == 'POST':
        serializer = InvoiceItemUpdateSerializer(item, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Invoice item updated successfully.')
            return redirect('billing:invoice-item-detail', guid=item.guid)
        else:
            messages.error(request, 'Failed to update invoice item.')
    else:
        serializer = InvoiceItemUpdateSerializer(item)

    return render(request, 'billing/invoice_item_form.html', {
        'item': item,
        'serialized_data': serializer.data
    })
