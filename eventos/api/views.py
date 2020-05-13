import smtplib
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from eventos.api.serializers import (EventsSerializer, PostIGSerializer,
                                     PostSerializer)
from eventos.models import Event, Post


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_Event(request):
    user = request.user
    st = request.data['status']
    stock = request.data['stock']
    title = request.data['title']
    type = request.data['type']
    newEvent = Event(eventOwner=user, eventType=type, title=title, status=st, stock=stock)
    newEvent.save()
    data = {}
    data["success"] = "create successful"
    return Response(data=data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_addUser_Event_view(request):
    data = {}
    code = request.data['pk']
    user = request.user
    EMAIL_ADDRESS = "support@biancaapp.com"
    EMAIL_PASSWORD = "ndkoeuvetbmxrqgu"
    try:
        event = Event.objects.get(pk=code)
    except (Event.DoesNotExist, user.DoesNotExist):
        data['response'] = 'Error'
        data['error_message'] = 'Código incorrecto'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    if event.stock > event.activeParticipants and event.status == "O":
        try:
            newPost = Post.objects.get(person=user, event=event)
            data['response'] = 'Error'
            data['error_message'] = 'Duplicate association.'
            return Response(data=data)

        except ObjectDoesNotExist:
            newPost = Post()
            newPost.person = user
            newPost.profile = user.profile
            newPost.event = event
            newPost.notificationToken = request.data['notificationToken']
            newPost.save()
            event.activeParticipants += 1
            event.save()
            # --------- Sending mail to us@biancaapp.com ------------------
            with smtplib.SMTP('smtp-relay.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                subject = f'New post: {user.profile.instaAccount}'
                body = f'{user.full_name} ha realizado {event.description} con su cuenta de instagram: {user.profile.instaAccount}. Para valdiar, entrar a https://biancaapp-ndlc.herokuapp.com/admin/eventos/post/'
                msg = f'Subject: {subject}\n\n{body}'
                smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)
            # --------------------------------------------------------------
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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_eventrel_state(request):
    data = {}
    code = request.data["pk"]
    user = request.user
    try:
        obj = Event.objects.get(pk=code)
    except (Event.DoesNotExist, user.DoesNotExist):
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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_fin_event_view(request):
    data = {}
    code = request.data["pk"]
    user = request.user
    data4Company = request.data["data4Company"]
    try:
        obj = Event.objects.get(pk=code)
    except (Event.DoesNotExist, user.DoesNotExist):
        data["failed"] = "Wrong Event Code"
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    try:
        post2fin = Post.objects.get(person=user, event=obj)
        if post2fin.status == 'W':
            post2fin.status = 'F'
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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_won_events_view(request):
    user = request.user
    bodyResp = {}
    codesWArray = []

    if Event.objects.filter(status="O").count() > 0:
        PostsOpen = Event.objects.filter(status="O")
        for each in PostsOpen:
            if each.usersWinners.filter(pk=user.pk).exists():
                codesWArray.append(each.code)
    else:
        bodyResp["eventsOpen"] = "False"
    bodyResp["codesWinners"] = codesWArray
    return Response(data=bodyResp)


class DeliverActiveContracts(ListAPIView):
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
        queryset = Post.objects.filter(person=user).exclude(event__status='C')
        return queryset


class DeliverIGforEvent(ListAPIView):
    """
    Delivers instagram list for a given event primary key
    ONLY FOR SUPERUSERS MANTAIN ACCES TO: ml@biancaapp.com
    """
    serializer_class = PostIGSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pk = self.request.query_params['pk']
        event = Event.objects.get(pk=pk)
        queryset = Post.objects.filter(event=event).filter(status="2BA")
        return queryset


class DeliverAllEvents(ListAPIView):
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
