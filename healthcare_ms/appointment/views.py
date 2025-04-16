from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from healthcare_ms.appointment.models import AppointmentType, AppointmentSlot, Appointment
from healthcare_ms.appointment.forms import AppointmentSlotForm, AppointmentForm
from healthcare_ms.appointment.serializers import (
    AppointmentTypeListSerializer,
    AppointmentTypeDetailSerializer,
    AppointmentTypeCreateSerializer,
    AppointmentTypeUpdateSerializer,
    AppointmentSlotListSerializer,
    AppointmentSlotDetailSerializer,
    AppointmentListSerializer,
    AppointmentDetailSerializer,
)


@login_required
def appointment_type_list(request):
    """View for listing appointment types."""
    search_query = request.GET.get('search', '')
    page_number = request.GET.get('page', 1)

    appointment_types = AppointmentType.objects.all()

    if search_query:
        appointment_types = appointment_types.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(appointment_types, 10)
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = AppointmentTypeListSerializer(page_obj, many=True)

    context = {
        'appointment_types': page_obj,
        'search_query': search_query,
        'serialized_data': serializer.data
    }
    return render(request, 'appointment/appointment_type_list.html', context)


@login_required
def appointment_type_detail(request, guid):
    """View for displaying appointment type details."""
    appointment_type = get_object_or_404(AppointmentType, guid=guid)
    serializer = AppointmentTypeDetailSerializer(appointment_type)
    context = {
        'appointment_type': appointment_type,
        'serialized_data': serializer.data
    }
    return render(request, 'appointment/appointment_type_detail.html', context)


@login_required
def appointment_type_create(request):
    """View for creating a new appointment type."""
    if request.method == 'POST':
        serializer = AppointmentTypeCreateSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, _('Appointment type created successfully.'))
            return redirect('appointment:appointment-type-list')
        else:
            messages.error(request, _('Failed to create appointment type.'))
    else:
        serializer = AppointmentTypeCreateSerializer()

    context = {
        'form': serializer,
    }
    return render(request, 'appointment/appointment_type_form.html', context)


@login_required
def appointment_type_update(request, guid):
    """View for updating an appointment type."""
    appointment_type = get_object_or_404(AppointmentType, guid=guid)

    if request.method == 'POST':
        serializer = AppointmentTypeUpdateSerializer(instance=appointment_type, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, _('Appointment type updated successfully.'))
            return redirect('appointment:appointment-type-list')
        else:
            messages.error(request, _('Failed to update appointment type.'))
    else:
        serializer = AppointmentTypeUpdateSerializer(instance=appointment_type)

    context = {
        'form': serializer,
        'appointment_type': appointment_type,
    }
    return render(request, 'appointment/appointment_type_form.html', context)


@login_required
def appointment_slot_list(request):
    """View for listing appointment slots."""
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page_number = request.GET.get('page', 1)

    appointment_slots = AppointmentSlot.objects.all()

    if search_query:
        appointment_slots = appointment_slots.filter(
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query)
        )

    if start_date and end_date:
        appointment_slots = appointment_slots.filter(date__range=[start_date, end_date])

    paginator = Paginator(appointment_slots, 10)
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = AppointmentSlotListSerializer(page_obj, many=True)

    context = {
        'appointment_slots': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'serialized_data': serializer.data
    }
    return render(request, 'appointment/appointment_slot_list.html', context)


@login_required
def appointment_slot_detail(request, guid):
    """View for displaying appointment slot details."""
    appointment_slot = get_object_or_404(AppointmentSlot, guid=guid)
    serializer = AppointmentSlotDetailSerializer(appointment_slot)
    context = {
        'appointment_slot': appointment_slot,
        'serialized_data': serializer.data
    }
    return render(request, 'appointment/appointment_slot_detail.html', context)


@login_required
def appointment_slot_create(request):
    """View for creating a new appointment slot."""
    if request.method == 'POST':
        form = AppointmentSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment slot created successfully.'))
            return redirect('appointment:appointment-slot-list')
        else:
            messages.error(request, _('Failed to create appointment slot.'))
    else:
        form = AppointmentSlotForm()

    context = {
        'form': form,
    }
    return render(request, 'appointment/appointment_slot_form.html', context)


@login_required
def appointment_slot_update(request, guid):
    """View for updating an appointment slot."""
    appointment_slot = get_object_or_404(AppointmentSlot, guid=guid)

    if request.method == 'POST':
        form = AppointmentSlotForm(request.POST, instance=appointment_slot)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment slot updated successfully.'))
            return redirect('appointment:appointment-slot-list')
        else:
            messages.error(request, _('Failed to update appointment slot.'))
    else:
        form = AppointmentSlotForm(instance=appointment_slot)

    context = {
        'form': form,
        'appointment_slot': appointment_slot,
    }
    return render(request, 'appointment/appointment_slot_form.html', context)


@login_required
def appointment_list(request):
    """View for listing appointments."""
    search_query = request.GET.get('search', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    page_number = request.GET.get('page', 1)

    appointments = Appointment.objects.all()

    if search_query:
        appointments = appointments.filter(
            Q(patient__first_name__icontains=search_query) |
            Q(patient__last_name__icontains=search_query) |
            Q(doctor__first_name__icontains=search_query) |
            Q(doctor__last_name__icontains=search_query) |
            Q(reason__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    if start_date and end_date:
        appointments = appointments.filter(slot__date__range=[start_date, end_date])

    paginator = Paginator(appointments, 10)
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = AppointmentListSerializer(page_obj, many=True)

    context = {
        'appointments': page_obj,
        'search_query': search_query,
        'start_date': start_date,
        'end_date': end_date,
        'serialized_data': serializer.data
    }
    return render(request, 'appointment/appointment_list.html', context)


@login_required
def appointment_detail(request, guid):
    """View for displaying appointment details."""
    appointment = get_object_or_404(Appointment, guid=guid)
    serializer = AppointmentDetailSerializer(appointment)
    context = {
        'appointment': appointment,
        'serialized_data': serializer.data
    }
    return render(request, 'appointment/appointment_detail.html', context)


@login_required
def appointment_create(request):
    """View for creating a new appointment."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment created successfully.'))
            return redirect('appointment:appointment-list')
        else:
            messages.error(request, _('Failed to create appointment.'))
    else:
        form = AppointmentForm()

    context = {
        'form': form,
    }
    return render(request, 'appointment/appointment_form.html', context)


@login_required
def appointment_update(request, guid):
    """View for updating an appointment."""
    appointment = get_object_or_404(Appointment, guid=guid)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, _('Appointment updated successfully.'))
            return redirect('appointment:appointment-list')
        else:
            messages.error(request, _('Failed to update appointment.'))
    else:
        form = AppointmentForm(instance=appointment)
    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'appointment/appointment_form.html', context)
