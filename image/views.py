from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.management import call_command


import json
import hashlib
import random
from .models import *
from .form import *


# Create your views here.
def index(request):
    image_list = Image.objects.all().order_by("-pub_date")
    paginator = Paginator(image_list, 25)
    page = request.GET.get('page')
    images = paginator.get_page(page)
    id2original = {}
    for image in images:
        id2original[image.id] = image.original_url
    
    context = {
            'images': images,
            'id2original': json.dumps(id2original),
            'img_per_line': request.session.get("img_per_line", 3),
            'night_mode': request.session.get("night_mode", False),
            }
    return render(request, 'image/image_list.html', context) 
def validate_ooxx(request):
    image_id = request.GET.get('image_id', None)
    if request.session.get('%s_has_voted'%image_id, False):
        return JsonResponse({'result': '你已经投过票了'})
    request.session['%s_has_voted'%image_id] = True
    image = Image.objects.get(id=image_id)
    if request.GET['attitude'] == 'oo':
        image.oo_num += 1
        vote = Vote(image_id=image, vote_time=timezone.now())
        vote.save()
    else:
        image.xx_num += 1
    image.save()
    return JsonResponse({'result': 'Success'})


def get_comment(request):
    image_id = request.GET.get('image_id', None)
    comments = Comment.objects.filter(image_id=image_id)
    response = []
    for comment in comments:
        try:
            reply_to = comment.reply_to.id
        except AttributeError:
            reply_to = None
        c = {
                'comment_id': comment.id,
                'name': comment.name,
                'content': comment.content,
                'pub_date': comment.pub_date,
                'oo_num': comment.oo_num,
                'xx_num': comment.xx_num,
                'reply_to': reply_to,
            }
        response.append(c)
    return JsonResponse(response, safe=False)

def add_comment(request):
    if request.method == 'POST':
        if request.POST['name'] == '':
            return JsonResponse({'result': '昵称不可为空'})
        if request.POST['content'] == '':
            return JsonResponse({'result': '内容不可为空'})
        image = Image.objects.get(id=request.POST['image_id'])
        image.comment_num += 1
        image.save()
        if request.POST['reply_to'] == '':
            reply_to = None
            content_prefix = ''
        else:
            reply_to = Comment.objects.get(id=request.POST['reply_to'])
            content_prefix = '回复<b class="user">%s</b>：' % reply_to.name
        comment = Comment(
                image_id = image,\
                name = request.POST['name'],\
                content = content_prefix + request.POST['content'],\
                pub_date = timezone.now(),\
                oo_num = 0,\
                xx_num = 0,\
                reply_to = reply_to,\
                )
        comment.save()
        return JsonResponse({'result': 'Success'})
    else:
        pass

def validate_comment_ooxx(request):
    comment_id = request.GET.get('comment_id', None)
    if request.session.get('%s_has_voted'%comment_id, False):
        return JsonResponse({'result': '你已经投过票了'})
    request.session['%s_has_voted'%comment_id] = True
    comment = Comment.objects.get(id=comment_id)
    if request.GET['attitude'] == 'oo':
        comment.oo_num += 1
    else:
        comment.xx_num += 1
    comment.save()
    return JsonResponse({'result': 'Success'})

def set_preference(request):
    img_per_line = request.GET.get('img_per_line', False)
    if img_per_line:
        request.session['img_per_line'] = img_per_line
    night_mode = request.GET.get('night_mode', False)
    if night_mode:
        request.session['night_mode'] = night_mode
    return JsonResponse({'result': 'Success'})

def add_image(request):
    name = request.POST.get('name', False)
    if not name:
        return HttpResponse("请填写昵称！")
    url = request.POST.get('url', False)
    if url:
        call_command('addusercaturl', url, name)
        return HttpResponse("添加成功！请耐心等待审核。")
    filename = request.POST.get('filename', False)
    if filename:
        ext = filename.split('.')[-1].strip().lower()
        filename = '/dev/shm/' + hashlib.md5(str(random.random()).encode()).hexdigest() + '.' + ext
        img = request.FILES['file']
        with open(filename, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
        call_command('addusercatfile', filename, name)
        return HttpResponse("添加成功！请耐心等待审核。")
    return HttpResponse("请填写URL或上传文件！")



