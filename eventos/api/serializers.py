from rest_framework import serializers

from eventos.models import Event, Post


class EventPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['title', 'company', 'slug', 'users']

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


class PostRelationsSerializer(serializers.ModelSerializer):

    instaaccount = serializers.SerializerMethodField('get_instaaccount_from_person')
    eventTitle = serializers.SerializerMethodField('get_eventTitle_from_event')
    eventStatus = serializers.SerializerMethodField('get_event_status')
    eventId = serializers.SerializerMethodField('get_event_id_from_event')

    def get_instaaccount_from_person(self, postrelations):
        instaaccount = postrelations.person.instaaccount
        return instaaccount

    def get_eventTitle_from_event(self, postrelations):
        eventTitle = PostRelations.event.title
        return eventTitle

    def get_event_id_from_event(self, postrelations):
        eventId = PostRelations.event.pk
        return eventId

    def get_event_status(self, postrelations):
        eventstatus = PostPelations.event.status
        return eventstatus

    class Meta:
        model = PostRelations
        fields = ['instaaccount', 'eventTitle', 'eventId', 'createTime', 'status', 'eventStatus', 'event']


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            'pk',
            'title',
            'image',
            'company',
            'desc',
            'createTime',
            'status'
            ]
