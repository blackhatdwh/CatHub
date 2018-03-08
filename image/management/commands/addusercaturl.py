from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from image.models import Image
import sys
import hashlib
from .search import search
from .thumbnail import convert
from .upload2weibo import upload
import subprocess
import random

# wget, gif2jpg, upload2weibo
class Command(BaseCommand):
    help = 'add a new cat'

    def add_arguments(self, parser):
        parser.add_argument('url&name', nargs='+', type=str) 

    def handle(self, *args, **options):
        url = options['url&name'][0]
        name = options['url&name'][1]
        ext = url.split('.')[-1].lower().strip()
        filename = '/dev/shm/' + hashlib.md5(str(random.random()).encode()).hexdigest() + '.' + ext
        # wget
        try:
            subprocess.getoutput('wget %s -O %s'%(url, filename))
        except:
            self.stderr.write(self.style.ERROR('Fail to download. URL: %s'%url))
            sys.exit()
            
        # generate thumbnail
        thumbnail_filename = convert(filename)
        if  thumbnail_filename != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to convert.'))
            sys.exit()

        # upload2weibo
        original_url = upload(filename)
        if original_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload gif.'))
            sys.exit()

        thumbnail_url = upload(thumbnail_filename)
        if thumbnail_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload jpg.'))
            sys.exit()

        new_cat = Image(name=name, original_url=original_url, thumbnail_url=thumbnail_url, pub_date=timezone.now(), oo_num=0, xx_num=0, comment_num=0)
        new_cat.save()
        subprocess.getoutput('rm '+filename)
        subprocess.getoutput('rm '+thumbnail_filename)

        self.stdout.write(self.style.SUCCESS('Successfully add a cat.'))
