from rest_framework.response import Response
from django.db.models import Q
from functools import reduce

from healthcare_ms.core.base_viewset import BaseViewSet
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription
from healthcare_ms.ehr.serializers import (
    MedicalRecordListSerializer,
    MedicalRecordDetailSerializer,
    MedicalRecordCreateSerializer,
    MedicalRecordUpdateSerializer,
    DiagnosisListSerializer,
    DiagnosisDetailSerializer,
    DiagnosisCreateSerializer,
    DiagnosisUpdateSerializer,
    TreatmentListSerializer,
    TreatmentDetailSerializer,
    TreatmentCreateSerializer,
    TreatmentUpdateSerializer,
    PrescriptionListSerializer,
    PrescriptionDetailSerializer,
    PrescriptionCreateSerializer,
    PrescriptionUpdateSerializer
)
from healthcare_ms.core.permissions import (
    MedicalRecordPermission,
    DiagnosisPermission,
    TreatmentPermission,
    PrescriptionPermission
)

import operator
import logging
logger = logging.getLogger(__name__)


class MedicalRecordViewSet(BaseViewSet):
    queryset = MedicalRecord.objects.all()
    search_fields = ['patient__username', 'doctor__username', 'symptoms']
    permission_classes = [MedicalRecordPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is admin or staff, return all records
        if user.user_type in ['admin', 'staff']:
            return queryset

        # If user is doctor, return only their records
        if user.user_type == 'doctor':
            return queryset.filter(doctor=user)

        # If user is patient, return only their records
        if user.user_type == 'patient':
            return queryset.filter(patient=user)

        return MedicalRecord.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return MedicalRecordListSerializer
        elif self.action == 'retrieve':
            return MedicalRecordDetailSerializer
        elif self.action == 'create':
            return MedicalRecordCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return MedicalRecordUpdateSerializer
        return MedicalRecordListSerializer

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
                "message": "Medical records displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Medical records displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        records = self.filter_queryset(self.get_queryset())

        if not records:
            return Response({
                "message": "No medical records found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            records = records.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(records, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            record = self.get_object()
        except MedicalRecord.DoesNotExist:
            return Response({
                "message": "Medical record not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(record)
        return Response({
            "message": "Medical record displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        # If user is doctor, automatically set the doctor field
        if request.user.user_type == 'doctor':
            request.data['doctor'] = request.user.guid

        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Medical record created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create medical record.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        serializer = self.get_serializer_class()(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Medical record updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update medical record.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        record = self.get_object()
        record.delete()
        return Response({
            "message": "Medical record deleted successfully."
        }, status=204)


class DiagnosisViewSet(BaseViewSet):
    queryset = Diagnosis.objects.all()
    search_fields = ['diagnosis_code', 'description']
    permission_classes = [DiagnosisPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is admin or staff, return all diagnoses
        if user.user_type in ['admin', 'staff']:
            return queryset

        # If user is doctor, return only their patients' diagnoses
        if user.user_type == 'doctor':
            return queryset.filter(medical_record__doctor=user)

        # If user is patient, return only their diagnoses
        if user.user_type == 'patient':
            return queryset.filter(medical_record__patient=user)

        return Diagnosis.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return DiagnosisListSerializer
        elif self.action == 'retrieve':
            return DiagnosisDetailSerializer
        elif self.action == 'create':
            return DiagnosisCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DiagnosisUpdateSerializer
        return DiagnosisListSerializer

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
                "message": "Diagnoses displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Diagnoses displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        diagnoses = self.filter_queryset(self.get_queryset())

        if not diagnoses:
            return Response({
                "message": "No diagnoses found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            diagnoses = diagnoses.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(diagnoses, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            diagnosis = self.get_object()
        except Diagnosis.DoesNotExist:
            return Response({
                "message": "Diagnosis not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(diagnosis)
        return Response({
            "message": "Diagnosis displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Diagnosis created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create diagnosis.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        diagnosis = self.get_object()
        serializer = self.get_serializer_class()(diagnosis, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Diagnosis updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update diagnosis.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        diagnosis = self.get_object()
        diagnosis.delete()
        return Response({
            "message": "Diagnosis deleted successfully."
        }, status=204)


class TreatmentViewSet(BaseViewSet):
    queryset = Treatment.objects.all()
    search_fields = ['name', 'description']
    permission_classes = [TreatmentPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is admin or staff, return all treatments
        if user.user_type in ['admin', 'staff']:
            return queryset

        # If user is doctor, return only their patients' treatments
        if user.user_type == 'doctor':
            return queryset.filter(medical_record__doctor=user)

        # If user is patient, return only their treatments
        if user.user_type == 'patient':
            return queryset.filter(medical_record__patient=user)

        return Treatment.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return TreatmentListSerializer
        elif self.action == 'retrieve':
            return TreatmentDetailSerializer
        elif self.action == 'create':
            return TreatmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TreatmentUpdateSerializer
        return TreatmentListSerializer

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
                "message": "Treatments displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Treatments displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        treatments = self.filter_queryset(self.get_queryset())

        if not treatments:
            return Response({
                "message": "No treatments found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            treatments = treatments.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(treatments, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            treatment = self.get_object()
        except Treatment.DoesNotExist:
            return Response({
                "message": "Treatment not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(treatment)
        return Response({
            "message": "Treatment displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Treatment created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create treatment.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        treatment = self.get_object()
        serializer = self.get_serializer_class()(treatment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Treatment updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update treatment.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        treatment = self.get_object()
        treatment.delete()
        return Response({
            "message": "Treatment deleted successfully."
        }, status=204)


class PrescriptionViewSet(BaseViewSet):
    queryset = Prescription.objects.all()
    search_fields = ['medication_name', 'dosage']
    permission_classes = [PrescriptionPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is admin or staff, return all prescriptions
        if user.user_type in ['admin', 'staff']:
            return queryset

        # If user is doctor, return only their patients' prescriptions
        if user.user_type == 'doctor':
            return queryset.filter(medical_record__doctor=user)

        # If user is patient, return only their prescriptions
        if user.user_type == 'patient':
            return queryset.filter(medical_record__patient=user)

        return Prescription.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return PrescriptionListSerializer
        elif self.action == 'retrieve':
            return PrescriptionDetailSerializer
        elif self.action == 'create':
            return PrescriptionCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PrescriptionUpdateSerializer
        return PrescriptionListSerializer

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
                "message": "Prescriptions displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Prescriptions displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        prescriptions = self.filter_queryset(self.get_queryset())

        if not prescriptions:
            return Response({
                "message": "No prescriptions found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            prescriptions = prescriptions.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(prescriptions, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            prescription = self.get_object()
        except Prescription.DoesNotExist:
            return Response({
                "message": "Prescription not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(prescription)
        return Response({
            "message": "Prescription displayed successfully.",
            "data": serializer.data
        }, status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Prescription created successfully.",
                "data": serializer.data
            }, status=201)
        return Response({
            "message": "Failed to create prescription.",
            "errors": serializer.errors
        }, status=400)

    def update(self, request, *args, **kwargs):
        prescription = self.get_object()
        serializer = self.get_serializer_class()(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Prescription updated successfully.",
                "data": serializer.data
            }, status=200)
        return Response({
            "message": "Failed to update prescription.",
            "errors": serializer.errors
        }, status=400)

    def destroy(self, request, *args, **kwargs):
        prescription = self.get_object()
        prescription.delete()
        return Response({
            "message": "Prescription deleted successfully."
        }, status=204)
