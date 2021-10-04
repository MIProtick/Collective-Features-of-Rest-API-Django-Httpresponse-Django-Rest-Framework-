import json
from django.views.generic import View
from django.http import HttpResponse

from updates.models import Updates as UpdateModel
from updates.forms import UpdateModelForm
from .mixins import CSRFExemptMixin
from app.mixins import HttpResponseMixin
from app.utils import is_valid_json

class UpdateModelDetailView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True
    
    def fetchData(self, id, *args, **kwargs):
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        else: return None
    
    
    def get(self, request, id, *args, **kwargs):
        obj = self.fetchData(id)
        if obj != None:
            js_data = obj.serialize()
        else: js_data = json.dumps({'message': 'Data Not found'})
        return HttpResponse(js_data, content_type='application/json')
    
    def post(self, request, id, *args, **kwargs):
        json_data = json.dumps({'message': 'Not allowed. Use /api/update/ endpoint.'})
        return self.render_to_response(json_data, status= 204)
        
    def put(self, request, id, *args, **kwargs):
        
        obj  = self.fetchData(id=id)
        if obj == None:
            js_data = json.dumps({'message': 'Data Not found'})
            return self.render_to_response(js_data, status= 404)
        
        passed_data = json.loads(request.body)
        data = json.loads(obj.serialize())
        
        for k,v in passed_data.items():
            data[k] = v
        
        form = UpdateModelForm(data, instance=obj)
        
        if form.is_valid():
            obj = form.save(commit=True)
            return self.render_to_response(obj.serialize(), status= 202)
        if form.errors:
            return self.render_to_response(json.dumps(form.errors), status= 403)
        
        json_data = json.dumps({'message': 'Invalid data'})
        return self.render_to_response(json_data, status= 403)
        
    def delete(self, request, id, *args, **kwargs):
        obj  = self.fetchData(id=id)
        if obj == None:
            js_data = json.dumps({'message': 'Data Not found'})
            return self.render_to_response(js_data, status= 404)
            
        is_deleted = obj.delete()
        if is_deleted:
            js_data = json.dumps({'message': 'Successfully deleted'})
            return self.render_to_response(js_data, status= 202)
        else: 
            js_data = json.dumps({'message': 'Data deletion failed'})
            return self.render_to_response(js_data, status= 202)
    
    
#  `api/update/`

class UpdateModelListView(HttpResponseMixin, CSRFExemptMixin, View):
    is_json = True
    queryset = None
    
    def fetchQuerySet(self):
        qs = UpdateModel.objects.all()
        self.queryset = qs
        return qs
    
    def fetchData(self, id, *args, **kwargs):
        qs = self.fetchQuerySet().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        else: return None
    
    def get(self, request, *args, **kwargs):
        if not is_valid_json(request.body):
            return self.render_to_response(json.dumps({'message': 'Invalid json data.'}), status= 400)
        
        oid = json.loads(request.body).get('id', None)
        if oid:
            obj = self.fetchData(oid)
            if obj is None:
                return self.render_to_response(json.dumps({'message': 'No data found with this id.'}), status= 404)
            js_data = obj.serialize()
            return self.render_to_response(js_data, status= 200)
        
        qs = self.fetchQuerySet()
        json_data = qs.serialize()
        return self.render_to_response(json_data)
        
    def post(self, request, *args, **kwargs):
        if not is_valid_json(request.body):
            return self.render_to_response(json.dumps({'message': 'Invalid json data.'}), status= 400)
        
        served_data = json.loads(request.body)
        if served_data.get('id'):
            return self.render_to_response(json.dumps({'message': 'Invalid json data with id. \'id\' attribute is not allowed.'}), status= 400)
        
        form = UpdateModelForm(served_data)
        if form.is_valid():
            obj = form.save(commit=True)
            js_obj = obj.serialize()
            return self.render_to_response(js_obj, status= 200)
        if form.errors:
            return self.render_to_response(json.dumps(form.errors), status= 400)
        
        json_data = json.dumps({'message': 'Not Allowed'})
        return self.render_to_response(json_data, status= 204)
    
    def put(self, request, *args, **kwargs):
        if not is_valid_json(request.body):
            return self.render_to_response(json.dumps({'message': 'Invalid json data.'}), status= 400)
        
        passed_data = json.loads(request.body)
        if passed_data.get('id'):
            return self.render_to_response(json.dumps({'message': 'Attribute \'id\' is required.'}), status= 400)
        
        oid= passed_data.get('id', None)
        obj  = self.fetchData(id=oid)
        if obj == None:
            js_data = json.dumps({'message': 'Object Not found'})
            return self.render_to_response(js_data, status= 404)
        
        data = json.loads(obj.serialize())
        
        for k,v in passed_data.items():
            data[k] = v
        
        form = UpdateModelForm(data, instance=obj)
        
        if form.is_valid():
            obj = form.save(commit=True)
            return self.render_to_response(obj.serialize(), status= 202)
        if form.errors:
            return self.render_to_response(json.dumps(form.errors), status= 403)
        
        json_data = json.dumps({'message': 'Invalid data'})
        return self.render_to_response(json_data, status= 403)
        
    def delete(self, request, *args, **kwargs):
        if not is_valid_json(request.body):
            return self.render_to_response(json.dumps({'message': 'Invalid json data.'}), status= 400)
        
        passed_data = json.loads(request.body)
        oid= passed_data.get('id', None)
        obj  = self.fetchData(id=oid)
        if obj == None:
            js_data = json.dumps({'message': 'Data Not found'})
            return self.render_to_response(js_data, status= 404)
            
        is_deleted = obj.delete()
        if is_deleted:
            js_data = json.dumps({'message': 'Successfully deleted'})
            return self.render_to_response(js_data, status= 202)
        else: 
            js_data = json.dumps({'message': 'Data deletion failed'})
            return self.render_to_response(js_data, status= 405)
        