from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from notification.models import Notification
from room.models import RoomJoining
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.core import serializers
# Create your views here.

@login_required
def get_notification(request):
    if request.method == 'GET':
        new_notification = Notification.objects.filter(receiver_id=request.user.user_id,verified=False).order_by('created_at').reverse()
        post_list = serializers.serialize('json', new_notification)
        return HttpResponse(post_list, content_type="text/json-comment-filtered")


@login_required
def checked_notification(request):
    if request.method == 'GET':
        checked_notification = []
        for notification in Notification.objects.filter(receiver_id = request.user.user_id,verified = False):
            notification.verified = True
            checked_notification.append(notification)
        Notification.objects.bulk_update(checked_notification, fields=['verified'])
        return HttpResponse('')
