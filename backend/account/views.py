import datetime
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import User

    

# Create your views here.
@csrf_exempt
def signup(request: HttpRequest):
    def create_user(request: HttpRequest) -> User:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        return user

    if request.method == 'POST':
        user = create_user(request)
        return JsonResponse({'id': user.pk})
    else:
        return HttpResponseBadRequest()

def login(request: HttpRequest):
    pass

def logout(request: HttpRequest):
    pass