from documents.services import MinioService
from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description',
            'file_name', 'file_size', 'status',
            'uploaded_by', 'url',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'file_name', 'file_size',
            'minio_path', 'status',
            'uploaded_by', 'created_at', 'updated_at'
        ]

    def get_url(self, obj):
        if not obj.minio_path:
            return None
        try:
            service = MinioService()
            return service.get_presigned_url(obj.minio_path)
        except Exception:
            return None


class DocumentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for update - all fields optional"""
    file = serializers.FileField(write_only=True, required=False)
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Document
        fields = ['title', 'description', 'file']

    def validate_file(self, value):
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size must be under 10MB")
        
        allowed_types = [
            'image/jpeg', 'image/png', 'image/gif',
            'application/pdf', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("File type not allowed")
        return value