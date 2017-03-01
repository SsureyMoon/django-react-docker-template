from django.conf import settings

def pass_server_environment(request):
    return {'wds_on': settings.WDS_ON}
