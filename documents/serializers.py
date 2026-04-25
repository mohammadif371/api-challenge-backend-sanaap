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
        # URL امن از MinIO - بعداً پیاده سازی میکنیم
        return None


class DocumentUploadSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(write_only=True)

    class Meta:
        model = Document
        fields = ['title', 'description', 'file']

    def validate_file(self, value):
        # Max 10MB
        max_size = 10 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("File size must be under 10MB")
        return value