from .models import AuditLog


def get_client_ip(request):
    """Extract real IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AuditLogMiddleware:
    """
    Automatically log document-related actions
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only log authenticated users
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return response

        # Only log document endpoints
        if '/api/documents/' not in request.path:
            return response

        # Determine action based on method
        action = self._get_action(request.method)
        if not action:
            return response

        # Extract document id from URL if exists
        document_id = self._get_document_id(request.path)

        AuditLog.objects.create(
            user=request.user,
            action=action,
            document_id=document_id,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            extra_data={
                'path': request.path,
                'status_code': response.status_code
            }
        )

        return response

    def _get_action(self, method):
        mapping = {
            'GET': AuditLog.Action.VIEW,
            'POST': AuditLog.Action.UPLOAD,
            'PUT': AuditLog.Action.UPDATE,
            'PATCH': AuditLog.Action.UPDATE,
            'DELETE': AuditLog.Action.DELETE,
        }
        return mapping.get(method)

    def _get_document_id(self, path):
        """Extract document id from path like /api/documents/5/"""
        parts = [p for p in path.split('/') if p]
        for i, part in enumerate(parts):
            if part == 'documents' and i + 1 < len(parts):
                try:
                    return int(parts[i + 1])
                except ValueError:
                    return None
        return None