############################################################

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

############################################################


@csrf_exempt
def hello(request):

    return HttpResponse(content="Hello. I'm here for you.")
