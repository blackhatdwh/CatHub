from django.core.management.base import BaseCommand, CommandError
from image.models import *

class Command(BaseCommand):
    help = 'add a new cat'

    def handle(self, *args, **options):
        print('fuck')
        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % 'haha'))
