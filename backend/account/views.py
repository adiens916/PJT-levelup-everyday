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

    def change_standard_reset_time(request: HttpRequest) -> None:
        standard_reset_time = request.POST.get('standard_reset_time')
        # ex) '03:30'
        # TODO: 정규표현식으로 체크하기
        if standard_reset_time:
            hour, minute = standard_reset_time.split(':')
            user.standard_reset_time = datetime.time(int(hour), int(minute))
            user.save()


    if request.method == 'POST':
        user = create_user(request)
        change_standard_reset_time(request)
        return JsonResponse({'id': user.pk})    
    else:
        return HttpResponseBadRequest()


def login(request: HttpRequest):
    pass


def logout(request: HttpRequest):
    pass