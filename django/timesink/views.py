from django.views.generic.base import View
from django.db.models import get_models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import json
from models import DeletionRecord

def get_model_class(name):
  model_cls = [m for m in get_models() if m.__name__ == meta["className"]]
  if model_cls:
    return model_cls[0]
  else:
    return None
    
def get_instance(cls_name, id):
  model_cls = get_model_class(cls_name)
  if model_cls:
    try:
      return model_cls.objects.get(id)
    except ObjectDoesNotExist:
      return None
  else:
    return None

def get_model_changes_list(model_cls, start):
  return []

def get_changes_list(start):
  changes = []
  for model_cls in get_models():
    changes.extend(get_model_changes_list(model_cls, start))
  return changes

def apply_instance_changes(instance, properties, timestamp):
  for key, value in properties.items():
    if getattr(instance.eav, key + "_timestamp") < timestamp:
      setattr(instance, key, value)
      setattr(instance.eav, key + "_timestamp", timestamp)

def apply_changes(client_changes):
  for change in client_changes:
    id = change["object"]
    className = change["className"]
    action = change["action"]
    timestamp = change["timestamp"]
    instance = get_instance(className, id)
    
    if action == "create":
      if not instance:
        get_model_class(className).objects.create(**change["properties"])
      else:
        apply_instance_changes(instance, change["properties"], timestamp)

    elif action == "delete":
      if instance:
        DeletionRecord.objects.create(object_id=instance.id, timestamp=change["timestamp"])
        instance.delete()
    
    elif action == "update":
      apply_instance_changes(instance, changes["properties"], timestamp)

    else:
      # Unsupported action
      pass

def create_deletion(id, class_name, timestamp):
  return {
    "object": id,
    "className": class_name,
    "action": "delete",
    "timestamp": timestamp
  }
  
def create_modification(id, class_name, key, value, timestamp):
  return {
    "object": id,
    "className": class_name,
    "action": "update",
    "timestamp": timestamp,
    "properties": {
      key: value
    }
  }
  
def create_creation(id, class_name, properties, timestamp):
  return {
    "object": id,
    "className" : class_name,
    "action": "create",
    "timestamp": timestamp,
    "properties": properties
  }
  
def get_properties(json_obj, instance):
  server_changes = {}
  client_changes = {}
  for key, p in json_obj.items():
    if not key.startswith("_"):
      ts = p["timestamp"]
      if not instance or getattr(instance.eav, key + "_timestamp") < ts:
        server_changes[key] = p
      elif instance and getattr(instance.eav, key + "_timestamp") > ts:
        client_changes[key] = dict(
          value = getattr(instance, key),
          timestamp = getattr(instance.eav, key + "_timestamp")
        )
  return server_changes, client_changes


class FullDataSetView(View):  
  def post(self, request, *args, **kwargs):
    data = json.loads(request.POST)
    server_changes = []
    client_changes = []

    for obj in data:
      meta = obj["_meta"]
      if not "className" in meta or not meta["className"]:
        return HttpResponse("Error: Meta tag missing \"className\"")
      if not "id" in meta or not meta["id"]:
        return HttpResponse("Error: Meta tag missing \"id\"")
      
      model_cls = get_model_class(meta["className"])
      if not model_cls:
        return HttpResponse("Error: No such class %s" % meta["className"])
      
      if not meta["id"]:
        return HttpResponse("Error: No id specified")
      
      id = meta["id"]
      cls_name = model_cls.__name__

      try:
        instance = model_cls.objects.get(id)
        if "deletedAt" in meta and meta["deletedAt"] and meta["deletedAt"] > instance._modifiedAt:
          server_changes.append(create_deletion(id), meta["deletedAt"])
        else:
          s, c = get_properties(obj, instance)
          for key, p in s:
            server_changes.append(create_modification(id, cls_name, key, p["value"], p["timestamp"]))
          for key, p in c:
            client_changes.append(create_modification(id, cls_name, key, p["value"], p["timestamp"]))

      except ObjectDoesNotExist:
        try:
          deletion = DeletionRecord.objects.get(object_id=id)
          client_changes.append(create_deletion(id, cls_name), deletion.timestamp)
        except DeletionRecord.DoesNotExist:
          server_changes.append(create_creation(id, cls_name, get_properties(obj), meta["createdAt"]))
        
    apply_changes(server_changes)
    return HttpResponse(json.dumps(client_changes))
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(FullDataSetView, self).dispatch(*args, **kwargs) 

class ChangeLogView(View):
  
  def post(self, request, *args, **kwargs):
    data = json.loads(request.POST)
    apply_changes(data["changes"])
    ret = get_changes_list(data["lastSync"])
    return HttpResponse(json.dumps(ret))
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(ChangeLogView, self).dispatch(*args, **kwargs) 

