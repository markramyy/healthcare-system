from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from healthcare_ms.core.base_serializer import BaseSerializer
from healthcare_ms.users.models import User


class ListUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'is_active', 'created', 'modified')


class DetailUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'profile_picture', 'is_verified', 'is_active', 'created', 'modified'
        )


class UpdateUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'address', 'profile_picture', 'is_active'
        )


class MeUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'profile_picture', 'is_verified', 'created', 'modified'
        )


class UserPasswordChangeSerializer(BaseSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": _("Password fields didn't match.")}
            )
        return attrs


class ExportUserCSVSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'is_verified', 'is_active', 'created', 'modified'
        )


class ExportUserJSONSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'profile_picture', 'is_verified', 'is_active', 'created', 'modified'
        )


class UserRegistrationSerializer(BaseSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'user_type',
            'phone_number', 'date_of_birth', 'address'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": _("Password fields didn't match.")}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'profile_picture', 'is_verified', 'created', 'modified'
        )
        read_only_fields = ('id', 'username', 'created', 'modified')


class UserLoginSerializer(BaseSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
