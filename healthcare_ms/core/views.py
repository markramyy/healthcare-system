from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from healthcare_ms.users.models import User
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription


def landing_page(request):
    return render(request, 'landing.html')


@login_required
def dashboard_home(request):
    # Get statistics
    total_users = User.objects.count()
    total_patients = PatientProfile.objects.count()
    total_insurance = Insurance.objects.count()
    total_emergency_contacts = EmergencyContact.objects.count()

    # Get EHR statistics
    total_medical_records = MedicalRecord.objects.count()
    total_diagnoses = Diagnosis.objects.count()
    total_treatments = Treatment.objects.count()
    total_prescriptions = Prescription.objects.count()

    context = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_insurance': total_insurance,
        'total_emergency_contacts': total_emergency_contacts,
        'total_medical_records': total_medical_records,
        'total_diagnoses': total_diagnoses,
        'total_treatments': total_treatments,
        'total_prescriptions': total_prescriptions,
    }

    return render(request, 'home.html', context)
