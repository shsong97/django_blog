# -.- coding: UTF-8 -.-
from django.http import HttpResponseRedirect

def home(request):
    return HttpResponseRedirect('/blog/')