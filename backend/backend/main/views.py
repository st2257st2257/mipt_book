import asyncio

from django.shortcuts import render
from .models import \
    Institute, \
    Building, \
    AudienceStatus, \
    Audience, \
    UsersWallet, \
    Book, \
    BookHistory
from .serializers import \
    InstituteSerializer, \
    BuildingSerializer, \
    AudienceStatusSerializer, \
    AudienceSerializer, \
    UsersWalletSerializer, \
    BookSerializer, \
    BookHistorySerializer
import requests
from .services import \
    get_timetable, \
    check_token, \
    get_book_audience_response, \
    create_user_wallet, \
    log
import logging
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
import json


class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение институтов.", "d")
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение здания. Параметры:{self.request.query_params}", "d")
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        institute = self.request.query_params.get('institute')
        if name is not None:
            queryset = super().get_queryset().filter(name=name)
        if institute is not None:
            queryset = queryset.filter(institute__name=institute)
        return self.filter_queryset(queryset)


class AudienceStatusViewSet(viewsets.ModelViewSet):
    queryset = AudienceStatus.objects.all()
    serializer_class = AudienceStatusSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос на получение статусов аудитории. Параметры:{queryset}", "d")
        return self.filter_queryset(queryset)


class UsersWalletViewSet(viewsets.ModelViewSet):
    queryset = UsersWallet.objects.all()
    serializer_class = UsersWalletSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
        log(f"Запрос на получение параметров кошелька. Параметры:{queryset}, U:{username}", "d")
        return self.filter_queryset(queryset)


class AudienceViewSet(viewsets.ModelViewSet):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос на получение аудиторий по фильтрам. Параметры:{queryset}", "d")
        building_name = self.request.query_params.get('building_name')
        institute = self.request.query_params.get('institute')
        status = self.request.query_params.get('status')
        if building_name is not None:
            queryset = super().get_queryset().filter(building__name=building_name)
        if institute is not None:
            queryset = queryset.filter(building__institute__name=institute)
        if status is not None:
            queryset = queryset.filter(audience_status__name=status)
        return self.filter_queryset(queryset)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос на получение бронирований по фильтрам. Параметры:{queryset}", "d")
        audience_number = self.request.query_params.get('audience_number')
        user = self.request.query_params.get('user')
        pair_number = self.request.query_params.get('pair_number')
        building_name = self.request.query_params.get('building_name')
        institute = self.request.query_params.get('institute')
        if audience_number is not None:
            queryset = queryset.filter(audience__number=audience_number)
        if user is not None:
            queryset = queryset.filter(user__username=user)
        if pair_number is not None:
            queryset = queryset.filter(pair_number=pair_number)
        if building_name is not None:
            queryset = queryset.filter(audience__building__name=building_name)
        if institute is not None:
            queryset = queryset.filter(audience__building__institute__name=institute)
        return self.filter_queryset(queryset)


class BookHistoryViewSet(viewsets.ModelViewSet):
    queryset = BookHistory.objects.all()
    serializer_class = BookHistorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        log(f"Запрос на получение истории бронирований по фильтрам. Параметры:{queryset}", "d")
        audience_number = self.request.query_params.get('audience_number')
        user = self.request.query_params.get('user')
        pair_number = self.request.query_params.get('pair_number')
        date = self.request.query_params.get('date')
        booking_time = self.request.query_params.get('booking_time')
        if audience_number is not None:
            queryset = queryset.filter(audience=audience_number)
        if user is not None:
            queryset = queryset.filter(user=user)
        if pair_number is not None:
            queryset = queryset.filter(pair_number=pair_number)
        if date is not None:
            queryset = queryset.filter(date=date)
        if booking_time is not None:
            queryset = queryset.filter(booking_time=booking_time)
        return self.filter_queryset(queryset)


