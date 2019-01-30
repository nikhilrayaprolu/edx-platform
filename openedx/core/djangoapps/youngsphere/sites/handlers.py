from django.dispatch import receiver

from openedx.core.djangoapps.youngsphere.sites.models import Notification, UnReadNotificationCount
from openedx.core.djangoapps.youngsphere.sites.signals import send_notification_single_user, \
    send_notification_multi_user
from fcm_django.models import FCMDevice

@receiver(send_notification_single_user)
def send_notification_single(sender, **kwargs):  # pylint: disable=unused-argument
    user_id = kwargs['user']
    notification = kwargs['notification']
    device = FCMDevice.objects.filter(user=user_id)
    addNotification(user_id, notification)
    device.send_message(title=notification['title'], body=notification['body'], icon=notification['icon'], data=notification['data'])


@receiver(send_notification_multi_user)
def send_notification_single(sender, **kwargs):  # pylint: disable=unused-argument
    user_ids = kwargs['users']
    notification = kwargs['notification']
    devices = FCMDevice.objects.filter(user__in=user_ids)
    for user_id in user_ids:
        addNotification(user_id, notification)
    devices.send_message(title=notification['title'], body=notification['body'], icon=notification['icon'], data=notification['data'])

def addNotification(user_id, notification):
    Notification(user_id = user_id, notification = notification)
    Notification.save()
    UnReadNotificationCount(user_id = user_id).increment()

