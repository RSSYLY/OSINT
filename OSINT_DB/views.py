from django.shortcuts import render, HttpResponse
import OSINT_DB.models
from Utils.Code import *
import json


# ----------------------------- Events CRUD -----------------------------
# 获取所有Events
def get_all_objects(request):
    ret_data = {
        "objects": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        objects = OSINT_DB.models.Objects.objects.all()
        ret_data["objects"] = [{"id": e.id, "name": e.name, "role": e.role, "gender": e.gender} for e in objects]
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")
    # Similar to get_all_events, retrieve all Objects entries and return them.

def get_all_events(request):
    ret_data = {
        "events": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        events = OSINT_DB.models.Events.objects.all()
        ret_data["events"] = [{"id": e.id, "name": e.name, "date": e.date.strftime('%Y-%m-%d'), "score": e.score} for e in events]
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 添加新Event
def add_event(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Event added successfully!"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        date = data.get('date')  # YYYY-MM-DD  Format
        score = data.get('score')
        event = OSINT_DB.models.Events(name=name, date=date, score=score)
        event.save()
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 更新Event
def update_event(request, event_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Event updated successfully!"
    }
    try:
        event = OSINT_DB.models.Events.objects.get(id=event_id)
        data = json.loads(request.body.decode('utf-8'))
        event.name = data.get('name', event.name)
        event.date = data.get('date', event.date)
        event.score = data.get('score', event.score)
        event.save()
    except OSINT_DB.models.Events.DoesNotExist:
        ret_data["code"] = ITEM_NOT_FOUND_CODE
        ret_data["msg"] = "Event not found!"
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 删除Event
def delete_event(request, event_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Event deleted successfully!"
    }
    try:
        event = OSINT_DB.models.Events.objects.get(id=event_id)
        event.delete()
    except OSINT_DB.models.Events.DoesNotExist:
        ret_data["code"] = ITEM_NOT_FOUND_CODE
        ret_data["msg"] = "Event not found!"
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# ----------------------------- Objects CRUD -----------------------------
# 获取所有Objects
def get_all_objects(request):
    ret_data = {
        "objects": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        objects = OSINT_DB.models.Objects.objects.all()
        ret_data["objects"] = [{"id": e.id, "name": e.name, "role": e.role, "gender": e.gender} for e in objects]
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")
    # Similar to get_all_events, retrieve all Objects entries and return them.


# 添加新Object
def add_object(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Object added successfully!"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        role = data.get('role')
        gender = data.get('gender')
        new_object = OSINT_DB.models.Objects(name=name, role=role, gender=gender)
        new_object.save()
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 更新Object
def update_object(request, object_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Object updated successfully!"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        obj = OSINT_DB.models.Objects.objects.get(id=object_id)
        obj.name = data.get('name', obj.name)
        obj.role = data .get('role', obj.role)
        obj.gender = data.get('gender', obj.gender)
        obj.save()
    except OSINT_DB.models.Objects.DoesNotExist:
        ret_data["code"] = ITEM_NOT_FOUND_CODE
        ret_data["msg"] = "Object not found!"
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 删除Object
def delete_object(request, object_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Object deleted successfully!"
    }
    try:
        obj = OSINT_DB.models.Objects.objects.get(id=object_id)
        obj.delete()
    except OSINT_DB.models.Objects.DoesNotExist:
        ret_data["code"] = ITEM_NOT_FOUND_CODE
        ret_data["msg"] = "Object not found!"
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# ----------------------------- Keywords CRUD -----------------------------
# 获取所有Keywords
def get_all_keywords(request):
    ret_data = {
        "keywords": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        keywords = OSINT_DB.models.Keywords.objects.all()
        ret_data["keywords"] = [{"id": k.id, "keyword": k.keyword, "date": k.date} for k in keywords]
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 添加新Keyword
def add_keyword(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Keyword added successfully!"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        keyword = data.get('keyword')
        new_keyword = OSINT_DB.models.Keywords(keyword=keyword)
        new_keyword.save()
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 更新Keyword
def update_keyword(request, keyword_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Keyword updated successfully!"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        keyword = OSINT_DB.models.Keywords.objects.get(id=keyword_id)
        keyword.keyword = data.get('keyword', keyword.keyword)
        keyword.save()
    except OSINT_DB.models.Keywords.DoesNotExist:
        ret_data["code"] = ITEM_NOT_FOUND_CODE
        ret_data["msg"] = "Keyword not found!"
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 删除Keyword
def delete_keyword(request, keyword_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "keyword deleted successfully!"
    }
    try:
        obj = OSINT_DB.models.Keywords.objects.get(id=keyword_id)
        obj.delete()
    except OSINT_DB.models.Keywords.DoesNotExist:
        ret_data["code"] = ITEM_NOT_FOUND_CODE
        ret_data["msg"] = "Object not found!"
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")
    # Similar to delete_event, retrieve the keyword by 'keyword_id' and delete it.
