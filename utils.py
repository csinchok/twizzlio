import json
from django.http import HttpResponse

def json_response(js):
    js = json.dumps(js)
    response = HttpResponse(js)
    response['Content-Type'] = 'application/json'
    return response