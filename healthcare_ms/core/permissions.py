from rest_framework import permissions


class PatientProfilePermission(permissions.BasePermission):
    """
    Custom permission for PatientProfileViewSet to handle different user types:
    - admin/staff: full access
    - doctor: access to their own patients only
    - patient: access to their own profile only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list action, only allow admin, staff, and doctors
        if view.action == 'list':
            return request.user.user_type == 'doctor'

        # For other actions, allow if user is authenticated
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their own patients
        if request.user.user_type == 'doctor':
            return obj.primary_doctor == request.user

        # Patients can only access their own profile
        if request.user.user_type == 'patient':
            return obj.user == request.user

        return False


class InsurancePermission(permissions.BasePermission):
    """
    Custom permission for InsuranceViewSet to handle different user types:
    - admin/staff: full access (except destroy for staff)
    - doctor: list and retrieve their patients' insurance only
    - patient: full access to their own insurance
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow patients
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'patient'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin has full access to all objects
        if request.user.user_type == 'admin':
            return True

        # Staff can access all objects except destroy
        if request.user.user_type == 'staff':
            return view.action != 'destroy'

        # Doctors can only access their patients' insurance
        if request.user.user_type == 'doctor':
            return obj.patient.primary_doctor == request.user

        # Patients can only access their own insurance
        if request.user.user_type == 'patient':
            return obj.patient == request.user

        return False


class EmergencyContactPermission(permissions.BasePermission):
    """
    Custom permission for EmergencyContactViewSet to handle different user types:
    - admin/staff: list and retrieve all emergency contacts
    - doctor: list and retrieve their patients' emergency contacts
    - patient: full access to their own emergency contacts
    """

    def has_permission(self, request, view):
        # Allow admin and staff to list and retrieve
        if request.user.user_type in ['admin', 'staff']:
            return view.action in ['list', 'retrieve']

        # For list and retrieve actions, allow doctors
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow patients
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'patient'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff can access all objects for list and retrieve
        if request.user.user_type in ['admin', 'staff']:
            return view.action in ['list', 'retrieve']

        # Doctors can only access their patients' emergency contacts
        if request.user.user_type == 'doctor':
            return obj.patient.primary_doctor == request.user

        # Patients can only access their own emergency contacts
        if request.user.user_type == 'patient':
            return obj.patient == request.user

        return False


class AppointmentTypePermission(permissions.BasePermission):
    """
    Custom permission for AppointmentTypeViewSet:
    - admin/staff: full access
    - doctor: list and retrieve only
    - patient: list and retrieve only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        return False


class AppointmentSlotPermission(permissions.BasePermission):
    """
    Custom permission for AppointmentSlotViewSet:
    - admin/staff: full access
    - doctor: full access to their own slots
    - patient: list and retrieve only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow doctors
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'doctor'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their own slots
        if request.user.user_type == 'doctor':
            return obj.doctor == request.user

        # Patients can only view slots
        if request.user.user_type == 'patient':
            return view.action in ['list', 'retrieve']

        return False


class AppointmentPermission(permissions.BasePermission):
    """
    Custom permission for AppointmentViewSet:
    - admin/staff: full access
    - doctor: full access to their own appointments
    - patient: full access to their own appointments
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their own appointments
        if request.user.user_type == 'doctor':
            return obj.doctor == request.user

        # Patients can only access their own appointments
        if request.user.user_type == 'patient':
            return obj.patient == request.user

        return False


class MedicalRecordPermission(permissions.BasePermission):
    """
    Custom permission for MedicalRecordViewSet:
    - admin/staff: full access
    - doctor: full access to their own records
    - patient: list and retrieve their own records only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow doctors
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'doctor'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their own records
        if request.user.user_type == 'doctor':
            return obj.doctor == request.user

        # Patients can only view their own records
        if request.user.user_type == 'patient':
            return obj.patient == request.user

        return False


