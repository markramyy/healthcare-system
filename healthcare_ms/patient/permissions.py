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
