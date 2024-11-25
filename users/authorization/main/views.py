from django.shortcuts import render
from .models import User, Access, Role, InstituteGroup, Preferences
from .serializers import UserSerializer, AccessSerializer, RoleSerializer, InstituteGroupSerializer, PreferencesSerializer

from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
import logging

import random
import string

import requests
from django.core.exceptions import ObjectDoesNotExist
import json
from .services import \
    create_user_wallet, \
    send_email
from .config import \
    get_change_name_text, \
    get_registration_text
from django.conf import settings
EMAIL_KEY = settings.EMAIL_KEY
USER_OAUTH_YANDEX_TOKEN = settings.USER_OAUTH_YANDEX_TOKEN
from .services import \
    log


class IndexAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        log("=================================", "i")
        preferences = {}
        for preference in request.user.preferences.all():
            preferences[preference.name] = preference.description

        content = {
            'username': request.user.username,
            'name': {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'third_name': request.user.third_name
            },
            'email': request.user.email,
            'book_rate': request.user.book_rate,
            'institute_group': request.user.institute_group.name,
            'user_role': request.user.user_role.name,
            'preferences': preferences
        }
        log(f"Запрос на получение информации о пользователе, U:{request.user.username}", "i")
        return Response(content)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос к получению роли", "i")
        return self.filter_queryset(queryset)


class InstituteGroupViewSet(viewsets.ModelViewSet):
    queryset = InstituteGroup.objects.all()
    serializer_class = InstituteGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос к получению институтских групп", "i")
        return self.filter_queryset(queryset)


class AccessViewSet(viewsets.ModelViewSet):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос к получению уровней доступа", "i")
        return self.filter_queryset(queryset)


