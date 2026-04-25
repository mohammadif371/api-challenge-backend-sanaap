from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'action',
            'document_id', 'document_title',
            'ip_address', 'extra_data',
            'created_at'
        ]