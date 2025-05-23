from healthcare_ms.core.base_serializer import BaseSerializer
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription
from healthcare_ms.users.serializers import ListUserAdminSerializer


class MedicalRecordListSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)
    doctor = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = (
            'guid', 'id', 'patient', 'doctor', 'visit_date',
            'symptoms', 'follow_up_date', 'is_active', 'created', 'modified'
        )


class MedicalRecordDetailSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)
    doctor = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = (
            'guid', 'id', 'patient', 'doctor', 'visit_date',
            'symptoms', 'notes', 'follow_up_date', 'is_active',
            'created', 'modified'
        )


class MedicalRecordCreateSerializer(BaseSerializer):
    class Meta:
        model = MedicalRecord
        fields = (
            'guid', 'patient', 'doctor', 'visit_date',
            'symptoms', 'notes', 'follow_up_date'
        )


class MedicalRecordUpdateSerializer(BaseSerializer):
    class Meta:
        model = MedicalRecord
        fields = (
            'guid', 'patient', 'doctor', 'visit_date',
            'symptoms', 'notes', 'follow_up_date', 'is_active'
        )


class DiagnosisListSerializer(BaseSerializer):
    medical_record = MedicalRecordListSerializer(read_only=True)

    class Meta:
        model = Diagnosis
        fields = (
            'guid', 'id', 'medical_record', 'diagnosis_code',
            'severity', 'is_active', 'created', 'modified'
        )


class DiagnosisDetailSerializer(BaseSerializer):
    medical_record = MedicalRecordListSerializer(read_only=True)

    class Meta:
        model = Diagnosis
        fields = (
            'guid', 'id', 'medical_record', 'diagnosis_code',
            'description', 'severity', 'is_active', 'created', 'modified'
        )


class DiagnosisCreateSerializer(BaseSerializer):
    class Meta:
        model = Diagnosis
        fields = (
            'guid', 'medical_record', 'diagnosis_code',
            'description', 'severity'
        )


class DiagnosisUpdateSerializer(BaseSerializer):
    class Meta:
        model = Diagnosis
        fields = (
            'guid', 'medical_record', 'diagnosis_code',
            'description', 'severity', 'is_active'
        )


class TreatmentListSerializer(BaseSerializer):
    medical_record = MedicalRecordListSerializer(read_only=True)

    class Meta:
        model = Treatment
        fields = (
            'guid', 'id', 'medical_record', 'name',
            'treatment_status', 'is_active', 'created', 'modified'
        )


class TreatmentDetailSerializer(BaseSerializer):
    medical_record = MedicalRecordListSerializer(read_only=True)

    class Meta:
        model = Treatment
        fields = (
            'guid', 'id', 'medical_record', 'name',
            'description', 'start_date', 'end_date', 'treatment_status',
            'is_active', 'created', 'modified'
        )


class TreatmentCreateSerializer(BaseSerializer):
    class Meta:
        model = Treatment
        fields = (
            'guid', 'medical_record', 'name', 'description',
            'start_date', 'end_date', 'treatment_status'
        )


class TreatmentUpdateSerializer(BaseSerializer):
    class Meta:
        model = Treatment
        fields = (
            'guid', 'medical_record', 'name', 'description',
            'start_date', 'end_date', 'treatment_status', 'is_active'
        )


class PrescriptionListSerializer(BaseSerializer):
    medical_record = MedicalRecordListSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = (
            'guid', 'id', 'medical_record', 'medication_name',
            'is_active', 'created', 'modified'
        )


class PrescriptionDetailSerializer(BaseSerializer):
    medical_record = MedicalRecordListSerializer(read_only=True)

    class Meta:
        model = Prescription
        fields = (
            'guid', 'id', 'medical_record', 'medication_name',
            'dosage', 'frequency', 'duration', 'instructions',
            'is_active', 'created', 'modified'
        )


class PrescriptionCreateSerializer(BaseSerializer):
    class Meta:
        model = Prescription
        fields = (
            'guid', 'medical_record', 'medication_name',
            'dosage', 'frequency', 'duration', 'instructions'
        )


class PrescriptionUpdateSerializer(BaseSerializer):
    class Meta:
        model = Prescription
        fields = (
            'guid', 'medical_record', 'medication_name',
            'dosage', 'frequency', 'duration', 'instructions', 'is_active'
        )
