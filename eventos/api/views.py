import smtplib
import json
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
import boto3
from botocore.exceptions import ClientError
from eventos.api.serializers import (EventsSerializer, PostIGSerializer, PostSerializer)
from eventos.models import Event, Post, InstaStoryPublication


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


EMAIL_ADDRESS = "support@biancaapp.com"
EMAIL_PASSWORD = "ndkoeuvetbmxrqgu"


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_addUser_Event_view(request):
    data = {}
    code = request.data['pk']
    user = request.user
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
            newInstaStory = InstaStoryPublication(person=user)
            newInstaStory.save()
            newPost = Post()
            newPost.person = user
            newPost.profile = user.profile
            newPost.event = event
            newPost.notificationToken = request.data['notificationToken']
            newPost.instagramStory = newInstaStory
            newPost.save()
            event.posts.add(newInstaStory)
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
def api_removeUser_Event_view(request):
    data = {}
    code = request.data['pk']
    user = request.user
    try:
        event = Event.objects.get(pk=code)
    except (Event.DoesNotExist, user.DoesNotExist):
        data['response'] = 'Error'
        data['error_message'] = 'Event not found.'
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

    try:
        newPost = Post.objects.get(person=user, event=event, status="2BA")
        newPost.delete()
        data['response'] = 'Success'
        data['error_message'] = 'User sucessfully removed.'
        return Response(data=data)

    except ObjectDoesNotExist:
        data['response'] = 'Error'
        data['error_message'] = 'User does not belong to event or not in status 2BA'
        return Response(data=data)


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
                post = Post.objects.get(person=user, event=obj)
                data['status'] = post.status
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


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def api_validate_cupon(request):
    print("La reconoci")
    user = request.user
    res = {}
    exchange_code = request.data['code']
    try:
        post = Post.objects.get(exchange_code=exchange_code)
        user_event = Event.objects.filter(eventOwner=user)
        if post.event not in user_event:
            res["error"] = "Código no corresponde a eventos del local."
            return Response(status=status.HTTP_404_NOT_FOUND)
    except (Post.MultipleObjectsReturned, Post.DoesNotExist):
        res["error"] = "No existe el post"
        return Response(res, status=status.HTTP_404_NOT_FOUND)
    event = post.event
    if post and event.eventType == 'A' \
    and post.receivedBenefit is False and post.status == 'W':
        post.status = 'F'
        post.receivedBenefit = True
        post.save()
        res["success"] = "succesfuly exchanged"
    else:
        res["error"] = "Codigo no válido o ya canjeado."
        return Response(res, status=status.HTTP_404_NOT_FOUND)
    return Response(data=res)


# https://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def api_validate_image_post(request):
    resImage = {}
    fotos = json.loads(request.body)
    resList = {}
    resList["imagesRes"] = []
    for each in fotos['images']:
        publi_id = each['publi_id']
        person_id = each['person_id']
        listaTags = each['tags']
        is_found = False
        try:
            instaStory = InstaStoryPublication.objects.get(pk=publi_id)
        except InstaStoryPublication.DoesNotExist:
            resImage[publi_id] = "Event doesnt exist"
            resList["imagesRes"].append(resImage)
            break
        if Event.objects.filter(posts=instaStory).exists():
            buckets3 = settings.AWS_STORAGE_BUCKET_NAME
            print(buckets3)
            s3_resource = boto3.resource("s3", aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            evento = Event.objects.filter(posts=publi_id)
            for tagEvent in evento[0].tags:
                if is_found is False:
                    if tagEvent in listaTags:
                        is_found = True
                else:
                    break
            newPath = "processed/" + publi_id + "." + person_id
            oldPath = buckets3 + "/" + str(instaStory.image)
            if (is_found):
                newPath = newPath + ".W"
                resImage[publi_id] = "W"
                instaStory.processed_image = "processed/" + publi_id + "." + person_id + ".W"
            else:
                newPath = newPath + ".R"
                resImage[publi_id] = "R"
                instaStory.processed_image = "processed/" + publi_id + "." + person_id + ".R"
            try:
                s3_resource.Object(buckets3, newPath).copy_from(CopySource=oldPath)
            except ClientError as ex:
                resImage["movefile"] = "Error"
                print(ex)
            try:
                s3_resource.Object(buckets3, str(instaStory.image)).delete()
                instaStory.image = ""
                instaStory.save()
            except ClientError as ex:
                resImage["delete"] = "Error"
            resList["imagesRes"].append(resImage)
            resImage[publi_id] = "Event doesnt exist"
            resList["imagesRes"].append(resImage)
    return Response(data=resList)


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
