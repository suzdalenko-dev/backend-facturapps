from django.shortcuts import render
from django.http import JsonResponse



def try_login(request):
    data = {
        'message': 'Login',
        'status': 'success'
    }
    return JsonResponse(data)