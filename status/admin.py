from django.contrib import admin

from .forms import StatusForm
from .models import Status

# Register your models here.

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', '__str__',]
    form = StatusForm
    # class Meta:
    #     model = Status

# admin.site.register(Status, StatusAdmin)