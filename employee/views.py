from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

import employee
from .models import *
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

from django.core import serializers

import bcrypt
import base64, hashlib


@csrf_exempt
def add_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        
        emp = Employee()

        emp.fname = json_data.get('fname')
        emp.lname = json_data.get('lname')
        emp.email = json_data.get('email')
        emp.department = json_data.get('department')
        emp.contact = json_data.get('contact')
        emp.position = json_data.get('position')
        emp.pin = json_data.get('pin')
        
        username = json_data['username']
        

        try:
            Employee.objects.get(username = username)
            return JsonResponse({'Error':'Username already taken'})
        except:
            emp.username = json_data['username']
            emp.password = hash_pw(json_data['password'].encode('utf-8')).decode('utf-8')
            emp.save()
            return JsonResponse({'username':username,
            'status':'OK'})

@csrf_exempt
def details_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        username = json_data.get('username')
        password = json_data.get('password')

        curr_password = Employee.objects.get(username=username).password
        if check_password(password.encode('utf-8'), curr_password.encode('utf-8')):
            employee = Employee.objects.filter(username=username)
            emp_json = json.loads(serializers.serialize('json',employee))[0]['fields']
            return JsonResponse({'details':emp_json})
        else:
            return JsonResponse({'Error':'Password incorrect'})

@csrf_exempt
def reports_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        username = json_data.get('username')
        password = json_data.get('password')

        curr_password = Employee.objects.get(username=username).password
        if check_password(password.encode('utf-8'), curr_password.encode('utf-8')):
            reports = DailyLog.objects.filter(employee__username = username)
            reports_ = serializers.serialize('json',reports)
            reports_ = json.loads(reports_)
            reports_fields = [d['fields'] for d in reports_]
            return JsonResponse({'reports':reports_fields})
        else:
            return JsonResponse({'Error':'Password incorrect'})

@csrf_exempt
def delete_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        username = json_data.get('username')
        password = json_data.get('password')
        user_to_delete = json_data.get('user_to_del')

        if Employee.objects.get(username=username).position not in ['Admin','admin']:
            return JsonResponse({'Error':'Must be admin'})

        curr_password = Employee.objects.get(username=username).password

        if check_password(password.encode('utf-8'), curr_password.encode('utf-8')):
            employee = Employee.objects.get(username=user_to_delete)
            employee.delete()
            return JsonResponse({'Status':'OK', 'Action':'Delete', 'Username':user_to_delete})
        else:
            return JsonResponse({'Error':'Password incorrect'})


@csrf_exempt
def login_employee(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        username = json_data.get('username')
        password = json_data.get('password')

        curr_password = Employee.objects.get(username=username).password
        if check_password(password.encode('utf-8'), curr_password.encode('utf-8')):
            try:
                now = timezone.now()

                last_obj = DailyLog.objects.filter(employee__username=username).latest('time')
                last_action = last_obj.check_type
                last_action_time = last_obj.time

                if last_action_time.date() != now.date():
                    last_action = 'checkout'

            except:
                last_action = None
                last_action_time = None


            if last_action in [None,'checkout']:
                curr_action = 'checkin'

            else:
                curr_action = 'checkout'

            attendance = DailyLog()
            attendance.employee = Employee.objects.get(username=username)
            attendance.time = now
            attendance.message = json_data.get('message')
            attendance.check_type = curr_action
            attendance.save()

            return JsonResponse({'Status':'OK','Action':curr_action,'curr_action_time': now,'last_action_time':last_action_time, })

        else:
            return JsonResponse({'Error':'Password incorrect'})



def hash_pw(password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)