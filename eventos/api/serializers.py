from rest_framework import serializers

#modelo a serializar
from eventos.models import eventpost, fotos, postrelations


class eventpostSerializer(serializers.ModelSerializer):

    #quiero obtener las fotos para cada post
 #   imagenes = serializers.SerializerMethodField('get_BarPost_Fotos')

    class Meta:
        model = eventpost
        fields = ['title','company','slug','users','code'] 
        
    #funcion para updatear
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.company = validated_data.get('content', instance.content)
  #      instance.slug = validated_data.get('created', instance.created)
  #      instance.users = validated_data.get('created', instance.created)
  #      return instance
  
  # def get_BarPost_Fotos(self,BarPost):
   #    fotos = BarPost.fotos





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
    

    def get_instaaccount_from_person(self, postrelations):
      instaaccount = postrelations.person.instaaccount
      return instaaccount

    def get_eventTitle_from_event(self, postrelations):
      eventTitle = postrelations.event.title
      return eventTitle

    class Meta:
        model = postrelations
        fields = ['instaaccount','eventTitle','createTime','status'] 

   
class EventsSerializer(serializers.ModelSerializer):

    class Meta:
      model = eventpost
      fields = ['title','company','desc','createTime','code','status'] 