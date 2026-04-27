from celery import shared_task
from .models import Document
from .services import MinioService
import io


@shared_task(bind=True, max_retries=3)
def upload_document_task(self, document_id: int, file_data: bytes, file_name: str, content_type: str):
    """
    Background task to upload document to MinIO
    Retries 3 times if fails
    """
    try:
        # Get document
        document = Document.objects.get(id=document_id)
        document.status = Document.Status.PENDING
        document.save()

        # Upload to MinIO
        service = MinioService()

        # Convert bytes back to file-like object
        file_obj = io.BytesIO(file_data)
        file_obj.size = len(file_data)
        file_obj.content_type = content_type

        path = service.upload_file(file_obj, file_name)

        # Update document status
        document.minio_path = path
        document.status = Document.Status.STORED
        document.save()

        # Notify via WebSocket 
        notify_document_update.delay(document_id, 'created')

        return {'status': 'success', 'document_id': document_id}

    except Document.DoesNotExist:
        return {'status': 'error', 'message': 'Document not found'}

    except Exception as exc:
        # Update status to failed
        Document.objects.filter(id=document_id).update(
            status=Document.Status.FAILED
        )
        # Retry after 5 seconds
        raise self.retry(exc=exc, countdown=5)


@shared_task
def notify_document_update(document_id: int, action: str):
    """
    Background task to send WebSocket notification
    """
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'documents',
        {
            'type': 'document_update',
            'document_id': document_id,
            'action': action
        }
    )