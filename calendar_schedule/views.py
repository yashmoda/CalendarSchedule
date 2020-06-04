import datetime
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from passlib.context import CryptContext
from calendar_schedule.models import UserData, CalendarData


@require_http_methods(["POST"])
@csrf_exempt
def register_user(request):
    response_json = {}
    try:
        name = request.POST.get('name')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            password_context = get_password_context()
            hashed_password = password_context.encrypt(password)
            UserData.objects.create(name=name, email_id=email_id, password=hashed_password)
            response_json['status'] = 200
            response_json['message'] = "The user has been successfully created."
            return JsonResponse(response_json)
        else:
            response_json['status'] = 300
            response_json['message'] = "The passwords do not match."
            return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


@require_http_methods(["POST"])
@csrf_exempt
def login_user(request):
    response_json = {}
    try:
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        try:
            user_instance = UserData.objects.get(email_id__exact=email_id)
        except Exception as e:
            response_json['status'] = 400
            response_json['message'] = "The user does not exist."
            return JsonResponse(response_json)
        user_password = user_instance.password
        password_context = get_password_context()
        if password_context.verify(password, user_password):
            access_token = encode_access_token(email_id)
            request.session['access_token'] = access_token
            response_json['access_token'] = access_token
            response_json['status'] = 200
            response_json['message'] = "You have been successfully logged in."
            return JsonResponse(response_json)
        else:
            response_json['status'] = 300
            response_json['message'] = "You have entered an incorrect password."
            return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


@require_http_methods(["GET"])
def logout_user(request):
    response_json = {}
    try:
        del request.session['access_token']
        response_json['status'] = 200
        response_json['message'] = "You have been logged out successfully."
        return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


@require_http_methods(["GET"])
def list_events(request):
    response_json = {"event_list": []}
    try:
        access_token = request.session["access_token"]
        user_email = decode_access_token(access_token)
        if UserData.objects.filter(email_id__exact=user_email).count() == 1:
            events = CalendarData.objects.filter(user_id__email_id__exact=user_email,
                                                 event_date__gte=datetime.datetime.today().date(),
                                                 is_deleted=False)
            for event in events:
                temp_json = {'event_name': event.event_name,
                             'event_description': event.event_description,
                             'event_date': event.event_date,
                             'event_time': event.event_time}
                response_json["event_list"].append(temp_json)
            response_json['status'] = 200
            response_json['message'] = "All the events has been listed successfully."
            return JsonResponse(response_json)
        else:
            response_json['status'] = 300
            response_json['message'] = "You an invalid user."
            return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


@require_http_methods(["POST"])
@csrf_exempt
def add_event(request):
    response_json = {}
    try:
        access_token = request.session["access_token"]
        user_email = decode_access_token(access_token)
        if UserData.objects.filter(email_id__exact=user_email).count() == 1:
            user_instance = UserData.objects.get(email_id__exact=user_email)
            event_name = request.POST.get('event_name')
            event_description = request.POST.get('event_description')
            event_date = request.POST.get('event_date')
            event_time = request.POST.get('event_time')
            event_date = datetime.datetime.strptime(event_date, "%d-%m-%Y").date()
            event_time = datetime.datetime.strptime(event_time, "%H:%M").time()
            CalendarData.objects.create(user_id=user_instance, event_name=event_name,
                                        event_description=event_description,
                                        event_date=event_date, event_time=event_time)
            response_json['status'] = 200
            response_json['message'] = "The event has been successfully created."
            return JsonResponse(response_json)
        else:
            response_json['status'] = 300
            response_json['message'] = "You are an invalid user."
            return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


@require_http_methods(["GET"])
def delete_event(request):
    response_json = {}
    try:
        access_token = request.session["access_token"]
        event_id = request.GET.get('event_id')
        user_email = decode_access_token(access_token)
        if UserData.objects.filter(email_id__exact=user_email).count() == 1:
            try:
                event_instance = CalendarData.objects.get(user_id__email_id__exact=user_email,
                                                          id=event_id, is_deleted=False)
                event_instance.is_deleted = True
                event_instance.save()
                response_json['status'] = 200
                response_json['message'] = "The event has been deleted."
            except Exception as e:
                response_json['status'] = 200
                response_json['message'] = "The event has already been deleted."
                return JsonResponse(response_json)
        else:
            response_json['status'] = 300
            response_json['message'] = "You are an invalid user."
            return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


# noinspection DuplicatedCode
@require_http_methods(["POST"])
@csrf_exempt
def edit_event(request):
    response_json = {}
    try:
        access_token = request.session["access_token"]
        user_email = decode_access_token(access_token)
        if UserData.objects.filter(email_id__exact=user_email).count() == 1:
            event_id = request.POST.get('event_id')
            event_name = request.POST.get('event_name')
            event_description = request.POST.get('event_description')
            event_date = request.POST.get('event_date')
            event_time = request.POST.get('event_time')
            event_date = datetime.datetime.strptime(event_date, "%d-%m-%Y").date()
            event_time = datetime.datetime.strptime(event_time, "%H:%M").time()
            try:
                event_instance = CalendarData.objects.get(user_id__email_id__exact=user_email,
                                                          id=event_id, is_deleted=False)
            except Exception as e:
                response_json['status'] = 400
                response_json['message'] = "The event does not exist."
                return JsonResponse(response_json)
            event_instance.event_time = event_time
            event_instance.event_date = event_date
            event_instance.event_name = event_name
            event_instance.event_description = event_description
            event_instance.save()
            response_json['status'] = 200
            response_json['message'] = "The event has been edited."
            return JsonResponse(response_json)
        else:
            response_json['status'] = 300
            response_json['message'] = "You are an invalid user."
            return JsonResponse(response_json)
    except Exception as e:
        print(str(e))
        response_json['status'] = 400
        response_json['message'] = "An error has occurred. Please try again later."
        return JsonResponse(response_json)


def encode_access_token(email):
    return str(jwt.encode({'access_token': email}, 'dflshdflshdfsld', algorithm='HS256').decode('utf-8'))


def decode_access_token(access_token):
    return jwt.decode(access_token, 'dflshdflshdfsld', algorithms=['HS256'])["access_token"]


def get_password_context():
    return CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256", pbkdf2_sha256__default_rounds=3000)