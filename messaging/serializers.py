from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
 translated_text = serializers.CharField(source='translated_text', read_only=True)
 
 class Meta:
     model = Message
     fields = "__all__"

 def create(self, validated_data):
     return Message.objects.create(
         #sender=validated_data['recipient'],
         sender=validated_data['sender'],
         #recipient=validated_data['sender'],
         recipient=validated_data['recipient'],
         text=validated_data['text'],
         #language=validated_data['language']
         language=validated_data.get('language', 'en')
     )
