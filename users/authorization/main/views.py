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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_user_name(request):
    if request.method == 'POST':
        token  = request.POST.get("token", "")
        try:
            user = Token.objects.get(key=token).user
            if user is not None:
                if request.POST.get('type') == "edit_user_name":
                    return Response("good")
                else:
                    return Response(
                        {
                            "Error": "BAD_REQUEST_TYPE",
                            "Description": "Wrong request type. Acceptable: edit_user_name"},
                        status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
            else:
                return Response(
                    {"Error": "BAD_REQUEST_TYPE", "Description": "Current user is none"},
                    status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response(
                {"Error": "BAD_REQUEST_TYPE", "Description": f"Wrong token: {e}"},
                 status=status.HTTP_400_BAD_REQUEST)

            # user_first_name  = request.POST.get("first_name", "")
            # user_second_name = request.POST.get("second_name", "")
            # user_third_name  = request.POST.get("third_name", "")


