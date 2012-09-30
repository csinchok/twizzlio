import simplejson
from django.http import HttpResponse

def json_response(json):
    json = simplejson.dumps(json)
    response = HttpResponse(json)
    response['Content-Type'] = 'application/json'
    return response