# -.- coding: UTF-8 -.-
from django.http import HttpResponse
def home(request):
    html_text="<html><head><title>Django Site Home</title></head>\
    <body><ul><li><a href='/blog'>블로그</a>\
    <li><a href='/polls'>투표</a>\
    </ul></body></html>"
    return HttpResponse(html_text)