class PreferencesViewSet(viewsets.ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос к получению предпочтений доступных в системе", "i")
        return self.filter_queryset(queryset)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        log(f"Начало регистрации пользователя", "i")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            return Response("Регистрация запрещена", status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            username = serializer.data.get('username', 'test_user')
            user = User.objects.get(username=username)
            token, created = Token.objects.get_or_create(user=user)
            log(f"=========. T:{token}", "i")
            user_wallet = create_user_wallet(token, user)
            
            # Собираем данные для отправки email сообщения
            email_address = user.email
            email_text = get_registration_text(user.username)
            email_title = f"Регистрация нового пользователя {user.username}"
            send_email(email_address, email_text, email_title)

            log(f"Пользователь успешно зарегистрирован. U:{user.username}", "i")
            return Response(
                {"data": serializer.data, "result": user_wallet},
                status=status.HTTP_201_CREATED)
        log(f"Неправильный serializer, S:{str(serializer)}", "e")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_user_name(request):
    if request.method == 'POST':
        data_request = json.loads(list(request.POST.dict())[0])
        token  = data_request.get("token", "")
        try:
            user = Token.objects.get(key=token).user
            if user is not None:
                request_type = data_request.get('type')
                match request_type:
                    case "edit_user_name" | "edit_user_email":
                        log(f"Начало редактирования ФИО или Почты", "i")
                        serializer = UserSerializer(user, data=data_request, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            user.save()

                            # Собираем данные для отправки email сообщения
                            email_address = user.email
                            email_text = get_change_name_text(user.username,data_request)
                            email_title = f"Изменение ФИО пользователя {user.username}"
                            send_email(email_address, email_text, email_title)

                            log(f"ФИО пользователя успешно изменены. U:{user.username}", "i")
                            return Response(
                                {
                                    "Result": "True",
                                    "serializer": str(serializer)
                                },
                                status=status.HTTP_202_ACCEPTED)
                        else:
                            log(f"===== 7", "e")
                            log(f"Неправильный serializer, S:{str(serializer)}", "e")
                            return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
                    case "edit_user_group":
                        log(f"Начало редактирования группы пользователя", "i")
                        group_name  = data_request.get("group", "Б00-000")
                        group = InstituteGroup.objects.filter(name=group_name)
                        if len(group) == 1:
                            user.institute_group = group[0]
                            user.save()
                            log(f"Группа успешно изменена, U:{user.username}, G:{group_name}", "i")
                            return Response({"Result": "True"}, status=status.HTTP_202_ACCEPTED)
                        else:
                            log(f"Неправильное название группы, G:{group_name}", "e")
                            return Response(
                                {
                                    "Error": "GROUP_NOT_ACCEPTABLE",
                                    "Description": "Wrong group name"
                                },
                                status=status.HTTP_406_NOT_ACCEPTABLE)
                    case "add_preference":
                        log(f"Редактирование предпочтений пользователя", "i")
                        preference_name  = data_request.get("preference_name", "Тихо")
                        user.add_preference(preference_name)
                        return Response({"Result": "True"}, status=status.HTTP_202_ACCEPTED)
                    case "remove_preference":
                        log(f"Редактирование предпочтений пользователя", "i")
                        preference_name  = data_request.get("preference_name", "Тихо")
                        user.remove_preference(preference_name)
                        return Response({"Result": "True"}, status=status.HTTP_202_ACCEPTED)
                    case _:
                        log(f"Неправильный тип запроса, T:{data_request.get('type')}", "e")
                        return Response(
                            {
                                "Error": "BAD_REQUEST_TYPE",
                                "Description": "Wrong request type. Acceptable: "
                                               "edit_user_name, edit_user_email, edit_user_group"},
                            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            else:
                log(f"Нельзя получить пользователя по токену, T:{token}", "e")
                return Response(
                    {"Error": "BAD_REQUEST_TYPE", "Description": "Current user is none"},
                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            log(f"Error:{e}", "e")
            return Response(
                {
                    "Error": "BAD_REQUEST_TYPE",
                    "Description": f"Wrong token: {e}",
                    "request.POST": f"{json.loads(list(request.POST.dict())[0])}"
                },
                 status=status.HTTP_400_BAD_REQUEST)
        except ConnectionError as e:
            log(f"ConnectionError. Error:{e}", "e")
            return Response(
                {"Error": "ConnectionError", "value": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            log(f"Error:{e}", "e")
            return Response({"Error": "Error", "value": str(e)},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)


def generate_random_letters(length=10):
  letters = random.choices(string.ascii_letters, k=length)
  return ''.join(letters)


def get_usrname_by_email(email):
    random_letters = generate_random_letters()
    return random_letters


@api_view(['POST', 'GET'])
def oauth_yandex(request):
    if request.method == 'GET':
        log(f"request.GET:{request.GET}  dict:{request.GET.dict()}", "i")
        data_request = request.GET.dict()

        url = "https://login.yandex.ru/info"
        params = {
            "oauth_token": data_request.get("access_token"),
            "format": "json",
            "jwt_secret": USER_OAUTH_YANDEX_TOKEN
        }
        
        response = requests.get(url, params=params)
        log(f"status_code={response.status_code}", "i")

        if response.status_code == 200:
            oauth_email = response.json().get('default_email', '')
            oauth_username = get_usrname_by_email(oauth_email)
            log(f"oauth_email={oauth_email} response={response.json()} username={oauth_username}", "i")

            number_of_users_with_email = len(User.objects.filter(email=oauth_email))
            if number_of_users_with_email == 0:
                log(f"Регистрация пользоватея: {oauth_email}", "i")
                new_user = User.objects.create_user(oauth_username)
                new_user.email = oauth_email
                new_user.first_name = response.json().get("first_name").split(" ")[0]
            
                if len(response.json().get("first_name").split(" ")) > 1:
                    new_user.third_name = response.json().get("first_name").split(" ")[1]
            
                new_user.last_name = response.json().get("last_name")
                new_user.token = data_request.get("access_token")
                new_user.institute_group = InstituteGroup.objects.get(name="Б00-000")
                new_user.user_role = Role.objects.get(name="Пользователь")
                new_user.save()

                new_token, created = Token.objects.get_or_create(user=new_user)
                log(f"=========. T:{new_token}", "i")
                user_wallet = create_user_wallet(new_token, new_user)

                return Response({
                    "Result": response.json(),
                    "token_for_user": new_token.key, 
                    "access_token": data_request.get("access_token", "")}, status=status.HTTP_202_ACCEPTED)
            elif number_of_users_with_email == 1:    
                log(f"Авторизация пользователя u:{oauth_email}", "i")
                my_user = User.objects.get(email=oauth_email)
                my_token, created = Token.objects.get_or_create(user=my_user)

                return Response({
                    "Result": response.json(),
                    "token_for_user": my_token.key,
                    "access_token": data_request.get("access_token", "")}, status=status.HTTP_202_ACCEPTED)
            else:
                log(f"Зарегистрировано слишком много пользователей с этой почтой: {number_of_users_with_email}", "i")
                return Response({"Error": "Error", "value": "Зарегистрировано слишком много пользователей с этой почтой"},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            log(f"Status code: {response.status_code}", "e")
            log(f"Response: {response}", "i")
        token  = data_request.get("token", "")
        try:
            user = Token.objects.get(key=token).user
            if user is not None:
                log("Возвращаем подтверждение существования пользователя при корректности токена", "i")
                return Response({"Result": "True", "Token": token}, status=status.HTTP_202_ACCEPTED)
            else:
                log("Создание пользователя по полученному токену из Яндекс Авторизации", "i")
                return Response({"Result": "True","Token": token}, status=status.HTTP_202_ACCEPTED)
        except ConnectionError as e:
            log(f"ConnectionError. Error:{e}", "e")
            return Response({"Error": "ConnectionError", "value": str(e), "Token__": token}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            log(f"Error:{e}", "e")
            return Response({"Error": "Error", "value": str(e),"Token_": token},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if request.method == 'GET':
        return render(request, 'oauth/index.html')
