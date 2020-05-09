from rest_framework import serializers

from eventos.models import Event, Post
from accounts.models import Profile


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'pk', 'status', 'eventType', 'benefitDescription', 'image']


class PostSerializer(serializers.ModelSerializer):

    event = EventSerializer(
        read_only=True
    )

    class Meta:
        model = Post
        fields = ['createTime', 'status', 'event', 'data4Company', 'receivedBenefit']


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'pk',
            'title',
            'image',
            'description',
            'createTime',
            'status',
            'benefitDescription',
            'eventType'
        ]


class IGListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['instaAccount']


class PostIGSerializer(serializers.ModelSerializer):

    profile = IGListSerializer(
            read_only=True
        )

    class Meta:
        model = Post
        fields = ['profile']
