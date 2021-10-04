import json
from django.conf import settings
from django.db import models
from django.core.serializers import serialize
# Create your models here.

def upload_update_image(instance, filename):
    return f"updates/{instance.user}/{filename}"


class UpdatesQuerySet(models.QuerySet):
    def serialize(self):
        qs = self
        data = []
        for obj in qs:
            dictobj = json.loads(obj.serialize())
            data.append(dictobj)
        # sr_data = serialize('json', qs, fields=('user', 'content', 'image'))
        # data = json.loads(sr_data)
        
        return json.dumps(data)


class UpdatesManager(models.Manager):
    def get_queryset(self):
        return UpdatesQuerySet(self.model, using=self._db)


class Updates(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to=upload_update_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = UpdatesManager()

    def __str__(self):
        return self.content or ""
        
    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ''
        
        sr_data = serialize('json', [self], fields=('id', 'user', 'content', 'image'))
        data = json.loads(sr_data)
        data[0]['fields']['image'] = image
        data[0]['fields']['id'] = self.id
        return json.dumps(data[0]['fields'])
