from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.db.models import Q
from functools import reduce

from healthcare_ms.core.base_viewset import BaseViewSet
from healthcare_ms.appointment.models import AppointmentType, AppointmentSlot, Appointment
from healthcare_ms.appointment.serializers import (
    AppointmentTypeListSerializer,
    AppointmentTypeDetailSerializer,
    AppointmentTypeCreateUpdateSerializer,
    AppointmentSlotListSerializer,
    AppointmentSlotDetailSerializer,
    AppointmentSlotCreateUpdateSerializer,
    AppointmentListSerializer,
    AppointmentDetailSerializer,
    AppointmentCreateUpdateSerializer
)

import operator
import logging
logger = logging.getLogger(__name__)


class AppointmentTypeViewSet(BaseViewSet):
    """
    API endpoint for managing appointment types.
    """
    queryset = AppointmentType.objects.all()
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentTypeListSerializer
        elif self.action == 'retrieve':
            return AppointmentTypeDetailSerializer
        elif self.action in ['create', 'update']:
            return AppointmentTypeCreateUpdateSerializer

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
                "message": "Appointment types displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Appointment types displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        appointment_types = self.filter_queryset(self.get_queryset())

        if not appointment_types:
            return Response({
                "message": "No appointment types found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            appointment_types = appointment_types.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(appointment_types, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            appointment_type = self.get_object()
        except AppointmentType.DoesNotExist:
            return Response({
                "message": "Appointment type not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(appointment_type)
        return Response({
            "message": "Appointment type displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Appointment type created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create appointment type.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        appointment_type = self.get_object()
        serializer = self.get_serializer_class()(appointment_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Appointment type updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update appointment type.",
            "errors": serializer.errors
        }, status=400)


class AppointmentSlotViewSet(BaseViewSet):
    queryset = AppointmentSlot.objects.all()
    filterset_fields = ['doctor', 'date', 'is_available']
    search_fields = ['doctor__first_name', 'doctor__last_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentSlotListSerializer
        elif self.action == 'retrieve':
            return AppointmentSlotDetailSerializer
        elif self.action in ['create', 'update']:
            return AppointmentSlotCreateUpdateSerializer

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
                "message": "Appointment slots displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Appointment slots displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        slots = self.filter_queryset(self.get_queryset())

        if not slots:
            return Response({
                "message": "No appointment slots found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            slots = slots.filter(reduce(operator.or_, queries))

        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            slots = slots.filter(date__range=[start_date, end_date])

        return self.get_paginated_response(slots, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            slot = self.get_object()
        except AppointmentSlot.DoesNotExist:
            return Response({
                "message": "Appointment slot not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(slot)
        return Response({
            "message": "Appointment slot displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Appointment slot created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create appointment slot.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        slot = self.get_object()
        serializer = self.get_serializer_class()(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Appointment slot updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update appointment slot.",
            "errors": serializer.errors
        }, status=400)


class AppointmentViewSet(BaseViewSet):
    queryset = Appointment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'patient', 'doctor', 'appointment_type',
        'slot', 'status', 'is_active'
    ]
    search_fields = [
        'patient__first_name', 'patient__last_name',
        'doctor__first_name', 'doctor__last_name',
        'reason', 'notes'
    ]
    ordering_fields = [
        'slot__date', 'slot__start_time',
        'status', 'created'
    ]
    ordering = ['-slot__date', '-slot__start_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentListSerializer
        elif self.action == 'retrieve':
            return AppointmentDetailSerializer
        elif self.action in ['create', 'update']:
            return AppointmentCreateUpdateSerializer

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
                "message": "Appointments displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Appointments displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        appointments = self.filter_queryset(self.get_queryset())

        if not appointments:
            return Response({
                "message": "No appointments found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            appointments = appointments.filter(reduce(operator.or_, queries))

        # Filter by date range if provided
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            appointments = appointments.filter(slot__date__range=[start_date, end_date])

        return self.get_paginated_response(appointments, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            appointment = self.get_object()
        except Appointment.DoesNotExist:
            return Response({
                "message": "Appointment not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(appointment)
        return Response({
            "message": "Appointment displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Appointment created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create appointment.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        appointment = self.get_object()
        serializer = self.get_serializer_class()(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Appointment updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update appointment.",
            "errors": serializer.errors
        }, status=400)
