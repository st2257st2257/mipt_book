import asyncio

from django.shortcuts import render

from .models import \
    EventItem, \
    EventType, \
    UserSearch, \
    Pair
from .serializers import \
    EventItemSerializer, \
    UserSearchSerializer, \
    PairSerializer, \
    EventTypeSerializer

from rest_framework import permissions, viewsets
from .services import \
    log

class EventItemViewSet(viewsets.ModelViewSet):
    queryset = EventItem.objects.all()
    serializer_class = EventItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_text = self.request.query_params.get('search_text')
        log(f"Запрос на получение всех запланированных мероприятий:{search_text}", "i")
        if search_text is not None:
            queryset = super().get_queryset().filter(name__icontains=search_text)
        return self.filter_queryset(queryset)


class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение типов мероприятий.", "i")
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class PairViewSet(viewsets.ModelViewSet):
    queryset = Pair.objects.all()
    serializer_class = PairSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение пар в системе", "i")
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class UserSearchViewSet(viewsets.ModelViewSet):
    queryset = Pair.objects.all()
    serializer_class = PairSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        log(f"Запрос на получение пользовательских поисков", "i")
        queryset = super().get_queryset()
        owner_user_wallet = self.request.query_params.get('owner_user_wallet')
        if owner_user_wallet is not None:
            queryset = super().get_queryset().filter(owner_user_wallet=owner_user_wallet)
        return self.filter_queryset(queryset)



