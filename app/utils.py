import json

def is_valid_json(data, *args, **kwargs):
    try:
        js_data = json.loads(data);
        return True
    except:
        return False
