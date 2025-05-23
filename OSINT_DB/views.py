import json

from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

import OSINT_DB.models
from Utils.Code import *


# ----------------------------- Events CRUD -----------------------------
# 获取所有Events
@api_view(['GET'])
def get_all_events(request):
    ret_data = {
        "events": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        events = OSINT_DB.models.Events.objects.all()
        ret_data["events"] = [{"id": e.id, "name": e.name, "date": e.date.strftime('%Y-%m-%d'), "score": e.score} for e
                              in events]
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 添加新Event
@api_view(['POST'])
@permission_classes([IsAdminUser])
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
@api_view(['POST'])
@permission_classes([IsAdminUser])
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
@api_view(['GET'])
@permission_classes([IsAdminUser])
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


# ——————————查询事件
# TODO 事件分析，包括事件的关键词、事件的参与者、事件的时间、事件的地点、事件的影响力等，等待前端对接
@api_view(['GET'])
@permission_classes([IsAdminUser])
def check_event(request):
    # 默认返回内容
    ret_data = {
        'code': SUCCESS_CODE,
        'msg': 'Event checked successfully!',
        'result': [],
    }
    # 判断入参是否为空
    if request.args is None:
        ret_data['ode'] = '504'
        ret_data['msg'] = '请求参数为空'
        return HttpResponse(json.dumps(ret_data), content_type="application/json")
    data = json.loads(request.body.decode('utf-8'))
    dbname = data.get('dbname')
    tbname = data.get('tbname')
    condition = data.get('condition')
    value = data.get('value')
    result = sql_result(dbname, tbname, condition, value)
    ret_data['result'] = [{"dbname": e.dbname, "tbname": e.tbname, "date": e.condition, "value": e.value} for e in result]
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


def sql_result(dbname, tbname, condition, value):
    # ：dbname（数据库名）、tbname（表名）、condition（查询条件）和value（查询值）
    conn = OSINT_DB.models.Events.objects.connect(dbname)
    try:
        print("数据库连接成功")
        cursor = conn.cursor()
        sql = 'SELECT * FROM {} where {}=?'.format(tbname, condition)
        cursor.execute(sql, (value,))

        results = cursor.fetchall()
        for data in results:
            print(data)
    except:
        print("查询失败")
    finally:
        conn.close()
    return results


# ----------------------------- Objects CRUD -----------------------------
# 获取所有Objects
@api_view(['GET'])
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
@api_view(['POST'])
@permission_classes([IsAdminUser])
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
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_object(request, object_id):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Object updated successfully!"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        obj = OSINT_DB.models.Objects.objects.get(id=object_id)
        obj.name = data.get('name', obj.name)
        obj.role = data.get('role', obj.role)
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
@api_view(['GET'])
@permission_classes([IsAdminUser])
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

# 通过name模糊搜索对象
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_object_by_keyword(request):
    ret_data = {
        "objects": [],
        "code": SUCCESS_CODE,
        "msg": ""
    }
    try:
        name = request.query_params.get('keyword')
        objects = OSINT_DB.models.Objects.objects.filter(name__contains=name)
        ret_data["objects"] = [{"id": e.id, "name": e.name, "role": e.role, "gender": e.gender} for e in objects]

    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# ----------------------------- Keywords CRUD -----------------------------
# 获取所有Keywords
@api_view(['GET'])
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
@api_view(['POST'])
@permission_classes([IsAdminUser])
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
@api_view(['POST'])
@permission_classes([IsAdminUser])
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
@api_view(['GET'])
@permission_classes([IsAdminUser])
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
