from django.db import models
from django.db.models.base import Model
from django.conf import settings


def upload_status_image(instance, filename):
    return f"status/{instance.user}/{filename}"
    

class StatusQuerySet(models.QuerySet):
    pass


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)

    
# Create your models here.
class Status(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_status_image, blank=True, null=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = StatusManager()

    class Meta:
        verbose_name = "status"
        verbose_name_plural = "statuses"

    def __str__(self):
        return str(self.content)[:50]
