from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer

class MessageCreateView(APIView):
 def post(self, request):
     #sender = User.objects.first()
     #recipient = User.objects.last()
     #data = {"sender": sender.id, "recipient": recipient.id, "text": "Hello", "language": "fr"}
     #serializer = MessageSerializer(data=data)
     serializer = MessageSerializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     msg = serializer.save()
     return Response({"message": msg.translated_text()})

class InboxView(APIView):
 def get(self, request):
     #user = User.objects.first()
     #msgs = Message.objects.filter(recipient=user)
     #msgs = Message.objects.all()
     #return Response([m.translated_text() for m in msgs])
     user_id = request.query_params.get('user_id')
     if not user_id:
        return Response({"error": "user_id query parameter is required"}, status=400)
     try:
        user = User.objects.get(id=user_id)
     except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

     msgs = Message.objects.filter(recipient=user)
     return Response([m.translated_text() for m in msgs])
