import pytest
from django.contrib.auth.models import User
from django.test import Client
from rest_framework.test import APIClient
from .models import Message

# ==================== Model Tests ====================

@pytest.mark.django_db
def test_translation():
    """Test that messages are correctly translated to the specified language."""
    u1 = User.objects.create(username='a')
    u2 = User.objects.create(username='b')
    msg = Message.objects.create(sender=u1, recipient=u2, text='Hello', language='fr')
    assert msg.translated_text() == "FR_Hello"

@pytest.mark.django_db
def test_sender_recipient():
    """Test that sender and recipient are correctly stored in the message."""
    u1 = User.objects.create(username='a')
    u2 = User.objects.create(username='b')
    msg = Message.objects.create(sender=u1, recipient=u2, text='Hi', language='en')
    assert msg.sender == u1
    assert msg.recipient == u2

@pytest.mark.django_db
def test_default_language():
    """Test that the default language is English."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    msg = Message.objects.create(sender=u1, recipient=u2, text='Hello')
    assert msg.language == 'en'
    assert msg.translated_text() == 'Hello'

@pytest.mark.django_db
def test_unsupported_language_fallback():
    """Test that unsupported languages fall back to the original text."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    msg = Message.objects.create(sender=u1, recipient=u2, text='Hello', language='de')
    assert msg.translated_text() == 'Hello'  # Falls back to original text

# ==================== API View Tests ====================

@pytest.mark.django_db
def test_create_message_authenticated():
    """Test that an authenticated user can create a message."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    
    client = APIClient()
    client.force_authenticate(user=u1)
    
    data = {
        'recipient': u2.id,
        'text': 'Hello recipient!',
        'language': 'en'
    }
    
    response = client.post('/api/messages/', data, format='json')
    assert response.status_code == 201
    assert response.data['sender'] == u1.id
    assert response.data['recipient'] == u2.id
    assert response.data['text'] == 'Hello recipient!'

@pytest.mark.django_db
def test_create_message_with_translation():
    """Test that created messages return the translated text in the response."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    
    client = APIClient()
    client.force_authenticate(user=u1)
    
    data = {
        'recipient': u2.id,
        'text': 'Bonjour',
        'language': 'fr'
    }
    
    response = client.post('/api/messages/', data, format='json')
    assert response.status_code == 201
    assert response.data['translated_text'] == 'FR_Bonjour'

@pytest.mark.django_db
def test_create_message_unauthenticated():
    """Test that unauthenticated users cannot create messages."""
    u2 = User.objects.create(username='recipient')
    
    client = APIClient()
    
    data = {
        'recipient': u2.id,
        'text': 'Hello',
        'language': 'en'
    }
    
    response = client.post('/api/messages/', data, format='json')
    assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
def test_create_message_to_self_validation():
    """Test that a user cannot send a message to themselves."""
    u1 = User.objects.create(username='sender')
    
    client = APIClient()
    client.force_authenticate(user=u1)
    
    data = {
        'sender': u1.id,
        'recipient': u1.id,
        'text': 'Talking to myself',
        'language': 'en'
    }
    
    response = client.post('/api/messages/', data, format='json')
    assert response.status_code == 400
    assert 'recipient' in response.data

@pytest.mark.django_db
def test_create_message_invalid_recipient():
    """Test that creating a message with invalid recipient returns error."""
    u1 = User.objects.create(username='sender')
    
    client = APIClient()
    client.force_authenticate(user=u1)
    
    data = {
        'recipient': 9999,  # Non-existent user
        'text': 'Hello',
        'language': 'en'
    }
    
    response = client.post('/api/messages/', data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_inbox_authenticated():
    """Test that an authenticated user can view their inbox."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    u3 = User.objects.create(username='other')
    
    # Create messages
    msg1 = Message.objects.create(sender=u1, recipient=u2, text='Hello', language='en')
    msg2 = Message.objects.create(sender=u3, recipient=u2, text='Hi', language='en')
    msg3 = Message.objects.create(sender=u2, recipient=u1, text='Reply', language='en')
    
    client = APIClient()
    client.force_authenticate(user=u2)
    
    response = client.get('/api/messages/inbox/', format='json')
    assert response.status_code == 200
    assert len(response.data) == 2  # u2 should only see messages sent to them
    
    # Verify the messages are for u2
    recipient_ids = [msg['recipient'] for msg in response.data]
    assert all(rid == u2.id for rid in recipient_ids)

@pytest.mark.django_db
def test_inbox_unauthenticated():
    """Test that unauthenticated users cannot view inbox."""
    client = APIClient()
    
    response = client.get('/api/messages/inbox/', format='json')
    assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
def test_inbox_empty():
    """Test that an empty inbox returns an empty list."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    
    # Create a message sent by u2 (not to u2)
    Message.objects.create(sender=u2, recipient=u1, text='Hello', language='en')
    
    client = APIClient()
    client.force_authenticate(user=u2)
    
    response = client.get('/api/messages/inbox/', format='json')
    assert response.status_code == 200
    assert len(response.data) == 0

@pytest.mark.django_db
def test_inbox_with_translations():
    """Test that inbox returns messages with proper translations."""
    u1 = User.objects.create(username='sender')
    u2 = User.objects.create(username='recipient')
    
    msg = Message.objects.create(sender=u1, recipient=u2, text='Bonjour', language='fr')
    
    client = APIClient()
    client.force_authenticate(user=u2)
    
    response = client.get('/api/messages/inbox/', format='json')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['translated_text'] == 'FR_Bonjour'
    assert response.data[0]['language'] == 'fr'
