from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta, date
import json
from healthcare_ms.users.models import User
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription
from healthcare_ms.appointment.models import Appointment


def landing_page(request):
    return render(request, 'landing.html')


@login_required
def dashboard_home(request):
    # Get basic statistics
    total_users = User.objects.count()
    total_patients = PatientProfile.objects.count()
    total_insurance = Insurance.objects.count()
    total_emergency_contacts = EmergencyContact.objects.count()

    # Get EHR statistics
    total_medical_records = MedicalRecord.objects.count()
    total_diagnoses = Diagnosis.objects.count()
    total_treatments = Treatment.objects.count()
    total_prescriptions = Prescription.objects.count()

    # Get recent activity
    today = datetime.now().date()
    last_week = today - timedelta(days=7)

    # Get patient demographics
    patients = User.objects.filter(user_type='patient')

    # Calculate age distribution
    age_distribution = {}
    for patient in patients:
        if patient.date_of_birth:
            age = (date.today() - patient.date_of_birth).days // 365
            age_distribution[age] = age_distribution.get(age, 0) + 1

    # Get gender distribution
    gender_distribution = list(PatientProfile.objects.values('gender').annotate(count=Count('id')))

    # Get recent patients with their profiles
    recent_patients = PatientProfile.objects.select_related('user').order_by('-created')[:5]

    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        slot__date__gte=today,
        appointment_status__in=['scheduled', 'confirmed']
    ).order_by('slot__date', 'slot__start_time')[:5]

    # Get treatment statistics
    treatment_stats = Treatment.objects.values('treatment_status').annotate(count=Count('id'))

    context = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_insurance': total_insurance,
        'total_emergency_contacts': total_emergency_contacts,
        'total_medical_records': total_medical_records,
        'total_diagnoses': total_diagnoses,
        'total_treatments': total_treatments,
        'total_prescriptions': total_prescriptions,
        'recent_patients': recent_patients,
        'upcoming_appointments': upcoming_appointments,
        'patient_demographics': {
            'age_groups': json.dumps(age_distribution),
            'gender_distribution': json.dumps(gender_distribution),
        },
        'treatment_stats': treatment_stats,
        'today': today,
        'last_week': last_week,
    }

    return render(request, 'home.html', context)
