from django.db import models

class DeletionRecord(models.Model):
  object_id = CharField(max_length=40)
  timestamp = DateField(auto_now_add=True)
  