class DiagnosisPermission(permissions.BasePermission):
    """
    Custom permission for DiagnosisViewSet:
    - admin/staff: full access
    - doctor: full access to their patients' diagnoses
    - patient: list and retrieve their own diagnoses only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow doctors
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'doctor'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' diagnoses
        if request.user.user_type == 'doctor':
            return obj.medical_record.doctor == request.user

        # Patients can only view their own diagnoses
        if request.user.user_type == 'patient':
            return obj.medical_record.patient == request.user

        return False


class TreatmentPermission(permissions.BasePermission):
    """
    Custom permission for TreatmentViewSet:
    - admin/staff: full access
    - doctor: full access to their patients' treatments
    - patient: list and retrieve their own treatments only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow doctors
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'doctor'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' treatments
        if request.user.user_type == 'doctor':
            return obj.medical_record.doctor == request.user

        # Patients can only view their own treatments
        if request.user.user_type == 'patient':
            return obj.medical_record.patient == request.user

        return False


class PrescriptionPermission(permissions.BasePermission):
    """
    Custom permission for PrescriptionViewSet:
    - admin/staff: full access
    - doctor: full access to their patients' prescriptions
    - patient: list and retrieve their own prescriptions only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow doctors
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'doctor'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' prescriptions
        if request.user.user_type == 'doctor':
            return obj.medical_record.doctor == request.user

        # Patients can only view their own prescriptions
        if request.user.user_type == 'patient':
            return obj.medical_record.patient == request.user

        return False


class ServicePermission(permissions.BasePermission):
    """
    Custom permission for ServiceViewSet:
    - admin/staff: full access
    - doctor: list and retrieve only
    - patient: list and retrieve only
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        return False


class InvoicePermission(permissions.BasePermission):
    """
    Custom permission for InvoiceViewSet:
    - admin/staff: full access
    - doctor: list and retrieve their patients' invoices only
    - patient: full access to their own invoices
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow patients
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'patient'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' invoices
        if request.user.user_type == 'doctor':
            return obj.patient.primary_doctor == request.user

        # Patients can only access their own invoices
        if request.user.user_type == 'patient':
            return obj.patient == request.user

        return False


class InvoiceItemPermission(permissions.BasePermission):
    """
    Custom permission for InvoiceItemViewSet:
    - admin/staff: full access
    - doctor: list and retrieve their patients' invoice items only
    - patient: full access to their own invoice items
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow patients
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'patient'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' invoice items
        if request.user.user_type == 'doctor':
            return obj.invoice.patient.primary_doctor == request.user

        # Patients can only access their own invoice items
        if request.user.user_type == 'patient':
            return obj.invoice.patient == request.user

        return False


class PaymentPermission(permissions.BasePermission):
    """
    Custom permission for PaymentViewSet:
    - admin/staff: full access
    - doctor: list and retrieve their patients' payments only
    - patient: full access to their own payments
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow patients
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'patient'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' payments
        if request.user.user_type == 'doctor':
            return obj.invoice.patient.primary_doctor == request.user

        # Patients can only access their own payments
        if request.user.user_type == 'patient':
            return obj.invoice.patient == request.user

        return False


class InsuranceClaimPermission(permissions.BasePermission):
    """
    Custom permission for InsuranceClaimViewSet:
    - admin/staff: full access
    - doctor: list and retrieve their patients' claims only
    - patient: full access to their own claims
    """

    def has_permission(self, request, view):
        # Allow admin and staff full access
        if request.user.user_type in ['admin', 'staff']:
            return True

        # For list and retrieve actions, allow doctors and patients
        if view.action in ['list', 'retrieve']:
            return request.user.user_type in ['doctor', 'patient']

        # For create, update, and destroy actions, allow patients
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.user_type == 'patient'

        return False

    def has_object_permission(self, request, view, obj):
        # Admin and staff have full access to all objects
        if request.user.user_type in ['admin', 'staff']:
            return True

        # Doctors can only access their patients' claims
        if request.user.user_type == 'doctor':
            return obj.invoice.patient.primary_doctor == request.user

        # Patients can only access their own claims
        if request.user.user_type == 'patient':
            return obj.invoice.patient == request.user

        return False
