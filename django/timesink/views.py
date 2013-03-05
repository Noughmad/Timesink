from django.views.generic.base import View
from django.db import models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import json

class FullDataSetView(View):
  def get_properties(json_obj, instance):
    values = {}
      for key, p in json_obj.items():
        if not key.startswith("_")
          ts = p["timestamp"]
          if not instance or getattr(instance.eav, key + "_timestamp") < ts:
            values[key] = p
    return values
  
  def post(self, request, *args, **kwargs):
    data = json.loads(request.POST)
    for obj in data:
      meta = obj["_meta"]
      if not "className" in meta or not meta["className"]
        return HttpResponse("Error: Meta tag missing \"className\"")
      if not "id" in meta or not meta["id"]
        return HttpResponse("Error: Meta tag missing \"id\"")
      
      model_cls = [m for m in models.get_models() if m.__name__ == meta["className"]]
      if not model_cls:
        return HttpResponse("Error: No such class %s" % meta["className"])
      model_cls = model_cls[0]
      
      if not meta["id"]:
        return HttpResponse("Error: No id specified")
      
      try:
        instance = model_cls.objects.get(meta["id"])
        if "deletedAt" in meta and meta["deletedAt"] and meta["deleteAd"] > instance._modifiedAt:
          instance.delete()
          continue
        else:
          for key, p in get_properties(obj, instance):
            setattr(instance, key, p["value"])
            setattr(instance.eav, key + "_timestamp", p["timestamp"])
      except ObjectDoesNotExist:
        instance = model_cls.objects.create(get_properties(obj))
        
      instance.save()
            
    return HttpResponse(json.dumps(data))
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(FullDataSetView, self).dispatch(*args, **kwargs) 

class ChangeLogView(View):
  
  def post(self, request, *args, **kwargs):
    data = json.loads(request.POST)
    return HttpResponse(json.dumps(data))
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(ChangeLogView, self).dispatch(*args, **kwargs) 

