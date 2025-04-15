from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    lookup_field = 'guid'
    read_only_fields = ['created', 'modified']


class AdminBaseSerializer(serializers.ModelSerializer):
    lookup_field = 'guid'
    read_only_fields = ['created', 'modified']
