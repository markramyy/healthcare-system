from rest_framework.response import Response
from rest_framework.decorators import action

from django.http import HttpResponse
from django.db.models import Q
from functools import reduce

from healthcare_ms.core.base_viewset import BaseViewSet
from healthcare_ms.users.models import User
from healthcare_ms.users.serializers import (
    ListUserAdminSerializer, DetailUserAdminSerializer,
    UpdateUserAdminSerializer, UserPasswordChangeSerializer,
    ExportUserCSVSerializer, MeUserAdminSerializer
)

import csv
import operator
import logging

logger = logging.getLogger(__name__)


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    filterset_fields = ['user_type', 'is_verified']
    search_fields = ['username', 'email']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListUserAdminSerializer
        elif self.action == 'retrieve':
            return DetailUserAdminSerializer
        elif self.action == 'update':
            return UpdateUserAdminSerializer
        elif self.action == 'me':
            return MeUserAdminSerializer
        elif self.action == 'change_password':
            return UserPasswordChangeSerializer
        elif self.action == 'export_csv':
            return ExportUserCSVSerializer

    def get_paginated_response(self, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            current_page = self.paginator.page.number
            last_page = self.paginator.page.paginator.num_pages

            return Response({
                "count": self.paginator.page.paginator.count,
                "page": current_page,
                "last_page": last_page,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "message": "Users displayed successfully",
                "data": serializer.data,
            }, status=200)

        serializer = serializer_class(queryset, many=True)
        return Response({
            "message": "Users displayed successfully",
            "data": serializer.data
        }, status=200)

    def list(self, request, *args, **kwargs):
        users = self.filter_queryset(self.get_queryset())

        if not users:
            return Response({
                "message": "No users found",
                "data": []
            }, status=200)

        search_term = request.query_params.get('search')
        if search_term:
            search_fields = self.search_fields
            queries = [Q(**{f'{field}__icontains': search_term}) for field in search_fields]
            users = users.filter(reduce(operator.or_, queries))

        return self.get_paginated_response(users, self.get_serializer_class())

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return Response({
                "message": "User not found.",
                "data": {}
            }, status=404)

        serializer = self.get_serializer_class()(user)
        return Response({
            "message": "User displayed successfully.",
            "data": serializer.data
        }, status=200)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer_class()(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User updated successfully.",
                "data": serializer.data
            }, status=200)

        return Response({
            "message": "Failed to update user.",
            "errors": serializer.errors
        }, status=400)

    @action(detail=False, methods=['GET'], url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        """Retrieve user details."""
        serializer = self.get_serializer_class()(request.user)
        return Response(status=200, data=serializer.data)

    @action(detail=False, methods=['POST'], url_path='change-password', url_name='change-password')
    def change_password(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({
                "message": "User not authenticated.",
                "data": {}
            }, status=401)

        serializer = self.get_serializer_class()(user, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Password changed successfully.",
                "data": {}
            }, status=200)

        return Response({
            "message": "Failed to change password.",
            "errors": serializer.errors
        }, status=400)

    @action(detail=False, methods=['GET'], url_path='export-csv', url_name='export-csv')
    def export_csv(self, request):
        users = self.filter_queryset(self.get_queryset())

        if not users.exists():
            return Response({"message": "No users to export"}, status=404)

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(users, many=True)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users.csv"'

        field_names = serializer_class.Meta.fields if hasattr(serializer_class.Meta, 'fields') else []

        writer = csv.writer(response)
        writer.writerow(field_names)

        for row in serializer.data:
            row_values = [str(row.get(field, '')) for field in field_names]
            writer.writerow(row_values)

        return response
