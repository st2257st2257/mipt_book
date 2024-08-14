from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class Index(APIView):
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
