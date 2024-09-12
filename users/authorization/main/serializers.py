from .models import User, Access, Role, InstituteGroup, Preferences
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email', 'blank_email'),
            username=validated_data.get('username', 'blank_user_name'),
            password=validated_data.get('pass', 'password'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            third_name=validated_data.get('third_name', ''),
            book_rate=validated_data.get('book_rate', 7)
        )

        return user

    def update(self, user, validated_data):
        # user = Token.objects.get(key=validated_data.get("token")).user
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name  = validated_data.get("last_name", user.last_name)
        user.third_name = validated_data.get("third_name", user.third_name)
        user.email = validated_data.get("email", user.email)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'third_name', 'book_rate', 'preferences']
        extra_kwargs = {'password': {'write_only': True}}


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
