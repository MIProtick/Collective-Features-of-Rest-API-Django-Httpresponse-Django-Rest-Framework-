from django.http import JsonResponse, HttpResponse

class HttpResponseMixin(object):
    is_json = False
    
    def render_to_response(self, context, status=200):
        if self.is_json:
            content_type = 'application/json'
        else:
            content_type = 'text/html'
        
        return HttpResponse(context, content_type=content_type, status=status)
    
    

class JsonResponseMixin(object):
    def render_to_json(self, context, *args, **kwargs):
        return JsonResponse(self.get_data(context), *args, **kwargs)
    
    def get_data(self, context):
        return context;