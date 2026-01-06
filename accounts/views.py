from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from django.db.utils import IntegrityError
from .models import User
import json

@csrf_exempt
@require_http_methods(['POST'])
def users_view(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    try:    
        user = User.objects.create(
            name=data['name'],
            email=data['email'],
            passhash=make_password(data['password'])
        )
    except IntegrityError:
        return JsonResponse({'error': 'Username or email already exists'}, status=409)

    return JsonResponse({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'passhash': user.passhash
    }, status=201)


@csrf_exempt
@require_http_methods(['POST'])
def login_jwt(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    try:
        user = User.objects.get(name=data['name'])
    except User.DoesNotExist:
        return JsonResponse({'error': 'User with that name does not exist'}, status=401)
    except KeyError:
        return JsonResponse({'error': 'User name is not provided'}, status=400)
    
    try:
        if check_password(data['password'], user.passhash):
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email
                }
            })
        return JsonResponse({"error": "Wrong password"}, status=401)
    except KeyError:
        return JsonResponse({'error': 'Password is not provided'}, status=400)

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