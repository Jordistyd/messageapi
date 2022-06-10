from django.shortcuts import HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Message
from .utils import serialize_message
import json
from .constants import Keys, Methods
from django.contrib.auth import get_user_model


class Login:

    @staticmethod
    @csrf_exempt
    def login_user(request):
        if request.method == Methods.POST:
            username = request.POST[Keys.USERNAME]
            password = request.POST[Keys.PASSWORD]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(Messages.show_all_messages, user_name=user.username)
            else:
                return HttpResponse("Check username/password")


class Messages:
    @staticmethod
    def show_all_messages(request, user_name):
        if request.method == Methods.GET:
            messages = set(Message.objects.filter(sender=user_name) | Message.objects.filter(receiver=user_name))
            display_message = serialize_message(messages)
            # Create The json display
            return JsonResponse(display_message, json_dumps_params={'indent': 4}, safe=False)

    @staticmethod
    def show_single_message(request, username):
        if request.method == Methods.GET:
            body = request.body.decode("utf-8")
            body_data = json.loads(body)

            # Implement mark as read functionality
            if body_data[Keys.IS_READ] == "True":
                Message.objects.filter(sender=username, subject=body_data[Keys.SUBJECT]).update(
                    is_read=True) | Message.objects.filter(receiver=username, subject=body_data[Keys.SUBJECT]).update(
                    is_read=True)
            elif body_data[Keys.IS_READ] == "False":
                Message.objects.filter(sender=username, subject=body_data[Keys.SUBJECT]).update(is_read=False) | \
                Message.objects.filter(receiver=username, subject=body_data[Keys.SUBJECT]).update(
                    is_read=False)

            # Show message sent or received
            message = set(Message.objects.filter(sender=username, subject=body_data[Keys.SUBJECT]) |
                          Message.objects.filter(receiver=username, subject=body_data[Keys.SUBJECT]))

            display_message = serialize_message(message)

            if len(display_message) == 0:
                return HttpResponse("No message exists")
            else:
                return JsonResponse(display_message, json_dumps_params={"indent": 4}, safe=False)

    @staticmethod
    def show_unread_messages(request, user_name):
        if request.method == Methods.GET:

            unread_messages = set(Message.objects.filter(sender=user_name, is_read=False) |
                                  Message.objects.filter(receiver=user_name, is_read=False))

            display_message = serialize_message(unread_messages)
            if len(display_message) == 0:
                return HttpResponse("No unread messages")
            else:
                return JsonResponse(display_message, json_dumps_params={"indent": 4}, safe=False)

    @staticmethod
    @csrf_exempt
    def delete_message(request, user_name, subject, type_delete):
        if request.method == Methods.DELETE:
            if type_delete == Keys.SENDER:
                Message.objects.filter(sender=user_name, subject=subject).delete()
                return HttpResponse(f"sender deleted {subject} Message")
            elif type_delete == Keys.RECEIVER:
                Message.objects.filter(receiver=user_name, subject=subject).delete()
                return HttpResponse(f"receiver deleted {subject} Message")
            return HttpResponse("Message Deleted")

    @staticmethod
    @csrf_exempt
    def post_new_message(request):
        if request.method == Methods.POST:
            user_model = get_user_model()
            users = user_model.objects.all()
            # Make sure to upload message to valid users
            if request.POST[Keys.SENDER] in str(users) or request.POST[Keys.RECEIVER] in str(users):
                new_message = Message(sender=request.POST[Keys.SENDER], receiver=request.POST[Keys.RECEIVER],
                                      subject=request.POST[Keys.SUBJECT], message=request.POST[Keys.MESSAGE])
                new_message.save()
                return HttpResponse(f"Message to {request.POST[Keys.RECEIVER]} has been sent!")
            else:
                return HttpResponse("Message not sent, check sender and receiver")
