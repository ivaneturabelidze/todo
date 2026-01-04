from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Task
import json

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def tasks_view(request):
    if request.method == 'GET':
        tasks = Task.objects.all().values(
            "id",
            "title",
            "status",
            "created_at",
            "due_date"
        )
        return JsonResponse(list(tasks), safe=False)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        required_fields = ['title', 'status', 'user_id']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return JsonResponse({'error': f'Missing fields{missing}'}, status=400)

        parent_task = None
        if data.get('parent_task'):
            try:
                parent_task = Task.objects.get(id=data['parent_task'])
            except Task.DoesNotExist:
                return JsonResponse({'error': 'parentTask not found'}, status=400)
        
        task = Task.objects.create(
            user_id=data['user_id'],
            title=data['title'],
            desc=data.get('desc', ''),
            due_date=data.get('due_date',None),
            status=data['status'],
            parent_task=parent_task
        )

        return JsonResponse({
            'id': task.id,
            'user_id': task.user_id,
            'title': task.title,
            'desc': task.desc,
            'created_at': task.created_at,
            'due_date': task.due_date,
            'status': task.status,
            'parent_task': task.parent_task.id if task.parent_task else None
        }, status=201)
    

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def task_view(request, task_id):
    if request.method == 'GET':
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
        
        return JsonResponse({
            "id": task.id,
            "user_id": task.user_id,
            'title': task.title,
            'desc': task.desc,
            'created_at': task.created_at,
            'due_date': task.due_date,
            'status': task.status,
            'parent_task': task.parent_task.id if task.parent_task is not None else None
        })
    
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task does not exist'}, status=404)

        if 'title' in data:
            task.title = data['title']
        if 'desc' in data:
            task.desc = data['desc']
        if 'due_date' in data:
            task.due_date = data['due_date']
        if 'status' in data:
            task.status = data['status']
        if 'parent_task' in data:
            if data['parent_task'] is None:
                task.parent_task = None
            else:
                try:
                    parent = Task.objects.get(id=data['parent_task'])
                    task.parent_task = parent
                except Task.DoesNotExist:
                    return JsonResponse({'error': 'parent_task not found'}, status=400)
        
        task.save()

        return JsonResponse({
            'message': 'Task updated successfully',
            'task': {
                'id': task.id,
                'user_id': task.user_id,
                'title': task.title,
                'desc': task.desc,
                'created_at': task.created_at,
                'due_date': task.due_date,
                'status': task.status,
                'parent_task': task.parent_task.id if task.parent_task else None,
            }
        })

    if request.method == 'DELETE':
        try:
            Task.objects.get(id=task_id).delete()
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)

        return JsonResponse({}, status=204)