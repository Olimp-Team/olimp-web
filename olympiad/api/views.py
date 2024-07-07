from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Аутентификация успешна
            return JsonResponse({'status': 'success'})
        else:
            # Аутентификация не удалась
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
