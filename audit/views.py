from rest_framework import generics
from .models import AuditLog
from .serializers import AuditLogSerializer
from users.permissions import IsAdmin


class AuditLogListView(generics.ListAPIView):
    """Only admin can see audit logs"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]