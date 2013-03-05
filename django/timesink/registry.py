from django.db import models

from eav.registry import EavConfig, Registry
from eav import Attribute

class TimesinkEavConfig(EavConfig):
  
  @classmethod
  def get_attributes(cls):
    names = [n + "_timestamp" for n in cls._meta.fields if !n.startswith("_")]
    return Attribute.on_site.filter(name__in=names)
  
def register(model_cls):
  Registry.register(model_cls, TimesinkEavConfig)
  for n in model_cls._meta.fields:
    if !n.startswith("_"):
      Attribute.objects.get_or_create(name=n+"_timestamp", datatype=Attribute.TYPE_DATE)
  model_cls.add_to_class("_createdAt", models.DateTimeField(auto_now_add=True))
  model_cls.add_to_class("_modifiedAt", models.DateTimeField(auto_now=True))
  model_cls.add_to_class("_deletedAt", models.DateTimeField(editable=False, blank=True))
  return model_cls
