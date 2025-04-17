from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
import csv
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View

from healthcare_ms.users.models import User
from healthcare_ms.users.serializers import (
    ListUserAdminSerializer,
    DetailUserAdminSerializer,
    UpdateUserAdminSerializer,
    UserPasswordChangeSerializer,
    ExportUserCSVSerializer,
    MeUserAdminSerializer,
    UserRegistrationSerializer
)
from healthcare_ms.users.forms import UserRegistrationForm
from healthcare_ms.core.decorators import role_required


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "data": DetailUserAdminSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to register user.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@login_required
def user_list(request):
    users = User.objects.all()

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # Filter by user type
    user_type = request.GET.get('user_type')
    if user_type:
        users = users.filter(user_type=user_type)

    # Filter by verification status
    is_verified = request.GET.get('is_verified')
    if is_verified is not None:
        users = users.filter(is_verified=is_verified.lower() == 'true')

    # Pagination
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Serialize the data
    serializer = ListUserAdminSerializer(page_obj, many=True)

    return render(request, 'users/user_list.html', {
        'users': page_obj,
        'is_paginated': True,
        'page_obj': page_obj,
        'serialized_data': serializer.data,
        'user_types': User.USER_TYPE_CHOICES
    })


@login_required
def user_detail(request, guid):
    user = get_object_or_404(User, guid=guid)
    serializer = DetailUserAdminSerializer(user)
    return render(request, 'users/user_detail.html', {
        'user': user,
        'serialized_data': serializer.data
    })


@login_required
def user_update(request, guid):
    user = get_object_or_404(User, guid=guid)

    if request.method == 'POST':
        serializer = UpdateUserAdminSerializer(user, data=request.POST, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'User updated successfully.')
            return redirect('users:user-detail', guid=user.guid)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        serializer = UpdateUserAdminSerializer(user)

    return render(request, 'users/user_form.html', {
        'user': user,
        'serialized_data': serializer.data
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        serializer = UserPasswordChangeSerializer(data=request.POST, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('users:user-detail', guid=request.user.guid)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        serializer = UserPasswordChangeSerializer()

    return render(request, 'users/change_password.html', {
        'serialized_data': serializer.data if hasattr(serializer, 'data') else None
    })


@login_required
def export_csv(request):
    users = User.objects.all()

    # Apply filters if present
    user_type = request.GET.get('user_type')
    if user_type:
        users = users.filter(user_type=user_type)

    is_verified = request.GET.get('is_verified')
    if is_verified is not None:
        users = users.filter(is_verified=is_verified.lower() == 'true')

    if not users.exists():
        messages.error(request, 'No users to export.')
        return redirect('users:user-list')

    serializer = ExportUserCSVSerializer(users, many=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    field_names = ExportUserCSVSerializer.Meta.fields

    writer = csv.writer(response)
    writer.writerow(field_names)

    for row in serializer.data:
        row_values = [str(row.get(field, '')) for field in field_names]
        writer.writerow(row_values)

    return response


@login_required
def me(request):
    serializer = MeUserAdminSerializer(request.user)
    return render(request, 'users/user_detail.html', {
        'user': request.user,
        'serialized_data': serializer.data,
        'is_me': True
    })


@login_required
@role_required('admin')
def delete_user(request, guid):
    user = get_object_or_404(User, guid=guid)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('users:user-list')
    return redirect('users:user-detail', guid=guid)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:home')
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:home')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'users/login.html', {'form': form})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            serializer = UserRegistrationSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                user = serializer.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('core:dashboard')
        return render(request, 'users/register.html', {'form': form})
