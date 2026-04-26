import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Client connected to WebSocket"""
        # All clients join the 'documents' group
        await self.channel_layer.group_add(
            'documents',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Client disconnected"""
        await self.channel_layer.group_discard(
            'documents',
            self.channel_name
        )

    async def document_update(self, event):
        """
        Receive message from channel layer
        and send to WebSocket client
        """
        await self.send(text_data=json.dumps({
            'document_id': event['document_id'],
            'action': event['action'],
            'message': f"Document {event['document_id']} was {event['action']}"
        }))