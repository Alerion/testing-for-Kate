# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.utils.functional import Promise

def render_to(template, processor=None):
    #if processor and not callable(processor):
    #    raise Exception('Processor is not callable.')
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request, processors=processor))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request, processors=processor))
            return output
        return wrapper
    return renderer

def ajax_processor(func):
    def wrapper(request, *args, **kwargs):
        result = func(request, *args, **kwargs)
        json = simplejson.dumps(result, cls=DjangoJSONEncoder)
        return HttpResponse(json, mimetype="application/json")
    return wrapper

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return super(LazyEncoder, self).default(obj)

class JSONResponse(HttpResponse):
    def __init__(self, pyobj, **kwargs):
        super(JSONResponse, self).__init__(
            simplejson.dumps(pyobj, cls=LazyEncoder),
            content_type='application/json; charset=%s' %
                            settings.DEFAULT_CHARSET,
            **kwargs)