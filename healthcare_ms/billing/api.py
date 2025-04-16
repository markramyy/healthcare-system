from rest_framework.response import Response
from django.db.models import Q
from functools import reduce

from healthcare_ms.core.base_viewset import BaseViewSet
from healthcare_ms.billing.models import Service, Invoice, InvoiceItem, Payment, InsuranceClaim
from healthcare_ms.billing.serializers import (
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceCreateUpdateSerializer,
    InvoiceListSerializer,
    InvoiceDetailSerializer,
    InvoiceCreateUpdateSerializer,
    InvoiceItemListSerializer,
    InvoiceItemDetailSerializer,
    InvoiceItemCreateUpdateSerializer,
    PaymentListSerializer,
    PaymentDetailSerializer,
    PaymentCreateUpdateSerializer,
    InsuranceClaimListSerializer,
    InsuranceClaimDetailSerializer,
    InsuranceClaimCreateUpdateSerializer
)

import operator
import logging
logger = logging.getLogger(__name__)


class ServiceViewSet(BaseViewSet):
    queryset = Service.objects.all()
    search_fields = ['code', 'name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ServiceListSerializer
        elif self.action == 'retrieve':
            return ServiceDetailSerializer
        elif self.action in ['create', 'update']:
            return ServiceCreateUpdateSerializer

    def get_paginated_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            current_page = self.paginator.page.number
            last_page = self.paginator.page.paginator.num_pages

            return Response({
                "count": self.paginator.page.paginator.count,
                "page": current_page,
                "last_page": last_page,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "message": "Services displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Services displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        services = self.filter_queryset(self.get_queryset())

        if not services:
            return Response({
                "message": "No services found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            services = services.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(services, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            service = self.get_object()
        except Service.DoesNotExist:
            return Response({
                "message": "Service not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(service)
        return Response({
            "message": "Service displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Service created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create service.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        service = self.get_object()
        serializer = self.get_serializer_class()(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Service updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update service.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        service = self.get_object()
        service.delete()
        return Response({
            "message": "Service deleted successfully."
        }, status=204)


class InvoiceViewSet(BaseViewSet):
    queryset = Invoice.objects.all()
    search_fields = ['patient__username', 'invoice_number', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        elif self.action == 'retrieve':
            return InvoiceDetailSerializer
        elif self.action in ['create', 'update']:
            return InvoiceCreateUpdateSerializer

    def get_paginated_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            current_page = self.paginator.page.number
            last_page = self.paginator.page.paginator.num_pages

            return Response({
                "count": self.paginator.page.paginator.count,
                "page": current_page,
                "last_page": last_page,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "message": "Invoices displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Invoices displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        invoices = self.filter_queryset(self.get_queryset())

        if not invoices:
            return Response({
                "message": "No invoices found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            invoices = invoices.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(invoices, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            invoice = self.get_object()
        except Invoice.DoesNotExist:
            return Response({
                "message": "Invoice not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(invoice)
        return Response({
            "message": "Invoice displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Invoice created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create invoice.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        invoice = self.get_object()
        serializer = self.get_serializer_class()(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Invoice updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update invoice.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        invoice = self.get_object()
        invoice.delete()
        return Response({
            "message": "Invoice deleted successfully."
        }, status=204)


class InvoiceItemViewSet(BaseViewSet):
    queryset = InvoiceItem.objects.all()
    search_fields = ['service__name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceItemListSerializer
        elif self.action == 'retrieve':
            return InvoiceItemDetailSerializer
        elif self.action in ['create', 'update']:
            return InvoiceItemCreateUpdateSerializer

    def get_paginated_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            current_page = self.paginator.page.number
            last_page = self.paginator.page.paginator.num_pages

            return Response({
                "count": self.paginator.page.paginator.count,
                "page": current_page,
                "last_page": last_page,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "message": "Invoice items displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Invoice items displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        items = self.filter_queryset(self.get_queryset())

        if not items:
            return Response({
                "message": "No invoice items found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            items = items.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(items, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            item = self.get_object()
        except InvoiceItem.DoesNotExist:
            return Response({
                "message": "Invoice item not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(item)
        return Response({
            "message": "Invoice item displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Invoice item created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create invoice item.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        item = self.get_object()
        serializer = self.get_serializer_class()(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Invoice item updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update invoice item.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response({
            "message": "Invoice item deleted successfully."
        }, status=204)


class PaymentViewSet(BaseViewSet):
    queryset = Payment.objects.all()
    search_fields = ['invoice__invoice_number', 'transaction_id', 'payment_method']

    def get_serializer_class(self):
        if self.action == 'list':
            return PaymentListSerializer
        elif self.action == 'retrieve':
            return PaymentDetailSerializer
        elif self.action in ['create', 'update']:
            return PaymentCreateUpdateSerializer

    def get_paginated_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            current_page = self.paginator.page.number
            last_page = self.paginator.page.paginator.num_pages

            return Response({
                "count": self.paginator.page.paginator.count,
                "page": current_page,
                "last_page": last_page,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "message": "Payments displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Payments displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        payments = self.filter_queryset(self.get_queryset())

        if not payments:
            return Response({
                "message": "No payments found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            payments = payments.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(payments, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            payment = self.get_object()
        except Payment.DoesNotExist:
            return Response({
                "message": "Payment not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(payment)
        return Response({
            "message": "Payment displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Payment created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create payment.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        payment = self.get_object()
        serializer = self.get_serializer_class()(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Payment updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update payment.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        payment = self.get_object()
        payment.delete()
        return Response({
            "message": "Payment deleted successfully."
        }, status=204)


class InsuranceClaimViewSet(BaseViewSet):
    queryset = InsuranceClaim.objects.all()
    search_fields = ['claim_number', 'insurance__provider', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return InsuranceClaimListSerializer
        elif self.action == 'retrieve':
            return InsuranceClaimDetailSerializer
        elif self.action in ['create', 'update']:
            return InsuranceClaimCreateUpdateSerializer

    def get_paginated_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            current_page = self.paginator.page.number
            last_page = self.paginator.page.paginator.num_pages

            return Response({
                "count": self.paginator.page.paginator.count,
                "page": current_page,
                "last_page": last_page,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "message": "Insurance claims displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Insurance claims displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        claims = self.filter_queryset(self.get_queryset())

        if not claims:
            return Response({
                "message": "No insurance claims found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            claims = claims.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(claims, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            claim = self.get_object()
        except InsuranceClaim.DoesNotExist:
            return Response({
                "message": "Insurance claim not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(claim)
        return Response({
            "message": "Insurance claim displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Insurance claim created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create insurance claim.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        claim = self.get_object()
        serializer = self.get_serializer_class()(claim, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Insurance claim updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update insurance claim.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        claim = self.get_object()
        claim.delete()
        return Response({
            "message": "Insurance claim deleted successfully."
        }, status=204)
