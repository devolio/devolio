from django.conf import settings


def offline_dev(request):
    return {'OFFLINE_DEV': settings.OFFLINE_DEV}