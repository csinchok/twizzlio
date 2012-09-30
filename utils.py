import json
from django.http import HttpResponse

def json_response(json):
    js = json.dumps(js)
    response = HttpResponse(js)
    response['Content-Type'] = 'application/json'
    return response