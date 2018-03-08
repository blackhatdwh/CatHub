from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from image.models import Image
import sys
from .search import search
from .thumbnail import convert
from .upload2weibo import upload
import subprocess
import random
import hashlib

# search, wget, thumbnail, upload2weibo
class Command(BaseCommand):
    help = 'auto add a new cat'

    def handle(self, *args, **options):
        # search
        url = search('cat')
        print(url)

        # wget
        filename = '/dev/shm/' + hashlib.md5(str(random.random()).encode()).hexdigest() + '.gif'
        try:
            subprocess.getoutput('wget %s -O %s'%(url, filename))
        except:
            self.stderr.write(self.style.ERROR('Fail to download. URL: %s'%url))
            sys.exit()
        print('wget finished')
            
        # thumbnail
        thumbnail_filename = convert(filename)
        if thumbnail_filename != -1:
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

        thumbnail_url= upload(thumbnail_filename)
        if thumbnail_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload jpg.'))
            sys.exit()

        new_cat = Image(name='CatHub', original_url=original_url, thumbnail_url=thumbnail_url, pub_date=timezone.now(), oo_num=0, xx_num=0, comment_num=0, legal=True)
        new_cat.save()
        subprocess.getoutput('rm '+filename)
        subprocess.getoutput('rm '+thumbnail_filename)

        self.stdout.write(self.style.SUCCESS('Successfully add a cat.'))
