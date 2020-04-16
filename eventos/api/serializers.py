from rest_framework import serializers

from eventos.models import Event, Post


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['title', 'slug', 'users']

    def update(self, instance, validated_data):
        """ Update event post """
        instance.title = validated_data.get('title', instance.title)
        instance.company = validated_data.get('content', instance.content)
        # instance.slug = validated_data.get('created', instance.created)
        # instance.users = validated_data.get('created', instance.created)
        # return instance

"""
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance
"""


class PostSerializer(serializers.ModelSerializer):

    instaaccount = serializers.SerializerMethodField('get_instaaccount_from_person')
    eventTitle = serializers.SerializerMethodField('get_eventTitle_from_event')
    eventStatus = serializers.SerializerMethodField('get_event_status')
    eventId = serializers.SerializerMethodField('get_event_id_from_event')

    def get_instaaccount_from_person(self, postrelations):
        instaaccount = Post.person.profile.instaaccount
        return instaaccount

    def get_eventTitle_from_event(self, postrelations):
        eventTitle = Post.event.title
        return eventTitle

    def get_event_id_from_event(self, postrelations):
        eventId = Post.event.pk
        return eventId

    def get_event_status(self, postrelations):
        eventstatus = Post.event.status
        return eventstatus

    class Meta:
        model = Post
        fields = ['instaAccount', 'eventTitle', 'eventId', 'createTime', 'status', 'eventStatus', 'event']


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
