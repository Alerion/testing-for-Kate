from app.main.models import TestPass

class LazyTest(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_test'):
            if request.user.is_authenticated():
                try:
                    request._cached_test = TestPass.objects.get(user=request.user, complite=False)
                except TestPass.DoesNotExist:
                    request._cached_test = None
            else:
                request._cached_test = None            
        return request._cached_test

class CurrentTestMiddleware(object):
    def process_request(self, request):
        request.__class__.current_test = LazyTest()

            