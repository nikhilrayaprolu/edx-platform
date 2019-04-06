import logging

from django.conf import settings
from django.core.management import BaseCommand

from openedx.core.djangoapps.youngsphere.sites.models import Page, GlobalGroup

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates a Global Group, and then go to admin panel to add further details required (group description, group image, group long name)"

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='*')

    def handle(self, *args, **options):
        for group_name in options['name']:
            new_page = Page(pageid=group_name, ownertype='globalgroup')
            new_page.save()
            global_group_name = GlobalGroup(name=group_name, description='', pageid=new_page)
            global_group_name.save()
