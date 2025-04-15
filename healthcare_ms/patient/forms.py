from django import forms
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.users.models import User


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'user', 'primary_doctor', 'blood_type',
            'height', 'weight', 'allergies', 'chronic_conditions'
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'primary_doctor': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'blood_type': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'height': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'weight': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'allergies': forms.Textarea(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(user_type='patient')
        self.fields['primary_doctor'].queryset = User.objects.filter(user_type='doctor')


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = [
            'patient', 'provider', 'policy_number',
            'group_number', 'coverage_start_date', 'coverage_end_date'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'provider': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'policy_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'group_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'coverage_start_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'type': 'date'}),
            'coverage_end_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.objects.filter(user_type='patient')


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = [
            'patient', 'name', 'relationship',
            'phone_number', 'email', 'address', 'is_primary'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'relationship': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'rows': 3}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-blue-600 bg-white bg-opacity-10 border-gray-300 rounded focus:ring-blue-500'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].queryset = User.objects.filter(user_type='patient')