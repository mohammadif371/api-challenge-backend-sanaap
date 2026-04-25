from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer
from .filters import DocumentFilter
from .services import MinioService
from .tasks import upload_document_task
from users.permissions import IsAdmin, IsEditor, IsViewer


class DocumentListView(generics.ListAPIView):
    """
    GET /api/documents/
    All authenticated users can list documents
    Supports filtering and pagination
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsViewer]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DocumentFilter


class DocumentUploadView(generics.CreateAPIView):
    """
    POST /api/documents/upload/
    Only admin and editor can upload
    """
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsEditor]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data['file']

        # Create document with pending status
        document = Document.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
            file_name=file.name,
            file_size=file.size,
            uploaded_by=request.user,
            status=Document.Status.PENDING
        )

        # Send to background task for MinIO upload
        upload_document_task.delay(document.id, file.read(), file.name, file.content_type)

        return Response(
            DocumentSerializer(document).data,
            status=status.HTTP_201_CREATED
        )


class DocumentDetailView(generics.RetrieveAPIView):
    """
    GET /api/documents/<id>/
    All authenticated users can retrieve
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsViewer]


class DocumentUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/documents/<id>/update/
    Only admin and editor can update
    """
    queryset = Document.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsEditor]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        document = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # If new file uploaded
        if 'file' in serializer.validated_data:
            file = serializer.validated_data['file']
            try:
                service = MinioService()
                # Delete old file and upload new one
                new_path = service.update_file(
                    document.minio_path,
                    file,
                    file.name
                )
                document.minio_path = new_path
                document.file_name = file.name
                document.file_size = file.size
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Update other fields
        if 'title' in serializer.validated_data:
            document.title = serializer.validated_data['title']
        if 'description' in serializer.validated_data:
            document.description = serializer.validated_data['description']

        document.save()
        return Response(DocumentSerializer(document).data)


class DocumentDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/documents/<id>/delete/
    Only admin can delete
    """
    queryset = Document.objects.all()
    permission_classes = [IsAdmin]

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        try:
            service = MinioService()
            service.delete_file(document.minio_path)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)