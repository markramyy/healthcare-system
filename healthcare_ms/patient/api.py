from rest_framework.response import Response
from django.db.models import Q
from functools import reduce
from rest_framework.decorators import action

from healthcare_ms.core.base_viewset import BaseViewSet
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.patient.serializers import (
    PatientProfileListSerializer,
    PatientProfileDetailSerializer,
    PatientProfileUpdateSerializer,
    InsuranceListSerializer,
    InsuranceDetailSerializer,
    InsuranceCreateSerializer,
    InsuranceUpdateSerializer,
    EmergencyContactListSerializer,
    EmergencyContactDetailSerializer,
    EmergencyContactCreateSerializer,
    EmergencyContactUpdateSerializer
)
from healthcare_ms.patient.permissions import (
    PatientProfilePermission,
    InsurancePermission,
    EmergencyContactPermission
)

import operator
import logging
logger = logging.getLogger(__name__)


class PatientProfileViewSet(BaseViewSet):
    queryset = PatientProfile.objects.all()
    search_fields = ['user__username', 'user__email', 'blood_type']
    permission_classes = [PatientProfilePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.user_type in ['admin', 'staff']:
            return queryset

        if user.user_type == 'doctor':
            return queryset.filter(primary_doctor=user)

        if user.user_type == 'patient':
            return queryset.filter(user=user)

        return PatientProfile.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientProfileListSerializer
        elif self.action in ['retrieve', 'me']:
            return PatientProfileDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return PatientProfileUpdateSerializer
        return PatientProfileListSerializer

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        if request.user.user_type != 'patient':
            return Response({
                "message": "This endpoint is only accessible by patients."
            }, status=403)

        try:
            profile = PatientProfile.objects.get(user=request.user)
            serializer = self.get_serializer_class()(profile)
            return Response({
                "message": "Patient profile retrieved successfully.",
                "data": serializer.data
            }, status=200)
        except PatientProfile.DoesNotExist:
            return Response({
                "message": "Patient profile not found.",
                "data": {}
            }, status=404)

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
                "message": "Patient profiles displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Patient profiles displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        profiles = self.filter_queryset(self.get_queryset())

        if not profiles:
            return Response({
                "message": "No patient profiles found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            profiles = profiles.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(profiles, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            profile = self.get_object()
        except PatientProfile.DoesNotExist:
            return Response({
                "message": "Patient profile not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(profile)
        return Response({
            "message": "Patient profile displayed successfully.",
            "data": serializer.data
        }, status=200)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer_class()(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Patient profile updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update patient profile.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        if request.user.user_type != 'admin':
            return Response({
                "message": "Only administrators can delete patient profiles."
            }, status=403)

        try:
            profile = self.get_object()
            profile.delete()
            return Response({
                "message": "Patient profile deleted successfully."
            }, status=204)
        except PatientProfile.DoesNotExist:
            return Response({
                "message": "Patient profile not found."
            }, status=404)


class InsuranceViewSet(BaseViewSet):
    queryset = Insurance.objects.all()
    search_fields = ['patient__username', 'provider', 'policy_number']
    permission_classes = [InsurancePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.user_type in ['admin', 'staff']:
            return queryset

        if user.user_type == 'doctor':
            return queryset.filter(patient__primary_doctor=user)

        if user.user_type == 'patient':
            return queryset.filter(patient=user)

        return Insurance.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return InsuranceListSerializer
        elif self.action == 'retrieve':
            return InsuranceDetailSerializer
        elif self.action == 'create':
            return InsuranceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InsuranceUpdateSerializer
        return InsuranceListSerializer

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
                "message": "Insurance policies displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Insurance policies displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        insurance = self.filter_queryset(self.get_queryset())

        if not insurance:
            return Response({
                "message": "No insurance policies found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            insurance = insurance.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(insurance, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            insurance = self.get_object()
        except Insurance.DoesNotExist:
            return Response({
                "message": "Insurance policy not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(insurance)
        return Response({
            "message": "Insurance policy displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        if request.user.user_type == 'patient':
            request.data['patient'] = request.user.guid

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Insurance policy created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create insurance policy.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        insurance = self.get_object()
        serializer = self.get_serializer_class()(insurance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Insurance policy updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update insurance policy.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        if request.user.user_type not in ['admin', 'patient']:
            return Response({
                "message": "You don't have permission to delete insurance policies."
            }, status=403)

        try:
            insurance = self.get_object()
            insurance.delete()
            return Response({
                "message": "Insurance policy deleted successfully."
            }, status=204)
        except Insurance.DoesNotExist:
            return Response({
                "message": "Insurance policy not found."
            }, status=404)


class EmergencyContactViewSet(BaseViewSet):
    queryset = EmergencyContact.objects.all()
    search_fields = ['patient__username', 'name', 'relationship']
    permission_classes = [EmergencyContactPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.user_type in ['admin', 'staff']:
            return queryset

        if user.user_type == 'doctor':
            return queryset.filter(patient__primary_doctor=user)

        if user.user_type == 'patient':
            return queryset.filter(patient=user)

        return EmergencyContact.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return EmergencyContactListSerializer
        elif self.action == 'retrieve':
            return EmergencyContactDetailSerializer
        elif self.action == 'create':
            return EmergencyContactCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EmergencyContactUpdateSerializer
        return EmergencyContactListSerializer

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
                "message": "Emergency contacts displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Emergency contacts displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        contacts = self.filter_queryset(self.get_queryset())

        if not contacts:
            return Response({
                "message": "No emergency contacts found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            contacts = contacts.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(contacts, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            contact = self.get_object()
        except EmergencyContact.DoesNotExist:
            return Response({
                "message": "Emergency contact not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(contact)
        return Response({
            "message": "Emergency contact displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        if request.user.user_type == 'patient':
            request.data['patient'] = request.user.guid

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Emergency contact created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create emergency contact.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        contact = self.get_object()
        serializer = self.get_serializer_class()(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Emergency contact updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update emergency contact.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        if request.user.user_type != 'patient':
            return Response({
                "message": "Only patients can delete their own emergency contacts."
            }, status=403)

        try:
            contact = self.get_object()
            contact.delete()
            return Response({
                "message": "Emergency contact deleted successfully."
            }, status=204)
        except EmergencyContact.DoesNotExist:
            return Response({
                "message": "Emergency contact not found."
            }, status=404)
