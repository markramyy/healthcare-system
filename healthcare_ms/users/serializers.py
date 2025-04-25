from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from healthcare_ms.core.base_serializer import BaseSerializer
from healthcare_ms.users.models import User


class ListUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ('guid', 'username', 'email', 'user_type')


class DetailUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'guid', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'profile_picture', 'is_verified'
        )


class UpdateUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'address', 'profile_picture'
        )


class MeUserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'guid', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'profile_picture', 'is_verified'
        )


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is not correct"))
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"new_password": _("Password fields didn't match.")}
            )
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ExportUserCSVSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth', 'address',
            'is_verified', 'created', 'modified'
        )


class UserRegistrationSerializer(BaseSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password2',
            'user_type'
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
