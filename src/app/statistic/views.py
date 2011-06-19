from django.http import HttpResponse
from lib import render_to
from app.main.models import Test, TestPass
from app.account.models import UserGroup
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.utils.simplejson import dumps

@render_to('statistic/index.html')
def index(request):
    return {}

@render_to('statistic/discipline_main.html')
def discipline_main(request):
    return {
        'items': Test.objects.all()
    }

@render_to('statistic/discipline.html')
def discipline(request, pk):
    obj = get_object_or_404(Test, pk=pk)
    results = TestPass.objects.filter(test=obj, complite=True)
    data = {}
    for i in range(2, 6):
        data[i] = 1
    for item in results:
        data[item.grade] += 1
    s = sum(data.values())
    percent_data = {}
    for key, value in data.items():
        percent_data[key] = round(value / 1. / s * 100)
    output = [[str(key), value] for key, value in data.items()]
    percent_output = [[str(key), value] for key, value in percent_data.items()]
    return {
        'obj': obj,
        'data': dumps(output),
        'perc_data': dumps(percent_output),
        'count': TestPass.objects.filter(test=obj, complite=True).count()
    }
    
@render_to('statistic/pass_discipline.html')
def pass_discipline(request):
    results = TestPass.objects.filter(complite=True)
    data = {}
    tests = Test.objects.all()
    for item in tests:
        data[item.name] = 1  
    for item in results:
        data[item.test.name] += 1
    output = [[unicode(key), value] for key, value in data.items()]
    return {
        'data': dumps(output)
    }
    
@render_to('statistic/group_main.html')
def group_main(request):
    return {
        'items': UserGroup.objects.all()
    }