from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from healthcare_ms.users.models import User
from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact


def landing_page(request):
    return render(request, 'landing.html')


@login_required
def dashboard_home(request):
    # Get statistics
    total_users = User.objects.count()
    total_patients = PatientProfile.objects.count()
    total_insurance = Insurance.objects.count()
    total_emergency_contacts = EmergencyContact.objects.count()

    context = {
        'total_users': total_users,
        'total_patients': total_patients,
        'total_insurance': total_insurance,
        'total_emergency_contacts': total_emergency_contacts,
    }

    return render(request, 'home.html', context)
