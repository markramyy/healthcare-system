from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django_filters.rest_framework import DjangoFilterBackend

from healthcare_ms.core.pagination import StandardResultsSetPagination


class MethodNotAllowed(APIException):
    status_code = 405
    default_detail = 'Method not allowed in this app.'
    default_code = 'method_not_allowed'


class BaseViewSet(viewsets.GenericViewSet):
    ...
    lookup_field = 'guid'
    ...

    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
