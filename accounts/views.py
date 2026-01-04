from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password
from .models import User
import json

@csrf_exempt
@require_http_methods(['POST'])
def users_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    user = User.objects.create(
        name=data['name'],
        email=data['email'],
        passhash=make_password(data['password'])
    )

    return JsonResponse({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'passhash': user.passhash
    }, status=201)


@require_http_methods(['GET'])
def user_details(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at
    })