from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
 sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent')
 recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='received')
 text = models.TextField()
 language = models.CharField(max_length=5, default="en")

 def translated_text(self):
     translations = {
         "en": self.text,
         "fr": "FR_" + self.text,
         "es": "ES_" + self.text,
     }
     #return translations.get("en")
     return translations.get(self.language, self.text)
