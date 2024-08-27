from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index_test_book(request):
    return render(request, 'book/index.html')
