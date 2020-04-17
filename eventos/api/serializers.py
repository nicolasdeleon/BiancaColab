from rest_framework import serializers

from eventos.models import Event, Post


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'pk', 'status','benefitDescription']


class PostSerializer(serializers.ModelSerializer):

    event = EventSerializer(
        read_only=True
        )

    class Meta:
        model = Post
        fields = ['createTime', 'status', 'event']


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'pk',
            'title',
            'image',
            'description',
            'createTime',
            'status'
            ]
