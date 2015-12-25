# from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from django.template import RequestContext
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render,render_to_response, redirect

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
# RETURN_URL = 'http://django-blog-shsong97-1.c9users.io/blog/calendar/'
RETURN_URL = 'https://song-diary.herokuapp.com/blog/calendar/'

def calendar_view(request):
    home_dir = os.path.dirname(__file__)
    store_file = os.path.join(home_dir, CLIENT_SECRET_FILE)
    flow = client.flow_from_clientsecrets(
        store_file,
        scope=SCOPES,
        redirect_uri=RETURN_URL)

    if not request.GET.has_key('code'):
        auth_uri = flow.step1_get_authorize_url()
        return redirect(auth_uri)
    
    auth_code = request.GET['code']
    request.session['code'] = auth_code
    credentials = flow.step2_exchange(auth_code)

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', 
        timeMin=now, 
        maxResults=10, 
        singleEvents=True,
        orderBy='startTime'
        ).execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    
    # calendar_list=[]
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    #     calendar_list.append(event['summary'])
    
    return render_to_response('blog/calendar.html',RequestContext(request,{'calendar_list':events}))
