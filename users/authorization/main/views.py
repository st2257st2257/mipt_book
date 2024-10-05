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

from django.core.exceptions import ObjectDoesNotExist
import json
from .services import \
    create_user_wallet


class IndexAuth(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
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
            'user_role': request.user.user_role.name
        }
        return Response(content)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class InstituteGroupViewSet(viewsets.ModelViewSet):
    queryset = InstituteGroup.objects.all()
    serializer_class = InstituteGroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class AccessViewSet(viewsets.ModelViewSet):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


class PreferencesViewSet(viewsets.ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_queryset(queryset)


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.data.get('username', 'test_user')
            user = User.objects.get(username=username)
            token = Token.objects.get_or_create(user=user)
            user_wallet = create_user_wallet(token, user)
            return Response(
                {"data": serializer.data, "result": user_wallet},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_user_name(request):
    if request.method == 'POST':
        data_request = json.loads(list(request.POST.dict())[0])
        token  = data_request.get("token", "")
        try:
            user = Token.objects.get(key=token).user
            if user is not None:
                if data_request.get('type') == "edit_user_name" or \
                    data_request.get('type') == "edit_user_email":
                    serializer = UserSerializer(user, data=data_request, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        user.save()
                        return Response(
                            {
                                "Result": "True",
                                "serializer": str(serializer)
                            },
                            status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(serializer.data, status=status.HTTP_406_NOT_ACCEPTABLE)
                elif data_request.get('type') == "edit_user_group":
                    group_name  = data_request.get("group", "Б02-001")
                    group = InstituteGroup.objects.filter(name=group_name)
                    if len(group) == 1:
                        user.institute_group = group[0]
                        user.save()
                        return Response({"Result": "True"}, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(
                            {
                                "Error": "GROUP_NOT_ACCEPTABLE",
                                "Description": "Wrong group name"
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    return Response(
                        {
                            "Error": "BAD_REQUEST_TYPE",
                            "Description": "Wrong request type. Acceptable: "
                                           "edit_user_name, edit_user_email, edit_user_group"},
                        status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            else:
                return Response(
                    {"Error": "BAD_REQUEST_TYPE", "Description": "Current user is none"},
                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response(
                {
                    "Error": "BAD_REQUEST_TYPE",
                    "Description": f"Wrong token: {e}",
                    "request.POST": f"{json.loads(list(request.POST.dict())[0])}"
                },
                 status=status.HTTP_400_BAD_REQUEST)
