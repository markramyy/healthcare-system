from healthcare_ms.core.base_serializer import BaseSerializer
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.users.serializers import ListUserAdminSerializer


class PatientProfileListSerializer(BaseSerializer):
    user = ListUserAdminSerializer(read_only=True)
    primary_doctor = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = (
            'guid', 'user', 'primary_doctor', 'blood_type',
            'height', 'weight'
        )


class PatientProfileDetailSerializer(BaseSerializer):
    user = ListUserAdminSerializer(read_only=True)
    primary_doctor = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = (
            'guid', 'user', 'primary_doctor', 'blood_type',
            'height', 'weight', 'allergies', 'chronic_conditions',
        )


class PatientProfileCreateSerializer(BaseSerializer):
    class Meta:
        model = PatientProfile
        fields = (
            'guid', 'user', 'primary_doctor', 'blood_type',
            'height', 'weight', 'allergies', 'chronic_conditions'
        )


class PatientProfileUpdateSerializer(BaseSerializer):
    class Meta:
        model = PatientProfile
        fields = (
            'guid', 'user', 'gender', 'primary_doctor', 'blood_type',
            'height', 'weight', 'allergies', 'chronic_conditions'
        )


class InsuranceListSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = Insurance
        fields = (
            'guid', 'patient', 'provider', 'policy_number',
            'group_number', 'coverage_start_date', 'coverage_end_date',
            'is_active'
        )


class InsuranceDetailSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = Insurance
        fields = (
            'guid', 'patient', 'provider', 'policy_number',
            'group_number', 'coverage_start_date', 'coverage_end_date',
            'is_active', 'deductible', 'copayment', 'coinsurance',
            'out_of_pocket_max', 'notes'
        )


class InsuranceCreateSerializer(BaseSerializer):
    class Meta:
        model = Insurance
        fields = (
            'guid', 'patient', 'provider', 'policy_number',
            'group_number', 'coverage_start_date', 'coverage_end_date',
            'is_active', 'deductible', 'copayment', 'coinsurance',
            'out_of_pocket_max', 'notes'
        )


class InsuranceUpdateSerializer(BaseSerializer):
    class Meta:
        model = Insurance
        fields = (
            'guid', 'patient', 'provider', 'policy_number',
            'group_number', 'coverage_start_date', 'coverage_end_date',
            'is_active', 'deductible', 'copayment', 'coinsurance',
            'out_of_pocket_max', 'notes'
        )


class EmergencyContactListSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = EmergencyContact
        fields = (
            'guid', 'patient', 'name', 'relationship',
            'is_primary'
        )


class EmergencyContactDetailSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = EmergencyContact
        fields = (
            'guid', 'patient', 'name', 'relationship',
            'phone_number', 'email', 'address', 'is_primary'
        )


class EmergencyContactCreateSerializer(BaseSerializer):
    class Meta:
        model = EmergencyContact
        fields = (
            'guid', 'patient', 'name', 'relationship',
            'phone_number', 'email', 'address', 'is_primary'
        )


class EmergencyContactUpdateSerializer(BaseSerializer):
    class Meta:
        model = EmergencyContact
        fields = (
            'guid', 'patient', 'name', 'relationship',
            'phone_number', 'email', 'address', 'is_primary'
        )
