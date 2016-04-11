from django.http import HttpResponse
from django.shortcuts import render
import datetime

def test(request):
	now = datetime.datetime.now()
	return render(request, 'states.html')
