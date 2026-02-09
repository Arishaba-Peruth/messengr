import pytest
from django.contrib.auth.models import User
from .models import Message

@pytest.mark.django_db
def test_translation():
 u1=User.objects.create(username='a')
 u2=User.objects.create(username='b')
 msg=Message.objects.create(sender=u1,recipient=u2,text='Hello',language='fr')
 assert msg.translated_text()=="FR_Hello"

@pytest.mark.django_db
def test_sender_recipient():
 u1=User.objects.create(username='a')
 u2=User.objects.create(username='b')
 msg=Message.objects.create(sender=u1,recipient=u2,text='Hi',language='en')
 assert msg.sender==u1
