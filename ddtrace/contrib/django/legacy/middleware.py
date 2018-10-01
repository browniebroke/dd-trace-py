from .patch import patch
from ..conf import settings
from ..middleware import TraceMiddleware as DjangoTraceMiddleware, \
                         TraceExceptionMiddleware as DjangoTraceExceptionMiddleware


class BaseTraceMiddleware(object):
    def __init__(self, proxied_middleware):
        self.middleware = proxied_middleware
        self.enabled = settings.AUTO_INSTRUMENT
        # We use the middleware initialization as an hook to replace the 1.8+ app config
        patch()


class TraceMiddleware(BaseTraceMiddleware):
    def __init__(self):
        super(TraceMiddleware, self).__init__(DjangoTraceMiddleware())

    def process_request(self, request):
        return self.middleware.process_request(request) if self.enabled else None

    def process_view(self, request, view_func, *args, **kwargs):
        return self.middleware.process_view(request, view_func, *args, **kwargs) \
            if self.enabled \
            else None

    def process_response(self, request, response):
        return self.middleware.process_response(request, response) if self.enabled else None


class TraceExceptionMiddleware(BaseTraceMiddleware):
    """
    Middleware that traces exceptions raised
    """
    def __init__(self):
        super(TraceExceptionMiddleware, self).__init__(DjangoTraceExceptionMiddleware())

    def process_exception(self, request, exception):
        return self.middleware.process_exception(request, exception) if self.enabled else None
