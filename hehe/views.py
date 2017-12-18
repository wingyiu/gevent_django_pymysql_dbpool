# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from .models import Question
import time

# Create your views here.
def index(request):
    qs = Question(question_text='a', )
    qs.save()
    time.sleep(0.02)
    return HttpResponse("You're looking at question ")