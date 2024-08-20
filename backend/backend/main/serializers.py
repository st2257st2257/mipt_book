from .models import Institute, Building, AudienceStatus, Audience, UsersWallet, Book, BookHistory
from rest_framework import serializers
import datetime


class InstituteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institute
        fields = ['name', 'description']


class BuildingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ['name', 'institute', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['institute'] = InstituteSerializer(instance.institute).data
        return response


class AudienceStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudienceStatus
        fields = ['name', 'description']


class AudienceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Audience
        fields = ['number', 'building', 'number_of_users', 'audience_status', 'description']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['building'] = {
            'name': instance.building.name,
            'institute': InstituteSerializer(instance.building.institute).data,
            'description': instance.building.description}
        response['audience_status'] = AudienceStatusSerializer(instance.audience_status).data
        return response


class UsersWalletSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UsersWallet
        fields = ['', '']


class BookSerializer(serializers.HyperlinkedModelSerializer):

    """def create(self, validated_data):
        user = Book.objects.create_user(
            audience=validated_data.get('audience', 'blank_email_audience'),
            user=validated_data.get('user', 'blank_user'),
            number_bb=validated_data.get('number_bb', 0),
            pair_number=validated_data.get('pair_number', 0),
            date=validated_data.get('date', datetime.date.today),
            booking_time=validated_data.get('booking_time', '')
        )

        return user"""

    class Meta:
        model = Book
        fields = ['audience', 'user', 'number_bb', 'pair_number', 'date', 'booking_time']


class BookHistorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookHistory
        fields = ['', '']
