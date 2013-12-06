import functools
import datetime

from django.http import HttpResponse
from django.utils import simplejson


JSON_DATE_FORMAT = "%m/%d/%Y"
JSON_DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

def _handler(obj):
    """
    Default JSON handler.
    """

    if isinstance(obj, datetime.datetime):
        return obj.strftime(JSON_DATETIME_FORMAT)

    if isinstance(obj, datetime.date):
        return obj.strftime(JSON_DATE_FORMAT)

    return obj


class JsonResponse(HttpResponse):

    def __init__(self, content='', content_type='application/x-json', *args, **kwargs):
        handler = kwargs.pop('handler', _handler)
        content = simplejson.dumps(content, default=handler)
        super(JsonResponse, self).__init__(content, content_type=content_type, *args, **kwargs)


def render_to_json(func):
    """
    View decorator which does the same as render_json. Example:

    @render_to_json
    def my_view(request):
        return {'hello' : 'world'}

    """

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):

        response = func(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        return JsonResponse(response)

    return wrapper
