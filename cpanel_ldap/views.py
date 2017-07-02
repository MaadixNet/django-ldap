# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from django.views.decorators.csrf import csrf_exempt
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
# Create your views here.

def cpanelStatus(request):
    response_string="ready"
    #return HttpResponse(response_string,mimetype='text/plain')
    return HttpResponse("ready")
