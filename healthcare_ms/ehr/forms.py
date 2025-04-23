from django import forms
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription
from healthcare_ms.users.models import User


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = [
            'patient', 'doctor', 'visit_date', 'symptoms',
            'notes', 'follow_up_date'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'doctor': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'visit_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'type': 'datetime-local'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'rows': 4
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'rows': 4
            }),
            'follow_up_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.objects.filter(user_type='patient')
        self.fields['doctor'].queryset = User.objects.filter(user_type='doctor')


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = [
            'medical_record', 'diagnosis_code', 'description', 'severity'
        ]
        widgets = {
            'medical_record': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'diagnosis_code': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'rows': 4
            }),
            'severity': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
        }


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = [
            'medical_record', 'name', 'description',
            'start_date', 'end_date', 'treatment_status'
        ]
        widgets = {
            'medical_record': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'rows': 4
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'type': 'datetime-local'
            }),
            'treatment_status': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'medical_record', 'medication_name', 'dosage',
            'frequency', 'duration', 'instructions'
        ]
        widgets = {
            'medical_record': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'medication_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'dosage': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'frequency': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'duration': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border'}),
            'instructions': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 rounded-lg border',
                'rows': 4
            }),
        }