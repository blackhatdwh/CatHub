from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from image.models import Image
import sys
import hashlib
from .search import search
from .thumbnail import convert
from .upload2weibo import upload
import subprocess

# search, wget, gif2jpg, upload2weibo
class Command(BaseCommand):
    help = 'add a new cat'

    def add_arguments(self, parser):
        parser.add_argument('filename&name', nargs='+', type=str) 

    def handle(self, *args, **options):
        filename = options['filename&name'][0]
        name = options['filename&name'][1]
            
        # generate thumbnail
        thumbnail_filename = convert(filename)
        if  thumbnail_filename != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to convert.'))
            raise CommandError('无法解析该图片')

        # upload2weibo
        original_url = upload(filename)
        if original_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload gif.'))
            raise CommandError('无法上传原图到微博图床')

        thumbnail_url = upload(thumbnail_filename)
        if thumbnail_url != -1:
            pass
        else:
            self.stderr.write(self.style.ERROR('Fail to upload jpg.'))
            raise CommandError('无法上传缩略图到微博图床')

        new_cat = Image(name=name, original_url=original_url, thumbnail_url=thumbnail_url, pub_date=timezone.now(), oo_num=0, xx_num=0, comment_num=0)
        new_cat.save()
        subprocess.getoutput('rm '+filename)
        subprocess.getoutput('rm '+thumbnail_filename)

        self.stdout.write(self.style.SUCCESS('.%s.'%new_cat.id))