@csrf_exempt
@api_view(('POST', 'GET'))
def book_audience(request):
    if request.method == 'POST':
        data_request = json.loads(list(request.POST.dict())[0])
        if data_request.get('type') == "book_audience":
            token = request.POST.get('token')
            check_token_result = asyncio.run(check_token(token))
            if check_token_result["result"]:
                return get_book_audience_response(
                    number=data_request.get('audience'),
                    user=data_request.get('user'),
                    number_bb=int(data_request.get('number_bb', 0)),
                    pair_number=int(data_request.get('pair_number', 0)))
            else:
                return Response(
                    {"Error": "BAD_TOKEN"},
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                {
                    "Error": "BAD_REQUEST_TYPE",
                    "YOUR_REQUEST_TYPE": request.POST.get('type'),
                    "data": json.loads(list(request.POST.dict())[0]),
                    "data_dict": list(request.POST.dict())[0],
                },
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'GET':
        return render(request, 'book/test.html')


@csrf_exempt
@api_view(('POST', 'GET'))
def index_user_wallet(request):
    # DATA FORMAT (POST):
    # {
    #   "token":    "this_is_your_token",
    #   "type":     "create_user_wallet",
    #   "username": "test_user"
    # }
    # logger.debug('')
    # logger.info('')
    # logger.warning('')
    # logger.error('')
    # logger.critical('')
    if request.method == 'POST':
        if request.POST.get('type') == "create_user_wallet":
            token = request.POST['token']
            try:
                check_token_result = asyncio.run(check_token(token))
                if check_token_result["result"]:
                    username = str(request.POST.get('username', None))
                    username.replace('Пользователь: ', '')
                    log(f"Username for register: '{username}'", "i")
                    if username is not None: # and username == check_token_result["value"]["username"]:
                        user_wallet = create_user_wallet(username, token=token)
                        if user_wallet:
                            log(f"User wallet created. Id:{user_wallet.id}, Name:{user_wallet.username}", "i")
                            return Response(
                                {
                                    "result": True,
                                    "create_user_wallet_id": user_wallet.id,
                                    "username": user_wallet.username,
                                    "number_bb": user_wallet.number_bb
                                },
                                status=status.HTTP_201_CREATED)
                        else:
                            log(f"Problems with creating user wallet. User:{username}", "w")
                            return Response(
                                {"Error": "FORBIDDEN_USERNAME"},
                                status=status.HTTP_403_FORBIDDEN)
                    else:
                        log(f"No username in request data. User:{username}, Data:{request.POST}", "w")
                        return Response(
                                {"Error": "NON_AUTHORITATIVE_INFORMATION"},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                else:
                    log(f"Problems with checking token. Token:{token}", "w")
                    return Response(
                        {"Error": "BAD_TOKEN", "value": check_token_result},
                        status=status.HTTP_401_UNAUTHORIZED)
            except ConnectionError as e:
                log(f"ConnectionError. Error:{e}", "e")
                return Response(
                    {"Error": "ConnectionError", "value": str(e)},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as e:
                log(f"Error:{e}", "e")
                return Response({"Error": "Error", "value": str(e)},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            log(f"BAD_REQUEST_TYPE. Request type:{request.POST.get('type')}", "e")
            return Response(
                {"Error": "BAD_REQUEST_TYPE"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'GET':
        return render(request, 'wallet/index.html')


@csrf_exempt
@api_view(('POST', 'GET'))
def index_timetable(request):
    if request.method == 'GET':
        if request.GET.get('type') == "get_timetable":
            log(f"Get timetable ended with success", "i")
            return Response(
                {
                    "result": True,
                    "audience": get_timetable(),
                    "user": 1
                },
                status=status.HTTP_201_CREATED)
        else:
            return render(request,
                  'timetable/index.html')
    if request.method == 'POST':
        return Response(
                {"Error": "BAD_REQUEST_TYPE"}
        )


@csrf_exempt
@api_view(('POST', 'GET'))
def index_stop_booking(request):
    # DATA FORMAT (POST):
    # {
    #   "token":    "this_is_your_token",
    #   "type":     "stop_booking",
    #   "audience": "audience_number"
    # }
    if request.method == 'POST':
        data_request = json.loads(list(request.POST.dict())[0])
        if data_request.get('type') == "stop_booking":
            token = data_request.get('token', '')
            audience_number = data_request.get('audience', '')
            log(f"Start stopping booking. Token:{token}, Audience:{audience_number}", "i")
            try:
                check_token_result = asyncio.run(check_token(token))
                if check_token_result["result"]:
                    books = Book.objects.filter(audience__number=audience_number)
                    booking_number = len(books)
                    if booking_number == 1:
                        book_item = Book.objects.get(audience__number=audience_number)
                        book_item.to_history()
                        log(f"Stopping booking ended with success.", "i")
                        return Response(
                            {
                                "result": True,
                                "audience": audience_number,
                                "token": token
                            },
                            status=status.HTTP_201_CREATED)
                    else:
                        for booking in books:
                            booking.to_history()
                        log(f"Double booking of the audience: {audience_number}. Booking number: {booking_number}", "e")
                        return Response(
                            {
                                "Error": "BookingError",
                                "value": f"length must be is 1, you got {booking_number}",
                                "audience": f"{audience_number}"
                            },
                            status=status.HTTP_501_NOT_IMPLEMENTED)
                else:
                    log(f"Problems with checking token in stop booking. Token:{token}", "e")
            except ConnectionError as e:
                log(f"ConnectionError. Error:{e}", "e")
                return Response(
                    {"Error": "ConnectionError", "value": str(e)},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except Exception as e:
                log(f"Error:{e}", "e")
                return Response({"Error": "Error", "value": str(e)},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            log(f"BAD_REQUEST_TYPE. Type:{data_request.get('type')}", "e")
            return Response(
                {"Error": "BAD_REQUEST_TYPE"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'GET':
        return render(request, 'book/stop_booking.html')
