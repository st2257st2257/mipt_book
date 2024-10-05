from .models import User, Access, Role, InstituteGroup, Preferences
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email', 'blank_email'),
            username=validated_data.get('username', 'blank_user_name'),
            first_name=validated_data.get('first_name', 'Имя'),
            last_name=validated_data.get('last_name', 'Фамилия'),
            third_name=validated_data.get('third_name', 'Отчество'),
            book_rate=validated_data.get('book_rate', 7),
        )
        # set group
        group = InstituteGroup.objects.get(name="Б02-001")
        user.institute_group = group
        user.institute_group.save()
        # set user role
        user_role = Role.objects.get(name="Пользователь")
        user.user_role = user_role
        user.user_role.save()
        # set password
        user.set_password(validated_data.get('password', 'pass'))
        user.save()
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
        fields = ['username', 'email','password', 'first_name', 'last_name', 'third_name', 'book_rate', 'preferences']
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
