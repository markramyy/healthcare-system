from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

from healthcare_ms.ehr.models import MedicalRecord, Diagnosis, Treatment, Prescription
from healthcare_ms.ehr.forms import (
    MedicalRecordForm,
    DiagnosisForm,
    TreatmentForm,
    PrescriptionForm
)
from healthcare_ms.ehr.serializers import (
    MedicalRecordListSerializer,
    MedicalRecordDetailSerializer,
    MedicalRecordCreateSerializer,
    MedicalRecordUpdateSerializer,
    DiagnosisListSerializer,
    DiagnosisDetailSerializer,
    DiagnosisCreateSerializer,
    DiagnosisUpdateSerializer,
    TreatmentListSerializer,
    TreatmentDetailSerializer,
    TreatmentCreateSerializer,
    TreatmentUpdateSerializer,
    PrescriptionListSerializer,
    PrescriptionDetailSerializer,
    PrescriptionCreateSerializer,
    PrescriptionUpdateSerializer
)


@login_required
def medical_record_list(request):
    # Filter records based on user type
    if request.user.user_type == 'patient':
        records = MedicalRecord.objects.filter(patient=request.user)
    elif request.user.user_type == 'doctor':
        records = MedicalRecord.objects.filter(doctor=request.user)
    else:
        records = MedicalRecord.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        records = records.filter(
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(patient__username__icontains=search_query) |
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query) |
            Q(doctor__username__icontains=search_query) |
            Q(symptoms__icontains=search_query) |
            Q(notes__icontains=search_query) |
            Q(visit_date__icontains=search_query) |
            Q(follow_up_date__icontains=search_query)
        ).distinct()

    # Pagination
    paginator = Paginator(records, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = MedicalRecordListSerializer(page_obj, many=True)

    return render(request, 'ehr/medical_record_list.html', {
        'records': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data,
        'search_query': search_query
    })


@login_required
def medical_record_detail(request, guid):
    record = get_object_or_404(MedicalRecord, guid=guid)
    serializer = MedicalRecordDetailSerializer(record)
    return render(request, 'ehr/medical_record_detail.html', {
        'record': record,
        'serialized_data': serializer.data
    })


@login_required
def medical_record_create(request):
    if request.user.user_type == 'patient':
        messages.error(request, 'Patients are not allowed to create medical records.')
        return redirect('ehr:medical-record-list')

    patient_guid = request.GET.get('patient')
    initial_data = {
        'patient': patient_guid
    }

    if request.method == 'POST':
        serializer = MedicalRecordCreateSerializer(data=request.POST)
        if serializer.is_valid():
            record = serializer.save(doctor=request.user)
            messages.success(request, 'Medical record created successfully.')
            return redirect('patient:profile-detail', guid=record.patient.guid)
        else:
            form = MedicalRecordForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = MedicalRecordForm(initial=initial_data)
        serializer = MedicalRecordCreateSerializer(initial=initial_data)

    return render(request, 'ehr/medical_record_form.html', {
        'form': form,
        'serialized_data': serializer.initial if hasattr(serializer, 'initial') else None,
        'is_create': True
    })


@login_required
def medical_record_update(request, guid):
    if request.user.user_type == 'patient':
        messages.error(request, 'Patients are not allowed to update medical records.')
        return redirect('ehr:medical-record-list')

    record = get_object_or_404(MedicalRecord, guid=guid)

    # Check if the authenticated user is the doctor who created the record
    if request.user.user_type == 'doctor' and record.doctor != request.user:
        messages.error(request, 'You are not authorized to update this medical record.')
        return redirect('ehr:medical-record-list')

    if request.method == 'POST':
        serializer = MedicalRecordUpdateSerializer(record, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Medical record updated successfully.')
            return redirect('ehr:medical-record-detail', guid=record.guid)
        else:
            form = MedicalRecordForm(request.POST, instance=record)
            form.errors.update(serializer.errors)
    else:
        form = MedicalRecordForm(instance=record)
        serializer = MedicalRecordUpdateSerializer(record)

    return render(request, 'ehr/medical_record_form.html', {
        'form': form,
        'serialized_data': serializer.data,
        'is_create': False
    })


@login_required
def medical_record_delete(request, guid):
    record = get_object_or_404(MedicalRecord, guid=guid)

    # Check if the authenticated user is the doctor who created the record
    if request.user.user_type == 'doctor' and record.doctor != request.user:
        messages.error(request, 'You are not authorized to delete this medical record.')
        return redirect('ehr:medical-record-list')

    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Medical record deleted successfully.')
        return redirect('ehr:medical-record-list')

    return render(request, 'ehr/medical_record_confirm_delete.html', {
        'record': record
    })


@login_required
def diagnosis_list(request):
    # Filter diagnoses based on user type
    if request.user.user_type == 'patient':
        diagnoses = Diagnosis.objects.filter(medical_record__patient=request.user)
    elif request.user.user_type == 'doctor':
        diagnoses = Diagnosis.objects.filter(medical_record__doctor=request.user)
    else:
        diagnoses = Diagnosis.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        diagnoses = diagnoses.filter(
            Q(diagnosis_code__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(diagnoses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = DiagnosisListSerializer(page_obj, many=True)

    return render(request, 'ehr/diagnosis_list.html', {
        'diagnoses': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def diagnosis_detail(request, guid):
    diagnosis = get_object_or_404(Diagnosis, guid=guid)
    serializer = DiagnosisDetailSerializer(diagnosis)
    return render(request, 'ehr/diagnosis_detail.html', {
        'diagnosis': diagnosis,
        'serialized_data': serializer.data
    })


@login_required
def diagnosis_create(request):
    if request.method == 'POST':
        serializer = DiagnosisCreateSerializer(data=request.POST)
        if serializer.is_valid():
            diagnosis = serializer.save()
            messages.success(request, 'Diagnosis created successfully.')
            return redirect('ehr:diagnosis-detail', guid=diagnosis.guid)
        else:
            form = DiagnosisForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = DiagnosisForm()
        # Filter medical records by authenticated doctor
        if request.user.user_type == 'doctor':
            form.fields['medical_record'].queryset = MedicalRecord.objects.filter(doctor=request.user)
        serializer = DiagnosisCreateSerializer()

    return render(request, 'ehr/diagnosis_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None,
        'is_create': True
    })


@login_required
def diagnosis_update(request, guid):
    diagnosis = get_object_or_404(Diagnosis, guid=guid)

    # Check if the authenticated user is the doctor who created the medical record
    if request.user.user_type == 'doctor' and diagnosis.medical_record.doctor != request.user:
        messages.error(request, 'You are not authorized to update this diagnosis.')
        return redirect('ehr:diagnosis-list')

    if request.method == 'POST':
        serializer = DiagnosisUpdateSerializer(diagnosis, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Diagnosis updated successfully.')
            return redirect('ehr:diagnosis-detail', guid=diagnosis.guid)
        else:
            form = DiagnosisForm(request.POST, instance=diagnosis)
            form.errors.update(serializer.errors)
    else:
        form = DiagnosisForm(instance=diagnosis)
        # Filter medical records by authenticated doctor
        if request.user.user_type == 'doctor':
            form.fields['medical_record'].queryset = MedicalRecord.objects.filter(doctor=request.user)
        serializer = DiagnosisUpdateSerializer(diagnosis)

    return render(request, 'ehr/diagnosis_form.html', {
        'form': form,
        'serialized_data': serializer.data,
        'is_create': False
    })


@login_required
def diagnosis_delete(request, guid):
    diagnosis = get_object_or_404(Diagnosis, guid=guid)

    # Check if the authenticated user is the doctor who created the medical record
    if request.user.user_type == 'doctor' and diagnosis.medical_record.doctor != request.user:
        messages.error(request, 'You are not authorized to delete this diagnosis.')
        return redirect('ehr:diagnosis-list')

    if request.method == 'POST':
        diagnosis.delete()
        messages.success(request, 'Diagnosis deleted successfully.')
        return redirect('ehr:diagnosis-list')

    return render(request, 'ehr/diagnosis_confirm_delete.html', {
        'diagnosis': diagnosis
    })


@login_required
def treatment_list(request):
    # Filter treatments based on user type
    if request.user.user_type == 'patient':
        treatments = Treatment.objects.filter(medical_record__patient=request.user)
    elif request.user.user_type == 'doctor':
        treatments = Treatment.objects.filter(medical_record__doctor=request.user)
    else:
        treatments = Treatment.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        treatments = treatments.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(treatments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = TreatmentListSerializer(page_obj, many=True)

    return render(request, 'ehr/treatment_list.html', {
        'treatments': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data
    })


@login_required
def treatment_detail(request, guid):
    treatment = get_object_or_404(Treatment, guid=guid)
    serializer = TreatmentDetailSerializer(treatment)
    return render(request, 'ehr/treatment_detail.html', {
        'treatment': treatment,
        'serialized_data': serializer.data
    })


@login_required
def treatment_create(request):
    if request.method == 'POST':
        serializer = TreatmentCreateSerializer(data=request.POST)
        if serializer.is_valid():
            treatment = serializer.save()
            messages.success(request, 'Treatment created successfully.')
            return redirect('ehr:treatment-detail', guid=treatment.guid)
        else:
            form = TreatmentForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = TreatmentForm()
        # Filter medical records by authenticated doctor
        if request.user.user_type == 'doctor':
            form.fields['medical_record'].queryset = MedicalRecord.objects.filter(doctor=request.user)
        serializer = TreatmentCreateSerializer()

    return render(request, 'ehr/treatment_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None,
        'is_create': True
    })


@login_required
def treatment_update(request, guid):
    treatment = get_object_or_404(Treatment, guid=guid)

    # Check if the authenticated user is the doctor who created the medical record
    if request.user.user_type == 'doctor' and treatment.medical_record.doctor != request.user:
        messages.error(request, 'You are not authorized to update this treatment.')
        return redirect('ehr:treatment-list')

    if request.method == 'POST':
        serializer = TreatmentUpdateSerializer(treatment, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Treatment updated successfully.')
            return redirect('ehr:treatment-detail', guid=treatment.guid)
        else:
            form = TreatmentForm(request.POST, instance=treatment)
            form.errors.update(serializer.errors)
    else:
        form = TreatmentForm(instance=treatment)
        # Filter medical records by authenticated doctor
        if request.user.user_type == 'doctor':
            form.fields['medical_record'].queryset = MedicalRecord.objects.filter(doctor=request.user)
        serializer = TreatmentUpdateSerializer(treatment)

    return render(request, 'ehr/treatment_form.html', {
        'form': form,
        'serialized_data': serializer.data,
        'is_create': False
    })


@login_required
def treatment_delete(request, guid):
    treatment = get_object_or_404(Treatment, guid=guid)

    # Check if the authenticated user is the doctor who created the medical record
    if request.user.user_type == 'doctor' and treatment.medical_record.doctor != request.user:
        messages.error(request, 'You are not authorized to delete this treatment.')
        return redirect('ehr:treatment-list')

    if request.method == 'POST':
        treatment.delete()
        messages.success(request, 'Treatment deleted successfully.')
        return redirect('ehr:treatment-list')

    return render(request, 'ehr/treatment_confirm_delete.html', {
        'treatment': treatment
    })


@login_required
def prescription_list(request):
    # Filter prescriptions based on user type
    if request.user.user_type == 'patient':
        prescriptions = Prescription.objects.filter(medical_record__patient=request.user)
    elif request.user.user_type == 'doctor':
        prescriptions = Prescription.objects.filter(medical_record__doctor=request.user)
    else:
        prescriptions = Prescription.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        prescriptions = prescriptions.filter(
            Q(medication_name__icontains=search_query) |
            Q(dosage__icontains=search_query) |
            Q(frequency__icontains=search_query) |
            Q(duration__icontains=search_query) |
            Q(instructions__icontains=search_query) |
            Q(medical_record__patient__first_name__icontains=search_query) |
            Q(medical_record__patient__last_name__icontains=search_query) |
            Q(medical_record__patient__username__icontains=search_query) |
            Q(medical_record__doctor__first_name__icontains=search_query) |
            Q(medical_record__doctor__last_name__icontains=search_query) |
            Q(medical_record__doctor__username__icontains=search_query) |
            Q(created__icontains=search_query)
        ).distinct()

    # Pagination
    paginator = Paginator(prescriptions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = PrescriptionListSerializer(page_obj, many=True)

    return render(request, 'ehr/prescription_list.html', {
        'prescriptions': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data,
        'search_query': search_query
    })


@login_required
def prescription_detail(request, guid):
    prescription = get_object_or_404(Prescription, guid=guid)
    serializer = PrescriptionDetailSerializer(prescription)
    return render(request, 'ehr/prescription_detail.html', {
        'prescription': prescription,
        'serialized_data': serializer.data
    })


@login_required
def prescription_create(request):
    if request.user.user_type == 'patient':
        messages.error(request, 'Patients are not allowed to create prescriptions.')
        return redirect('ehr:prescription-list')

    if request.method == 'POST':
        serializer = PrescriptionCreateSerializer(data=request.POST)
        if serializer.is_valid():
            prescription = serializer.save()
            messages.success(request, 'Prescription created successfully.')
            return redirect('ehr:prescription-detail', guid=prescription.guid)
        else:
            form = PrescriptionForm(request.POST)
            form.errors.update(serializer.errors)
    else:
        form = PrescriptionForm()
        serializer = PrescriptionCreateSerializer()

    return render(request, 'ehr/prescription_form.html', {
        'form': form,
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def prescription_update(request, guid):
    if request.user.user_type == 'patient':
        messages.error(request, 'Patients are not allowed to update prescriptions.')
        return redirect('ehr:prescription-list')

    prescription = get_object_or_404(Prescription, guid=guid)

    if request.method == 'POST':
        serializer = PrescriptionUpdateSerializer(prescription, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Prescription updated successfully.')
            return redirect('ehr:prescription-detail', guid=prescription.guid)
        else:
            form = PrescriptionForm(request.POST, instance=prescription)
            form.errors.update(serializer.errors)
    else:
        form = PrescriptionForm(instance=prescription)
        serializer = PrescriptionUpdateSerializer(prescription)

    return render(request, 'ehr/prescription_form.html', {
        'form': form,
        'serialized_data': serializer.data
    })


@login_required
def prescription_delete(request, guid):
    prescription = get_object_or_404(Prescription, guid=guid)

    # Check if the authenticated user is the doctor who created the medical record
    if request.user.user_type == 'doctor' and prescription.medical_record.doctor != request.user:
        messages.error(request, 'You are not authorized to delete this prescription.')
        return redirect('ehr:prescription-list')

    if request.method == 'POST':
        prescription.delete()
        messages.success(request, 'Prescription deleted successfully.')
        return redirect('ehr:prescription-list')

    return render(request, 'ehr/prescription_confirm_delete.html', {
        'prescription': prescription
    })
