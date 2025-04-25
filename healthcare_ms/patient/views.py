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
    PatientProfileCreateSerializer,
    PatientProfileUpdateSerializer,
    InsuranceListSerializer,
    InsuranceDetailSerializer,
    InsuranceCreateSerializer,
    InsuranceUpdateSerializer,
    EmergencyContactListSerializer,
    EmergencyContactDetailSerializer,
    EmergencyContactCreateSerializer,
    EmergencyContactUpdateSerializer
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
        serializer = PatientProfileCreateSerializer(data=request.POST)
        if serializer.is_valid():
            profile = serializer.save()
            messages.success(request, 'Patient profile created successfully.')
            return redirect('patient:profile-detail', guid=profile.guid)
        else:
            form = PatientProfileForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = PatientProfileForm()
        serializer = PatientProfileCreateSerializer()

    return render(request, 'patient/profile_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def profile_update(request, guid):
    profile = get_object_or_404(PatientProfile, guid=guid)

    if request.method == 'POST':
        serializer = PatientProfileUpdateSerializer(profile, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Patient profile updated successfully.')
            return redirect('patient:profile-detail', guid=profile.guid)
        else:
            form = PatientProfileForm(request.POST, instance=profile)
            form.errors.update(serializer.errors)
    else:
        form = PatientProfileForm(instance=profile)
        serializer = PatientProfileUpdateSerializer(profile)

    return render(request, 'patient/profile_form.html', {
        'form': form,
        'profile': profile,
        'serialized_data': serializer.data
    })


@login_required
def insurance_list(request):
    # Only allow patients to access their own insurance policies
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can access their insurance policies.')
        return redirect('home')

    insurance_policies = Insurance.objects.filter(patient=request.user)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        insurance_policies = insurance_policies.filter(
            Q(provider__icontains=search_query) |
            Q(policy_number__icontains=search_query) |
            Q(group_number__icontains=search_query)
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
        'serialized_data': serializer.data,
        'search_query': search_query
    })


@login_required
def insurance_create(request):
    # Only allow patients to create insurance policies
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can create insurance policies.')
        return redirect('home')

    if request.method == 'POST':
        data = request.POST.copy()
        data['patient'] = request.user.id

        # Handle decimal fields
        for field in ['deductible', 'copayment', 'coinsurance', 'out_of_pocket_max']:
            if field in data and data[field]:
                try:
                    data[field] = float(data[field])
                except (ValueError, TypeError):
                    data[field] = 0

        serializer = InsuranceCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Insurance policy created successfully.')
            return redirect('patient:insurance-list')
        else:
            form = InsuranceForm(request.POST)
            form.errors.update(serializer.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InsuranceForm()
        serializer = InsuranceCreateSerializer()

    return render(request, 'patient/insurance_form.html', {
        'form': form,
        'serialized_data': serializer.initial if hasattr(serializer, 'initial') else None,
        'is_create': True
    })


@login_required
def insurance_update(request, guid):
    # Only allow patients to update their own insurance policies
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can update their insurance policies.')
        return redirect('home')

    insurance = get_object_or_404(Insurance, guid=guid)

    # Check if the insurance belongs to the current user
    if insurance.patient != request.user:
        messages.error(request, 'You can only update your own insurance policies.')
        return redirect('patient:insurance-list')

    if request.method == 'POST':
        data = request.POST.copy()
        data['patient'] = request.user.id

        # Handle decimal fields
        for field in ['deductible', 'copayment', 'coinsurance', 'out_of_pocket_max']:
            if field in data and data[field]:
                try:
                    data[field] = float(data[field])
                except (ValueError, TypeError):
                    data[field] = 0

        serializer = InsuranceUpdateSerializer(insurance, data=data)

        if serializer.is_valid():
            updated_insurance = serializer.save()
            messages.success(request, 'Insurance policy updated successfully.')
            return redirect('patient:insurance-detail', guid=updated_insurance.guid)
        else:
            form = InsuranceForm(request.POST, instance=insurance)
            form.errors.update(serializer.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = InsuranceForm(instance=insurance)
        serializer = InsuranceUpdateSerializer(insurance)

    return render(request, 'patient/insurance_form.html', {
        'form': form,
        'insurance': insurance,
        'serialized_data': serializer.data,
        'is_create': False
    })


@login_required
def insurance_delete(request, guid):
    # Only allow patients to delete their own insurance policies
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can delete their insurance policies.')
        return redirect('home')

    insurance = get_object_or_404(Insurance, guid=guid)

    # Check if the insurance belongs to the current user
    if insurance.patient != request.user:
        messages.error(request, 'You can only delete your own insurance policies.')
        return redirect('patient:insurance-list')

    if request.method == 'POST':
        insurance.delete()
        messages.success(request, 'Insurance policy deleted successfully.')
        return redirect('patient:insurance-list')

    return render(request, 'patient/insurance_confirm_delete.html', {
        'insurance': insurance
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
    # Only allow patients to access their own emergency contacts
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can access their emergency contacts.')
        return redirect('home')

    contacts = EmergencyContact.objects.filter(patient=request.user)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contacts = contacts.filter(
            Q(name__icontains=search_query) |
            Q(relationship__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query)
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
        'serialized_data': serializer.data,
        'search_query': search_query
    })


@login_required
def emergency_contact_create(request):
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can create emergency contacts.')
        return redirect('home')

    if request.method == 'POST':
        data = request.POST.copy()
        data['patient'] = request.user.id

        serializer = EmergencyContactCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Emergency contact created successfully.')
            return redirect('patient:emergency-contact-list')
        else:
            form = EmergencyContactForm(request.POST)
            form.errors.update(serializer.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmergencyContactForm()
        serializer = EmergencyContactCreateSerializer()

    return render(request, 'patient/emergency_contact_form.html', {
        'form': form,
        'serialized_data': serializer.initial if hasattr(serializer, 'initial') else None,
        'is_create': True
    })


@login_required
def emergency_contact_update(request, guid):
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can update their emergency contacts.')
        return redirect('home')

    contact = get_object_or_404(EmergencyContact, guid=guid)

    if contact.patient != request.user:
        messages.error(request, 'You can only update your own emergency contacts.')
        return redirect('patient:emergency-contact-list')

    if request.method == 'POST':
        data = request.POST.copy()
        data['patient'] = request.user.id
        serializer = EmergencyContactUpdateSerializer(contact, data=data)

        if serializer.is_valid():
            updated_contact = serializer.save()
            messages.success(request, 'Emergency contact updated successfully.')
            return redirect('patient:emergency-contact-detail', guid=updated_contact.guid)
        else:
            form = EmergencyContactForm(request.POST, instance=contact)
            form.errors.update(serializer.errors)
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmergencyContactForm(instance=contact)
        serializer = EmergencyContactUpdateSerializer(contact)

    return render(request, 'patient/emergency_contact_form.html', {
        'form': form,
        'contact': contact,
        'serialized_data': serializer.data,
        'is_create': False
    })


@login_required
def emergency_contact_detail(request, guid):
    contact = get_object_or_404(EmergencyContact, guid=guid)
    serializer = EmergencyContactDetailSerializer(contact)
    return render(request, 'patient/emergency_contact_detail.html', {
        'contact': contact,
        'serialized_data': serializer.data
    })


@login_required
def emergency_contact_delete(request, guid):
    if request.user.user_type != 'patient':
        messages.error(request, 'Only patients can delete their emergency contacts.')
        return redirect('home')

    contact = get_object_or_404(EmergencyContact, guid=guid)

    if contact.patient != request.user:
        messages.error(request, 'You can only delete your own emergency contacts.')
        return redirect('patient:emergency-contact-list')

    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Emergency contact deleted successfully.')
        return redirect('patient:emergency-contact-list')

    return render(request, 'patient/emergency_contact_confirm_delete.html', {
        'contact': contact
    })
