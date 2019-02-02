""" Django Sites framework models overrides """
from django.conf import settings
from django.contrib.auth.models import User
#from django.core.cache import caches
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http.request import split_domain_port
#from django.contrib.sites.models import Site, SiteManager, SITE_CACHE
from django.core.exceptions import ImproperlyConfigured
from jsonfield import JSONField
from organizations.models import Organization
import django

# cache = caches['general']
#
#
# def _cache_key_for_site_id(site_id):
#     return 'site:id:%s' % (site_id,)
#
#
# def _cache_key_for_site_host(site_host):
#     return 'site:host:%s' % (site_host,)
#
#
# def patched_get_site_by_id(self, site_id):
#     key = _cache_key_for_site_id(site_id)
#     site = cache.get(key)
#     if site is None:
#         site = self.get(pk=site_id)
#         SITE_CACHE[site_id] = site
#     cache.add(key, site)
#     return site
#
#
# def patched_get_site_by_request(self, request):
#
#     host = request.get_host()
#     key = _cache_key_for_site_host(host)
#     site = cache.get(key)
#     if site is None:
#         try:
#             # First attempt to look up the site by host with or without port.
#             site = self.get(domain__iexact=host)
#         except Site.DoesNotExist:
#             # Fallback to looking up site after stripping port from the host.
#             domain, port = split_domain_port(host)
#             if not port:
#                 raise
#             site = self.get(domain__iexact=domain)
#         SITE_CACHE[host] = site
#     cache.add(key, site)
#     return site
#
#
# def patched_clear_cache(self):
#     keys_id = [_cache_key_for_site_id(site_id) for site_id in SITE_CACHE]
#     keys_host = [_cache_key_for_site_host(site_host) for site_host in SITE_CACHE]
#     cache.delete_many(keys_id + keys_host)
#     SITE_CACHE.clear()
#
#
# def patched_clear_site_cache(sender, **kwargs):
#     """
#     Clears the cache (if primed) each time a site is saved or deleted
#     """
#     instance = kwargs['instance']
#     site = instance.site
#     key_id = _cache_key_for_site_id(site.pk)
#     key_host = _cache_key_for_site_host(site.domain)
#     cache.delete_many([key_id, key_host])
#     try:
#         del SITE_CACHE[site.pk]
#     except KeyError:
#         pass
#     try:
#         del SITE_CACHE[site.domain]
#     except KeyError:
#         pass
#
#
# class AlternativeDomain(models.Model):
#     site = models.OneToOneField(Site, related_name='alternative_domain')
#     domain = models.CharField(max_length=500)
#
#     def __unicode__(self):
#         return self.domain
#
#     def switch_with_active(self):
#         """
#         Switches the currently active site with the alternative domain (custom or default) and saves
#         the currently active site as the alternative domain.
#         """
#         current_domain = self.site.domain
#         self.site.domain = self.domain
#         self.domain = current_domain
#         self.site.save()
#         self.save()
#
#     def is_tahoe_domain(self):
#         """
#         Checks if the domain is the default Tahoe domain and not a custom domain
#         :return:
#         """
#         return settings.LMS_BASE in self.domain

class School(models.Model):
    organization = models.OneToOneField(Organization, related_name='school_profile')
    schoolname = models.CharField(max_length=50, blank=True, null=True)
    principal = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=20, blank=True, null=True)
    board = models.CharField(max_length=20, blank=True, null=True)
    schoollogo = models.ImageField(blank=True, upload_to='school_logo', default='school_logo/no-image.jpg')

class Class(models.Model):
    organization = models.ForeignKey(Organization)
    class_level = models.CharField(max_length=5)
    display_name = models.CharField(max_length=10)
    num_sections = models.IntegerField(default=0)

class Section(models.Model):
    section_class = models.ForeignKey(Class)
    section_name = models.CharField(max_length=5)
    description = models.CharField(max_length=144, blank=True, null=True)

class Course(models.Model):
    organization = models.ForeignKey(Organization)
    course_class = models.ForeignKey(Class)
    course_section = models.ForeignKey(Section)
    course_name = models.CharField(max_length=50)
    description = models.CharField(max_length=144, blank=True, null=True)
    year = models.IntegerField(default=2020)
    course_id = models.CharField(max_length=80, blank=True, null=True)
    course_status = models.CharField(max_length=3, blank=True, null=True)

class UserMiniProfile(models.Model):
    user = models.ForeignKey(User, related_name='mini_user_profile')
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    contact_number = models.CharField(max_length=40, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True)
    school = models.ForeignKey(School,blank = True,null=True)

class UserSectionMapping(models.Model):
    user = models.ForeignKey(User, related_name='section')
    section = models.ForeignKey(Section)

class Notification(models.Model):
    user_id = models.ForeignKey(User)
    notification =JSONField(
        null=True,
        blank=True,
    )

class UnReadNotificationCount(models.Model):
    user_id = models.ForeignKey(User, primary_key=True)
    unread_count = models.IntegerField(default=0)

    def increment(self):
        self.unread_count += 1
        self.save()

    def zero(self):
        self.unread_count = 0
        self.save()

class Device(models.Model):
    device_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    active = models.BooleanField(
        default=True,
        help_text="Inactive devices will not be sent notifications"
    )
    user = models.ForeignKey(User, blank=True, null=True,
                             on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True
    )

    class Meta:
        abstract = True



# @receiver(post_save, sender=AlternativeDomain)
# def delete_alternative_domain_cache(sender, instance, **kwargs):
#     if instance.site.domain.endswith(settings.SITE_NAME):
#         cache_key_site = instance.site.domain
#     else:
#         cache_key_site = instance.domain
#
#     cache_key = '{prefix}-{site}'.format(
#         prefix=settings.CUSTOM_DOMAINS_REDIRECT_CACHE_KEY_PREFIX,
#         site=cache_key_site
#     )
#     cache.delete(cache_key)
#
# django.contrib.sites.models.clear_site_cache = patched_clear_site_cache
# SiteManager.clear_cache = patched_clear_cache
# SiteManager._get_site_by_id = patched_get_site_by_id  # pylint: disable=protected-access
# SiteManager._get_site_by_request = patched_get_site_by_request  # pylint: disable=protected-access
