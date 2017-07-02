# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
#from .models import LdapAdminUser
from .backend  import LDAPUserAuthBackend

def notifications(request):
    output = LdapAdminUser.objects.get(username = "admin" )

    notification_template = "admin/notifications/index.html" 
    template = loader.get_template(notification_template)
    context = { 
        'output': output,
        }
    return HttpResponse(template.render(context, request))

def sender_email(request):
    notification_template = "admin/notifications/index.html" 
    template = loader.get_template(notification_template)
    #context = RequestContext(request)
    if request.method == 'POST':
        senderemail = request.POST['selmail']
        #update senderemail
    else:
        output = LdapAdminUser.objects.get(request.user)
        senderemail = 'www-data@'
        context = {
            'output': output,
        }
        return HttpResponse(template.render(context, request))


