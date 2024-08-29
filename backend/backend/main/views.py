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

from .services import \
    _get_timetable, \
    check_token, \
    get_audience_by_number, \
    get_user_by_username, \
    get_book_audience_response

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


class InstituteViewSet(viewsets.ModelViewSet):
    queryset = Institute.objects.all()
    serializer_class = InstituteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
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
        return self.filter_queryset(queryset)


class AudienceViewSet(viewsets.ModelViewSet):
    queryset = Audience.objects.all()
    serializer_class = AudienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
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


# @api_view(['POST'])
@csrf_exempt
@api_view(('POST', 'GET'))
def book_audience(request):
    if request.method == 'POST':
        if request.POST.get('type') == "book_audience":
            if check_token(request.POST['token']):
                number = request.POST.get('audience')
                user = request.POST.get('user')
                number_bb = int(request.POST.get('number_bb'))
                pair_number = int(request.POST.get('pair_number'))
                return get_book_audience_response()
                new_book = Book(
                    audience=get_audience_by_number(number),
                    user=get_user_by_username(user),
                    number_bb=number_bb,
                    pair_number=pair_number,
                    date=datetime.datetime.now().date(),
                    booking_time=datetime.datetime.now().time(),
                    visibility=1)
                new_book.save()
                audience = Audience.objects.get(number=number)
                if audience.day_history.pair[pair_number][1] == "Свободно":
                    audience.day_history.pair[pair_number][1] = "Занято"
                    audience.day_history.save()
                    audience.save()
                    return Response(
                        {
                            "result": True,
                            "audience": new_book.audience.number,
                            "user": new_book.user.username,
                            "number_bb": number_bb,
                            "pair_number": pair_number
                        },
                        status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {
                            "result": False,
                            "audience": new_book.audience.number,
                            "status": audience.day_history.pair[pair_number][1],
                            "number_bb": number_bb,
                            "pair_number": pair_number
                        },
                        status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"Error": "BAD_TOKEN"},
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                {"Error": "BAD_REQUEST_TYPE"},
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.method == 'GET':
        return render(request, 'book/test.html')


@csrf_exempt
@api_view(('POST', 'GET'))
def get_timetable(request):
    if request.method == 'GET':
        if request.GET.get('type') == "get_timetable":
            return Response(
                {
                    "result": True,
                    "audience": _get_timetable(),
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
