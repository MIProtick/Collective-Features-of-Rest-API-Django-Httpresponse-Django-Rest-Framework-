from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.core.serializers import serialize

from .models import Updates
from app.mixins import JsonResponseMixin

# Create your views here.

def updates_details_view(request):
    data = {
        'count': 1,
        'name': 'protick'
    }
    return JsonResponse(data)


class UpdatesCBV(JsonResponseMixin, View):
    def get(self, response, *args, **kwargs):
        data = {
            'count': 1,
            'name': 'protick'
        }
        return self.render_to_json(data)
        

class SerizedDetailsView(View):
    def get(self, response, *args, **kwargs):
        obj = Updates.objects.get(id=1)
        data = obj.serialize()
        return HttpResponse(data, content_type='application/json')
        
class SerizedListView(View):
    def get(self, response, *args, **kwargs):
        obj = Updates.objects.all()
        data = Updates.objects.all().serialize()
        # data = serialize('json', obj)
        # print(data)
        # data = {
        #     'count': 1,
        #     'name': obj.content
        # }
        return HttpResponse(data, content_type='application/json')