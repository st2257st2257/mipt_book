from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index_test_get(request):
    return render(request, 'get/index.html')


@csrf_exempt
def index_test_auth(request):
    return render(request, 'authorization/index.html')


@csrf_exempt
def index_test_register(request):
    return render(request, 'registration/index.html')
