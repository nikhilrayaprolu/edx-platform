from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
import stream
from django.conf import settings

from student.models import CourseEnrollment
from openedx.core.djangoapps.youngsphere.sites.models import Course, Page, School, UserMiniProfile

send_notification_single_user = Signal(providing_args=['user', 'notification'])
send_notification_multi_user = Signal(providing_args=['users', 'notification'])

client = stream.connect(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)


@receiver(post_save, sender = UserMiniProfile)
def new_stream_user(sender, instance, **kwargs):
    user_page, created = Page.objects.get_or_create(pageid=instance.user.username, ownertype='user')
    if instance.page_id != user_page:
        instance.page_id = user_page
        instance.save(update_fields=['page_id'])
    try:
        client.users.add(
            instance.user.username,
            {"name": (instance.first_name or '') + ' ' + (instance.last_name or '')
             },
        )
    except:
        print((instance.first_name or '') + ' ' + (instance.last_name or ''))
        client.users.update(
            instance.user.username,
            {"name": (instance.first_name or '') + ' ' + (instance.last_name or '')
             },
        )

    follows = []
    pageobject = {
        'source': 'timeline:' + instance.user.username,
        'target': 'user:' + instance.user.username,
    }
    follows.append(pageobject)
    pageobject = {
        'source': 'timeline:' + instance.user.username,
        'target': 'school:' + instance.school.page_id.pageid,
    }
    follows.append(pageobject)
    client.follow_many(follows)


@receiver(post_save, sender = Course)
def new_stream_course(sender, instance, **kwargs):
    if not instance.page_id:
        course_page, created = Page.objects.get_or_create(
            pageid=str(instance.course_id.replace('+', '-').replace(':', '-')), ownertype='course')
        print("course_page being printed", course_page, created)
        instance.page_id = course_page
        instance.save(update_fields=['page_id'])

@receiver(post_save, sender = School)
def new_stream_school(sender, instance, **kwargs):
    school_page, created = Page.objects.get_or_create(pageid=instance.organization.short_name, ownertype='school')
    if instance.page_id != school_page:
        instance.page_id = school_page
        instance.save(update_fields=['page_id'])

@receiver(post_save, sender = CourseEnrollment)
def new_stream_course_follow(sender, instance, **kwargs):
    user = instance.user.username
    course_id = instance.course
    follows = []
    pageobject = {
        'source': 'user:' + user,
        'target': 'course:' + str(course_id.id).replace('+','-').replace(':','-'),
    }
    follows.append(pageobject)
    client.follow_many(follows)


