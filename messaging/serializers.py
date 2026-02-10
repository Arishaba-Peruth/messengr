from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    translated_text = serializers.SerializerMethodField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'text', 'language', 'translated_text']
    
    def get_translated_text(self, obj):
        """Return the translated text based on the message's language setting."""
        return obj.translated_text()

    def create(self, validated_data):
        return Message.objects.create(
            #Custom validate() method to prevent self-messaging
            sender=validated_data['sender'],
            recipient=validated_data['recipient'],
            text=validated_data['text'],
            language=validated_data.get('language', 'en')
        )
    
    def validate(self, data):
        """Ensure recipient is not the same as sender."""
        if data.get('sender') == data.get('recipient'):
            raise serializers.ValidationError(
                {"recipient": "A user cannot send a message to themselves."}
            )
        return data
