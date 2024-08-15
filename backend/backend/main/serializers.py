from .models import Institute, Building, AudienceStatus, Audience, UsersWallet, Book, BookHistory
from rest_framework import serializers


class InstituteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institute
        fields = ['name', 'description']


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ['name', 'institute', 'description']


class AudienceStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudienceStatus
        fields = ['name', 'description']


class AudienceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Audience
        fields = ['number', 'building', 'number_of_users', 'audience_status', 'description']


class UsersWalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UsersWallet
        fields = ['', '']


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['', '']


class BookHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookHistory
        fields = ['', '']
