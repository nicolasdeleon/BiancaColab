from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from BarEvento.models import BarPost
from BarEvento.models import PostRelations
from BarEvento.api.serializers import BarPostSerializer

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_BarPost_view(request, slug):
    try:
        obj = BarPost.objects.get(slug=slug)
    except BarPost.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BarPostSerializer(obj)
        return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,)) #necesitas estar autenticado
def api_update_BarPost_view(request, slug):
    try:
        obj = BarPost.objects.get(slug=slug)
    except BarPost.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

   # user = request.user #ahora puedo pedir usuario
    #if blogpost_author != user:
    #    return Response({'response': "you dont have permission to edit that"})

    if request.method == 'PUT':
        serializer = BarPostSerializer(obj, data=request.data) #esto es como el request.POST de los forms
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_BarPost_view(request, slug):
    try:
        obj = BarPost.objects.get(slug=slug)
    except BarPost.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = obj.delete()
        data = {}
        if operation:
            data["success"] = "object deleted"       
        else:
            data["failed"] = "object could not be deleted"
        return Response(data = data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_addUser_BarPost_view(request):
    data={}
    code = request.data["code"]    
    try:
        obj = BarPost.objects.get(code=code)
    except BarPost.DoesNotExist or user.DoesNotExist:
        data["failed"] = "Wrong Event Code"
        return Response(data=data,status= status.HTTP_404_NOT_FOUND)

    user = request.user
    if request.method == 'POST':
        obj.users.add(user)
        qs = obj.users.all()
        serializer = BarPostSerializer(obj)

        newPR = PostRelations()
        newPR.person = user
        newPR.event = obj
        newPR.code = obj.code
        newPR.save()

        if qs.filter(pk=user.pk).exists():
            data["success"] = "user belongs to the field"
        else:
            data["failed"] = "could not add user to event"
        return Response(data=data)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_won_event_view(request):
    data={}
    code = request.data["code"]    
    try:
        obj = BarPost.objects.get(code=code)
    except BarPost.DoesNotExist or user.DoesNotExist:
        data["failed"] = "Wrong Event Code"
        return Response(data=data,status= status.HTTP_404_NOT_FOUND)

    #data["Vacio"] = "Vacio"
    if obj.is_finalized == False:
        user = request.user
        if request.method == 'GET':
         winners = obj.users_winners.all()
         if winners.filter(pk=user.pk).exists():
              data["user_win"] = "True" # El usuario ganó
              data["is_finalized"] = "False"
         else:
                data["user_win"] = "False" #El usuario no ganó
                data["is_finalized"] = "False"
           # data["Gano"] = winners[0].email #cuidado con el index out of range
        # return Response(data=data)
       # return Response("hello:")
    else:
        data["is_finalized"] = "True"
        Response("finalizo")
    return Response(data=data)


    '''
Devuelve TODOS los eventos que ganó el usuario y NO están finalizados.

    if eventPostsOpen.objects.filter(users=user.pk).exists():
        postsActives = eventPostsOpen.objects.filter(pk=user.pk)
        codeWinner =  postsActives[0].code
    else:
        codeWinner  = "False" #El usuario no ganó      
'''

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_won_events_view(request):
    user = request.user
    bodyResp = {}
    codesW = ""
    codesWArray = []
#Busco todos los eventos que tiene el user y no están finalizados.
#Person.objects.filter(
#...     group__name='The Beatles',
#...     membership__date_joined__gt=date(1961,1,1))
  #  eventPostsOpen =BarPost.objects.exclude(is_finalized= False).count()
   # zero = 0
   #http://mrsenko.com/blog/atodorov/2016/08/30/loading-initial-data-for-many-to-many-fields/
   #https://stackoverflow.com/questions/24894961/django-meta-many-to-many
    if BarPost.objects.filter(is_finalized= False).count()> 0:
        #bodyResp["mayor"] ="True" 
        #bodyResp["count "] =  BarPost.objects.filter(is_finalized= False).count()
        barPostsOpen = BarPost.objects.filter(is_finalized= False)
        #bodyResp["barpostOpen"] = barPostsOpen[0].code
        #i=0
        #bodyResp["indice0"] = i

        for each in barPostsOpen:
         #   bodyResp["barpostOpeninFOR"] = barPostsOpen[2].code
         #   bodyResp["indicefor"] = i
            if each.users_winners.filter(pk=user.pk).exists():
                    codesWArray.append(each.code)
                    #codesW += each.code+","
                    
         
    else:
        bodyResp["mayor"]   = "False"
     

 # bodyResp["codeWinner"] = codeWinner
    #bodyResp["codesW"]   = codesW
    bodyResp["codesWinners"] = codesWArray
    return Response(data=bodyResp)
