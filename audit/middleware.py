from .models import AuditLog
from documents.models import Document


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AuditLogMiddleware:
    """Automatically log document-related actions"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return response

        if '/api/documents/' not in request.path:
            return response

        action = self._get_action(request.method)
        if not action:
            return response

        document_id = self._get_document_id(request.path)
        document_title = self._get_document_title(document_id)

        AuditLog.objects.create(
            user=request.user,
            action=action,
            document_id=document_id,
            document_title=document_title,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            extra_data={
                'path': request.path,
                'status_code': response.status_code
            }
        )

        return response

    def _get_action(self, method):
        return {
            'GET': AuditLog.Action.VIEW,
            'POST': AuditLog.Action.UPLOAD,
            'PUT': AuditLog.Action.UPDATE,
            'PATCH': AuditLog.Action.UPDATE,
            'DELETE': AuditLog.Action.DELETE,
        }.get(method)

    def _get_document_id(self, path):
        parts = [p for p in path.split('/') if p]
        for i, part in enumerate(parts):
            if part == 'documents' and i + 1 < len(parts):
                try:
                    return int(parts[i + 1])
                except ValueError:
                    return None
        return None

    def _get_document_title(self, document_id):
        if document_id is None:
            return None
        try:
            return Document.objects.values_list('title', flat=True).get(id=document_id)
        except Document.DoesNotExist:
            return None