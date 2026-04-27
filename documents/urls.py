from django.urls import path
from .views import (
    DocumentBatchUploadView,
    DocumentListView,
    DocumentUploadView,
    DocumentDetailView,
    DocumentUpdateView,
    DocumentDeleteView
)

urlpatterns = [
    path('documents/', DocumentListView.as_view(), name='document-list'),
    path('documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
     path('documents/batch-upload/', DocumentBatchUploadView.as_view(), name='document-batch-upload'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    path('documents/<int:pk>/update/', DocumentUpdateView.as_view(), name='document-update'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document-delete'),
]