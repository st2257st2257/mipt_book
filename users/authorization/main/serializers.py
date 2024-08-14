from .models import User, Access, Role, InstituteGroup, Preferences
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'second_name', 'third_name', 'book_rate', 'preferences']


class AccessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Access
        fields = ['description']


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'description']


class InstituteGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InstituteGroup
        fields = ['name', 'description']


class PreferencesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preferences
        fields = ['name', 'description']
