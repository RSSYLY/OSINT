from django.shortcuts import render, HttpResponse
import OSINT_DB.models
from Utils.Code import *
import json


# Create your views here.
def get_all_objects(req):
    ret_data = {
        "objects": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        Objects_ret = OSINT_DB.models.Objects.objects.all()
        ret_data["objects"] = [i.to_dict() for i in Objects_ret]
        print(ret_data)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = e.__str__()
        return HttpResponse(json.dumps(ret_data), content_type="application/json")


def get_all_events(req):
    ret_data = {
        "objects": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    Events_ret = OSINT_DB.models.Events.objects.all()
    ret_data["objects"] = [i.to_dict() for i in Events_ret]
    print(ret_data)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")
