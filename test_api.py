#!/usr/bin/env python
"""
Simple script to test the messaging API by creating test data
Run this: python manage.py shell < test_api.py
Or: python test_api.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from messaging.models import Message

# Create test users if they don't exist
user1, created1 = User.objects.get_or_create(username='alice', defaults={'email': 'alice@example.com'})
user2, created2 = User.objects.get_or_create(username='bob', defaults={'email': 'bob@example.com'})

if created1:
    print(f"✓ Created user: alice")
if created2:
    print(f"✓ Created user: bob")

print("\n" + "=" * 60)
print("MESSAGING API TEST DATA")
print("=" * 60)

# Create test messages
messages_data = [
    {'sender': user1, 'recipient': user2, 'text': 'Hello Bob!', 'language': 'en'},
    {'sender': user1, 'recipient': user2, 'text': 'Hola Bob', 'language': 'es'},
    {'sender': user1, 'recipient': user2, 'text': 'Bonjour Bob', 'language': 'fr'},
    {'sender': user2, 'recipient': user1, 'text': 'Hi Alice!', 'language': 'en'},
]

for data in messages_data:
    msg = Message.objects.create(**data)
    print(f"\n✓ Message created:")
    print(f"  From: {msg.sender.username}")
    print(f"  To: {msg.recipient.username}")
    print(f"  Text: {msg.text}")
    print(f"  Language: {msg.language}")
    print(f"  Translated: {msg.translated_text()}")

print("\n" + "=" * 60)
print("✅ Test data created successfully!")
print("=" * 60)
print("\nNow you can test the API:")
print("1. API Endpoints (with trailing slash):")
print("   - POST /api/messages/        (create message)")
print("   - GET /api/messages/inbox/   (view inbox)")
print("\n2. To test with authentication:")
print("   - Use Django REST Framework's browsable API")
print("   - Login with Django admin credentials")
print("   - Or use 'curl' with authentication headers")
print("=" * 60)
