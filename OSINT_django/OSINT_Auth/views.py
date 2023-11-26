from django.http import HttpResponse
from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def login(req):
    data = req.body.decode('utf-8')
    data_js = json.loads(data)
    username = data_js['username']
    password = data_js['password']
    msg = "Login successfully"
    code = "200"
    token = "111111"
    return_msg = {
        "msg" : msg,
        "code" : code,
        "token" : token
    }
    return HttpResponse(json.dumps(return_msg), content_type='application/json')
