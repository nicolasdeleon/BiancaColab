from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from accounts.models import user
from eventos.models import eventpost, postrelations
from eventos.api.serializers import eventpostSerializer, PostRelationsSerializer, EventsSerializer
from rest_framework.filters import SearchFilter, OrderingFilter


from django.core.exceptions import ObjectDoesNotExist

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_eventpost_view(request, slug):
    try:
        obj = eventpost.objects.get(slug=slug)
    except eventpost.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = eventpostSerializer(obj)
        return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,)) #necesitas estar autenticado
def api_update_eventpost_view(request, slug):
    try:
        obj = eventpost.objects.get(slug=slug)
    except eventpost.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = eventpostSerializer(obj, data=request.data) #esto es como el request.POST de los forms
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
        obj = eventpost.objects.get(slug=slug)
    except eventpost.DoesNotExist:
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
def api_addUser_eventpost_view(request):
    data={}
    code = request.data["code"]  
    user = request.user

    try:
        obj = eventpost.objects.get(code=code) #CHEQUEO CODIGO DEL EVENTO VS EL QUE ME MANDA EL USUARIO
    except eventpost.DoesNotExist or user.DoesNotExist:
        data['response'] = 'Error'
        data['error_message'] = 'Código incorrecto'
        return Response(data=data,status= status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
       
        obj.users.add(user)
        #qs = obj.users.all() #Esto el dia de mañana se podria sacar, siento que es ineficiente
        serializer = eventpostSerializer(obj) 

        #if qs.filter(pk=user.pk).exists():
        try:
                #sPRbyU = postrelations.objects.get(person = user, code = code)
                sPRbyU = postrelations.objects.get(person = user, event = obj)
                data['response'] = 'Error'
                data['error_message'] = 'Duplicate association.'
                    
        except ObjectDoesNotExist:
                    newPR = postrelations()
                    newPR.person = user
                    newPR.event = obj
                    newPR.save()
                    data["success"] = "users belong to the event"
        #else:
        #    data["failed"] = "could not add user to event"
        return Response(data=data)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_won_event_view(request):
    data={}
    code = request.data["code"]
    user = request.user    
    try:
        obj = eventpost.objects.get(code=code)
    except eventpost.DoesNotExist or user.DoesNotExist:
        data["failed"] = "Wrong Event Code"
        return Response(data=data,status= status.HTTP_404_NOT_FOUND)

    #data["Vacio"] = "Vacio"
    #if obj.is_finalized == False:
    statusE = obj.status
    if statusE == "O" or statusE == "2BO":    
        user = request.user
        if request.method == 'GET':
         winners = obj.users_winners.all()
         if winners.filter(pk=user.pk).exists():
              data["user_win"] = "True" # El usuario ganó
              data["statusEvent"] = statusE 
         else:
                data["user_win"] = "False" #El usuario no ganó
                data["statusEvent"] = statusE 
           # data["Gano"] = winners[0].email #cuidado con el index out of range
        # return Response(data=data)
       # return Response("hello:")
    else:
        data["is_finalized"] = "True"
        data["status"] = statusE
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
    #if eventpost.objects.filter(is_finalized= False).count()> 0:
    if eventpost.objects.filter(status= "O").count()> 0:    
        #bodyResp["mayor"] ="True" 
        #bodyResp["count "] =  BarPost.objects.filter(is_finalized= False).count()
        PostsOpen = eventpost.objects.filter(status= "O")
        #bodyResp["barpostOpen"] = barPostsOpen[0].code
        #i=0
        #bodyResp["indice0"] = i

        for each in PostsOpen:
         #   bodyResp["barpostOpeninFOR"] = barPostsOpen[2].code
         #   bodyResp["indicefor"] = i
            if each.users_winners.filter(pk=user.pk).exists():
                    codesWArray.append(each.code)
                    #codesW += each.code+","
                    
         
    else:
        bodyResp["eventsOpen"]   = "False"
     

 # bodyResp["codeWinner"] = codeWinner
    #bodyResp["codesW"]   = codesW
    bodyResp["codesWinners"] = codesWArray
    return Response(data=bodyResp)

'''
Se muestran todas las relaciones de mi usuario
En params se coloca 
    - search = 2BA (o cualquier otro status - opcional)
    Si se busca tanto por status y event__status se deben colocar los filtros en ese orden
    ej:
    search = 2BA
    search = F
    - orderedring = -create_time
En headers se coloca el Token Authorization
'''
class api_PostRelations_view(ListAPIView):
    serializer_class = PostRelationsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
#    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)

    search_fields = ['status','event__status']    
    
    def get_queryset(self):
        context = {}
        try:
            user = self.request.user     
        except user.DoesNotExist:
            context['response'] = 'Error'
            context['error_message'] = 'User does not exist'
            return Response(context,status=status.HTTP_404_NOT_FOUND)
 #       if user is not None:
        queryset = postrelations.objects.filter(person=user).exclude(event__status = 'C')
 #       else:
 #           queryset = PostRelations.objects.all()   
        return queryset


'''
Se muestran todos los eventos de a 30 por pÃ¡gina (se setea en settings)
Se puede enviar filtro por is_finalized para obtener los activos
En params se coloca:
    - search = 0 (0 = false del campo is_finalized)
    - orderering = -create_time
    - En el caso que sean mas de 30 resultados agregar page = 1,2,3...
'''

class api_all_events_view(ListAPIView):
    serializer_class = EventsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['status']    
    queryset = eventpost.objects.all()

    def get_queryset(self):
        queryset = eventpost.objects.exclude(status = 'C')
        return queryset