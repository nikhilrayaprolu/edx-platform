from django.dispatch import Signal

send_notification_single_user = Signal(providing_args=['user', 'notification'])
send_notification_multi_user = Signal(providing_args=['users', 'notification'])