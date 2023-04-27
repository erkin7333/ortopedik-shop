from django.urls import reverse

def title(request):
    return {
        "url_name": "{}:{}".format(request.resolver_match.app_name, request.resolver_match.url_name)
    }
