from django import forms
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.users.models import User


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = [
            'user', 'gender', 'primary_doctor', 'blood_type',
            'height', 'weight', 'allergies', 'chronic_conditions'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(user_type='patient')
        self.fields['primary_doctor'].required = False
        self.fields['primary_doctor'].queryset = User.objects.filter(user_type='doctor')
        self.fields['primary_doctor'].empty_label = "-- Select Primary Doctor --"

        self.fields['blood_type'].required = False
        self.fields['height'].required = False
        self.fields['weight'].required = False
        self.fields['allergies'].required = False
        self.fields['chronic_conditions'].required = False


class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = [
            'patient', 'provider', 'policy_number',
            'group_number', 'coverage_start_date', 'coverage_end_date', 'is_active',
            'deductible', 'copayment', 'coinsurance', 'out_of_pocket_max', 'notes'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'provider': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'policy_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'group_number': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white'}),
            'coverage_start_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'type': 'date'}),
            'coverage_end_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-blue-600 bg-white bg-opacity-10 border-gray-300 rounded focus:ring-blue-500'}),
            'deductible': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'step': '0.01', 'min': '0'}),
            'copayment': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'step': '0.01', 'min': '0'}),
            'coinsurance': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'step': '0.01', 'min': '0', 'max': '100'}),
            'out_of_pocket_max': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 rounded-lg bg-white bg-opacity-10 text-white', 'rows': 3}),
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