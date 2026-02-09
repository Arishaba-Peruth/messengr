from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer

class MessageCreateView(APIView):
    """
    POST /api/messages/
    Create a new message and send it to a recipient.
    
    Requires authentication. The authenticated user becomes the sender.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Create a message from the authenticated user to a recipient."""
        # Add the authenticated user as the sender
        data = request.data.copy()
        data['sender'] = request.user.id
        
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            msg = serializer.save()
            return Response(
                {
                    "id": msg.id,
                    "sender": msg.sender.id,
                    "recipient": msg.recipient.id,
                    "text": msg.text,
                    "language": msg.language,
                    "translated_text": msg.translated_text()
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InboxView(APIView):
    """
    GET /api/messages/inbox/
    Retrieve all messages received by the authenticated user.
    
    Messages are returned with text translated to the recipient's preferred language.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all messages for the authenticated user, translated to their language."""
        # Get all messages where the authenticated user is the recipient
        msgs = Message.objects.filter(recipient=request.user).select_related('sender')
        
        # Serialize the messages
        serializer = MessageSerializer(msgs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
