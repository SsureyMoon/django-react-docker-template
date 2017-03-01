from functools import wraps
from django.http import Http404

def allowed_resources(resources_list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resource_name = kwargs['resource_name']
            if resource_name in resources_list:
                return func(*args, **kwargs)
            raise Http404("resource name({}) is not allowed".format(resource_name))
        return wrapper

    return decorator
