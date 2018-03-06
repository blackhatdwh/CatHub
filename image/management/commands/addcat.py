from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from image.models import Image
import sys
from .search import search
from .gif2jpg import gif2jpg
from .upload2weibo import upload
import subprocess

# search, wget, gif2jpg, upload2weibo
class Command(BaseCommand):
    help = 'add a new cat'

    def handle(self, *args, **options):
        # search
        url = search('cat')
        try:
            subprocess.getoutput('rm new_cat.gif')
            subprocess.getoutput('rm new_cat.jpg')
        except:
            pass

        # wget
        try:
            subprocess.getoutput('wget %s -O new_cat.gif'%url)
        except:
            self.stderr.write(self.style.ERROR('Fail to download. URL: %s'%url))
            sys.exit()
            
        # gif2jpg
        if gif2jpg() != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to convert.'))
            sys.exit()

        # upload2weibo
        gif_url = upload('new_cat.gif')
        if gif_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload gif.'))

        jpg_url = upload('new_cat.jpg')
        if jpg_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload jpg.'))

        new_cat = Image(name='CatHub', gif_url=gif_url, still_url=jpg_url, pub_date=timezone.now(), oo_num=0, xx_num=0, comment_num=0)
        new_cat.save()

        self.stdout.write(self.style.SUCCESS('Successfully add a cat.'))
