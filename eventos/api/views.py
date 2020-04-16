from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from eventos.api.serializers import (EventsSerializer, PostSerializer,
                                     EventSerializer)
from eventos.models import Event, Post


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_create_Event(request):
    user = request.user
    st = request.data['status']
    stock = request.data['stock']
    title = request.data['title']
    type = request.data['type']
    newEvent = Event(eventOwner=user, eventType=type, title=title, status=st, stock=stock).save(),
    data={}
    data["success"] = "create successful"
    return Response(data=data)
        
        
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_detail_Event_view(request, slug):
    try:
        obj = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(obj)
        return Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_Event_view(request, slug):
    try:
        obj = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EventSerializer(obj, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_BarPost_view(request, slug):
    try:
        obj = Event.objects.get(slug=slug)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = obj.delete()
        data = {}
        if operation:
            data["success"] = "object deleted"
        else:
            data["failed"] = "object could not be deleted"
        return Response(data=data)


# @api_view(['POST',])
# @permission_classes((IsAuthenticated,))
# def api_addUser_EventPost_view(request):
#     data = {}
#     code = request.data['code']
#     user = request.user
#     try:
#         # CHEQUEO CODIGO DEL EVENTO VS EL QUE ME MANDA EL USUARIO
#         obj = EventPost.objects.get(code=code)
#     except EventPost.DoesNotExist or user.DoesNotExist:
#         data['response'] = 'Error'
#         data['error_message'] = 'Código incorrecto'
#         return Response(data=data, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'POST':
#         obj.users.add(user)
#         # qs = obj.users.all() #Esto el dia de mañana se podria sacar, siento que es ineficiente
#         # if qs.filter(pk=user.pk).exists():
#         try:
#             #sPRbyU = postrelations.objects.get(person = user, code = code)
#             sPRbyU = postrelations.objects.get(person=user, event=obj)
#             data['response'] = 'Error'
#             data['error_message'] = 'Duplicate association.'

#         except ObjectDoesNotExist:
#             newPR = postrelations()
#             newPR.person = user
#             newPR.event = obj
#             newPR.notificationToken = request.data['notificationToken']
#             newPR.save()
#             data["success"] = "users belong to the event"
#         return Response(data=data)



@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_addUser_Event_view(request):
    data = {}
    code = request.data['pk']
    user = request.user
    try:
        # CHEQUEO CODIGO DEL EVENTO VS EL QUE ME MANDA EL USUARIO
        event = Event.objects.get(pk=code)
    except Event.DoesNotExist or user.DoesNotExist:
        data['response'] = 'Error'
        data['error_message'] = 'Código incorrecto'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if event.stock << event.activeParticipants and event.status == "O":
         try:
            #sPRbyU = postrelations.objects.get(person = user, code = code)
            newPost = Post.objects.get(person=user, event=event)
            data['response'] = 'Error'
            data['error_message'] = 'Duplicate association.'

         except ObjectDoesNotExist:
            newPost = Post()
            newPost.person = user
            newPost.event = event
            newPost.notificationToken = request.data['notificationToken']
            newPost.save()
            event.activeParticipants+= 1
            event.save()
            data["success"] = "users belong to the event"
            if event.stock == event.activeParticipants:
                    event.status = "F"
                    event.save()
         return Response(data=data)
        else:
            event.status = "F"
            event.save()
            data['response'] = 'Error'
            data['error_message'] = 'Evento finalizado'
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_eventrel_state(request):
    data = {}
    code = request.data["pk"]
    user = request.user
    try:
        obj = Event.objects.get(pk=code)
    except Event.DoesNotExist or user.DoesNotExist:
        data["failed"] = "Wrong Event Code"
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    statusE = obj.status
    if statusE in ('O', '2BO'):
        user = request.user
        if request.method == 'POST':
         try:
            event = Post.objects.get(person=user, event=obj)
            data['status'] = event.status
            data['response'] = 'OK'
         except ObjectDoesNotExist:
            data['status'] = 'N'
            data['response'] = 'OK'

    else:
        data["is_finalized"] = "True"
        data["status"] = statusE
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        
    return Response(data=data)

'''
Api para que un usuario finalice el evento porque recibió su beneficio.

'''
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_fin_event_view(request):
    data={}
    code = request.data["pk"]
    user = request.user
    data4Company = request.data["data4Company"]    
    try:
        obj = Event.objects.get(pk=code)
    except Event.DoesNotExist or user.DoesNotExist:
        data["failed"] = "Wrong Event Code"
        return Response(data=data,status= status.HTTP_404_NOT_FOUND)

    try:
        post2fin = Post.objects.get(person =user, event =obj)
        if post2fin.status == 'W':
            post2fin.status ='F'
            post2fin.data4Company = data4Company
            post2fin.save()
            data["success"] = "update successful"
            data['status'] = 'Finalized'
        else:
         data['response'] = 'Error'
         data['error_message'] = 'Post is not winner'
                    
    except ObjectDoesNotExist:
            data['response'] = 'Error'
            data['error_message'] = 'EventRelation doesnt exist'
    return Response(data=data)





@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_won_events_view(request):
    user = request.user
    bodyResp = {}
    codesW = ""
    codesWArray = []
    # Busco todos los eventos que tiene el user y no están finalizados.
    # Person.objects.filter(
    # ...     group__name='The Beatles',
    # ...     membership__date_joined__gt=date(1961,1,1))
    # EventPostsOpen =BarPost.objects.exclude(is_finalized= False).count()
    # zero = 0
    # http://mrsenko.com/blog/atodorov/2016/08/30/loading-initial-data-for-many-to-many-fields/
    # https://stackoverflow.com/questions/24894961/django-meta-many-to-many
    # if EventPost.objects.filter(is_finalized= False).count()> 0:
    if Event.objects.filter(status="O").count() > 0:
        # bodyResp["mayor"] ="True"
        # bodyResp["count "] =  BarPost.objects.filter(is_finalized= False).count()
        PostsOpen = Event.objects.filter(status="O")
        #bodyResp["barpostOpen"] = barPostsOpen[0].code
        #i=0
        #bodyResp["indice0"] = i
        for each in PostsOpen:
         #   bodyResp["barpostOpeninFOR"] = barPostsOpen[2].code
         #   bodyResp["indicefor"] = i
            if each.usersWinners.filter(pk=user.pk).exists():
                codesWArray.append(each.code)
                #codesW += each.code+","
    else:
        bodyResp["eventsOpen"] = "False"
    # bodyResp["codeWinner"] = codeWinner
    # bodyResp["codesW"]   = codesW
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


class api_Post_view(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    # pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['status', 'event__status']

    def get_queryset(self):
        context = {}
        try:
            user = self.request.user
        except user.DoesNotExist:
            context['response'] = 'Error'
            context['error_message'] = 'User does not exist'
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        # if user is not None:
        queryset = Post.objects.filter(person=user).exclude(event__status='C')
        # else:
           # queryset = PostRelations.objects.all()
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
    queryset = Event.objects.all()

    def get_queryset(self):
        queryset = Event.objects.exclude(status='C').order_by('-createTime')
        return queryset


    '''
Devuelve TODOS los eventos que ganó el usuario y NO están finalizados.
    if EventPostsOpen.objects.filter(users=user.pk).exists():
        postsActives = EventPostsOpen.objects.filter(pk=user.pk)
        codeWinner =  postsActives[0].code
    else:
        codeWinner  = "False" #El usuario no ganó      
'''