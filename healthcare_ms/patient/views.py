from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from healthcare_ms.patient.models import PatientProfile, Insurance, EmergencyContact
from healthcare_ms.patient.forms import (
    PatientProfileForm,
    InsuranceForm,
    EmergencyContactForm
)
from healthcare_ms.patient.serializers import (
    PatientProfileListSerializer,
    PatientProfileDetailSerializer,
    PatientProfileCreateUpdateSerializer,
    InsuranceListSerializer,
    InsuranceDetailSerializer,
    InsuranceCreateUpdateSerializer,
    EmergencyContactListSerializer,
    EmergencyContactDetailSerializer,
    EmergencyContactCreateUpdateSerializer
)


@login_required
def profile_list(request):
    profiles = PatientProfile.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        profiles = profiles.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(blood_type__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(profiles, 9)  # Show 9 profiles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = PatientProfileListSerializer(page_obj, many=True)

    return render(request, 'patient/profile_list.html', {
        'profiles': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def profile_detail(request, guid):
    profile = get_object_or_404(PatientProfile, guid=guid)
    serializer = PatientProfileDetailSerializer(profile)
    return render(request, 'patient/profile_detail.html', {
        'profile': profile,
        'serialized_data': serializer.data
    })


@login_required
def profile_create(request):
    if request.method == 'POST':
        serializer = PatientProfileCreateUpdateSerializer(data=request.POST)
        if serializer.is_valid():
            profile = serializer.save()
            messages.success(request, 'Patient profile created successfully.')
            return redirect('patient:profile-detail', guid=profile.guid)
        else:
            form = PatientProfileForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = PatientProfileForm()
        serializer = PatientProfileCreateUpdateSerializer()

    return render(request, 'patient/profile_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def profile_update(request, guid):
    profile = get_object_or_404(PatientProfile, guid=guid)

    if request.method == 'POST':
        serializer = PatientProfileCreateUpdateSerializer(profile, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Patient profile updated successfully.')
            return redirect('patient:profile-detail', guid=profile.guid)
        else:
            form = PatientProfileForm(request.POST, instance=profile)
            form.errors.update(serializer.errors)
    else:
        form = PatientProfileForm(instance=profile)
        serializer = PatientProfileCreateUpdateSerializer(profile)

    return render(request, 'patient/profile_form.html', {
        'form': form,
        'serialized_data': serializer.data
    })


@login_required
def insurance_list(request):
    insurance_policies = Insurance.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        insurance_policies = insurance_policies.filter(
            Q(patient__username__icontains=search_query) |
            Q(provider__icontains=search_query) |
            Q(policy_number__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(insurance_policies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = InsuranceListSerializer(page_obj, many=True)

    return render(request, 'patient/insurance_list.html', {
        'insurance_policies': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def insurance_create(request):
    if request.method == 'POST':
        serializer = InsuranceCreateUpdateSerializer(data=request.POST)
        if serializer.is_valid():
            insurance = serializer.save()
            messages.success(request, 'Insurance policy created successfully.')
            return redirect('patient:profile-detail', guid=insurance.patient.guid)
        else:
            form = InsuranceForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = InsuranceForm(initial={'patient': request.GET.get('patient')})
        serializer = InsuranceCreateUpdateSerializer()

    return render(request, 'patient/insurance_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def insurance_update(request, guid):
    insurance = get_object_or_404(Insurance, guid=guid)

    if request.method == 'POST':
        serializer = InsuranceCreateUpdateSerializer(insurance, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Insurance policy updated successfully.')
            return redirect('patient:profile-detail', guid=insurance.patient.guid)
        else:
            form = InsuranceForm(request.POST, instance=insurance)
            form.errors.update(serializer.errors)
    else:
        form = InsuranceForm(instance=insurance)
        serializer = InsuranceCreateUpdateSerializer(insurance)

    return render(request, 'patient/insurance_form.html', {
        'form': form,
        'serialized_data': serializer.data
    })


@login_required
def insurance_detail(request, guid):
    insurance = get_object_or_404(Insurance, guid=guid)
    serializer = InsuranceDetailSerializer(insurance)
    return render(request, 'patient/insurance_detail.html', {
        'insurance': insurance,
        'serialized_data': serializer.data
    })


@login_required
def emergency_contact_list(request):
    contacts = EmergencyContact.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contacts = contacts.filter(
            Q(patient__username__icontains=search_query) | Q(name__icontains=search_query) | Q(relationship__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = EmergencyContactListSerializer(page_obj, many=True)

    return render(request, 'patient/emergency_contact_list.html', {
        'contacts': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def emergency_contact_create(request):
    if request.method == 'POST':
        serializer = EmergencyContactCreateUpdateSerializer(data=request.POST)
        if serializer.is_valid():
            contact = serializer.save()
            messages.success(request, 'Emergency contact created successfully.')
            return redirect('patient:profile-detail', guid=contact.patient.guid)
        else:
            form = EmergencyContactForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = EmergencyContactForm(initial={'patient': request.GET.get('patient')})
        serializer = EmergencyContactCreateUpdateSerializer()

    return render(request, 'patient/emergency_contact_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def emergency_contact_update(request, guid):
    contact = get_object_or_404(EmergencyContact, guid=guid)

    if request.method == 'POST':
        serializer = EmergencyContactCreateUpdateSerializer(contact, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Emergency contact updated successfully.')
            return redirect('patient:profile-detail', guid=contact.patient.guid)
        else:
            form = EmergencyContactForm(request.POST, instance=contact)
            form.errors.update(serializer.errors)
    else:
        form = EmergencyContactForm(instance=contact)
        serializer = EmergencyContactCreateUpdateSerializer(contact)

    return render(request, 'patient/emergency_contact_form.html', {
        'form': form,
        'serialized_data': serializer.data
    })


@login_required
def emergency_contact_detail(request, guid):
    contact = get_object_or_404(EmergencyContact, guid=guid)
    serializer = EmergencyContactDetailSerializer(contact)
    return render(request, 'patient/emergency_contact_detail.html', {
        'contact': contact,
        'serialized_data': serializer.data
    })
