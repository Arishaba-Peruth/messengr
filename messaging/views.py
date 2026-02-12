from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from .models import Message

class MessageCreateView(APIView):

    @swagger_auto_schema(
        request_body=MessageSerializer,
        responses={201: MessageSerializer}
    )
    def post(self, request):
        sender = User.objects.first()
        recipient = User.objects.last()
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=sender, recipient=recipient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class InboxView(APIView):

    @swagger_auto_schema(
        responses={200: MessageSerializer(many=True)}
    )
    def get(self, request):
        user = User.objects.last()
        msgs = Message.objects.filter(recipient=user)
        serializer = MessageSerializer(msgs, many=True)
        return Response(serializer.data)
    
class MessageDeleteView(APIView):
    @swagger_auto_schema( responses={204: 'No Content'} )
    def delete(self, request, pk):
        try:
            msg = Message.objects.get(pk=pk)
            msg.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    