from healthcare_ms.core.base_serializer import BaseSerializer
from healthcare_ms.appointment.models import AppointmentType, AppointmentSlot, Appointment
from healthcare_ms.users.serializers import ListUserAdminSerializer


class AppointmentTypeListSerializer(BaseSerializer):
    class Meta:
        model = AppointmentType
        fields = (
            'guid', 'id', 'name', 'duration',
            'is_active', 'created', 'modified'
        )


class AppointmentTypeDetailSerializer(BaseSerializer):
    class Meta:
        model = AppointmentType
        fields = (
            'guid', 'id', 'name', 'description',
            'duration', 'is_active', 'created', 'modified'
        )


class AppointmentTypeCreateSerializer(BaseSerializer):
    class Meta:
        model = AppointmentType
        fields = (
            'guid', 'name', 'description', 'duration'
        )


class AppointmentTypeUpdateSerializer(BaseSerializer):
    class Meta:
        model = AppointmentType
        fields = (
            'guid', 'name', 'description', 'duration', 'is_active'
        )


class AppointmentSlotListSerializer(BaseSerializer):
    doctor = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = AppointmentSlot
        fields = (
            'guid', 'id', 'doctor', 'date',
            'start_time', 'end_time', 'is_available',
            'is_active', 'created', 'modified'
        )


class AppointmentSlotDetailSerializer(BaseSerializer):
    doctor = ListUserAdminSerializer(read_only=True)

    class Meta:
        model = AppointmentSlot
        fields = (
            'guid', 'id', 'doctor', 'date',
            'start_time', 'end_time', 'is_available',
            'is_active', 'created', 'modified'
        )


class AppointmentSlotCreateSerializer(BaseSerializer):
    class Meta:
        model = AppointmentSlot
        fields = (
            'guid', 'doctor', 'date',
            'start_time', 'end_time', 'is_available'
        )


class AppointmentSlotUpdateSerializer(BaseSerializer):
    class Meta:
        model = AppointmentSlot
        fields = (
            'guid', 'doctor', 'date',
            'start_time', 'end_time', 'is_available', 'is_active'
        )


class AppointmentListSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)
    doctor = ListUserAdminSerializer(read_only=True)
    appointment_type = AppointmentTypeListSerializer(read_only=True)
    slot = AppointmentSlotListSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'guid', 'id', 'patient', 'doctor',
            'appointment_type', 'slot', 'status',
            'is_active', 'created', 'modified'
        )


class AppointmentDetailSerializer(BaseSerializer):
    patient = ListUserAdminSerializer(read_only=True)
    doctor = ListUserAdminSerializer(read_only=True)
    appointment_type = AppointmentTypeListSerializer(read_only=True)
    slot = AppointmentSlotListSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'guid', 'id', 'patient', 'doctor',
            'appointment_type', 'slot', 'status',
            'notes', 'reason', 'is_active',
            'created', 'modified'
        )


class AppointmentCreateSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = (
            'guid', 'patient', 'doctor', 'appointment_type',
            'slot', 'status', 'notes', 'reason'
        )


class AppointmentUpdateSerializer(BaseSerializer):
    class Meta:
        model = Appointment
        fields = (
            'guid', 'patient', 'doctor', 'appointment_type',
            'slot', 'status', 'notes', 'reason', 'is_active'
        )
