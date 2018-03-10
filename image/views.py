from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.core.management import call_command


import json
import hashlib
import random
from io import StringIO
from .models import *
from .form import *
from .verify import google_verify_image

import time


# Create your views here.
def index(request):
    image_list = Image.objects.filter(legal=True).order_by("-pub_date")
    paginator = Paginator(image_list, 10)
    page = request.GET.get('page', 1)
    try:
        images = paginator.page(page)
    except:
        return JsonResponse({'meta': {'length': 0}}, safe=False)
    id2original = {}
    for image in images:
        id2original[image.id] = image.original_url
    if page == 1:
        context = {
                'images': images,
                'page': page,
                'accept_terms': 'false',
                'id2original': json.dumps(id2original),
                'img_per_line': request.session.get("img_per_line", 3),
                'night_mode': request.session.get("night_mode", 'false'),
                'accept_terms': request.session.get("accept_terms", 'false'),
                'username': request.session.get('username', ''),
                }
        return render(request, 'image/image_list.html', context) 
    else:
        images_json = []
        id2original = {}
        for image in images:
            image_json = {}
            image_json['id'] = image.id
            image_json['thumbnail_url'] = image.thumbnail_url
            image_json['oo_num'] = image.oo_num
            image_json['xx_num'] = image.xx_num
            image_json['comment_num'] = image.comment_num
            image_json['name'] = image.name
            image_json['pub_date'] = image.pub_date
            image_json['credit_url'] = image.credit_url
            images_json.append(image_json)
            id2original[image.id] = image.original_url
        meta = {}
        meta['length'] = len(images)
        context_json = {'images': images_json, 'id2original': id2original, 'meta': meta}
        return JsonResponse(context_json, safe=False)
def validate_ooxx(request):
    image_id = request.GET.get('image_id', None)
    if request.session.get('%s_has_voted'%image_id, False):
        return HttpResponse('你已经投过票了')
    request.session['%s_has_voted'%image_id] = True
    image = Image.objects.get(id=image_id)
    if request.GET['attitude'] == 'oo':
        image.oo_num += 1
        vote = Vote(image_id=image, vote_time=timezone.now())
        vote.save()
    else:
        image.xx_num += 1
    image.save()
    return HttpResponse('Success')


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
            return HttpResponse('昵称不可为空')
        if request.POST['content'] == '':
            return HttpResponse('内容不可为空')
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
        # TODO validate comment
        comment.legal = True
        comment.save()
        return HttpResponse('Success')
    else:
        pass

def validate_comment_ooxx(request):
    comment_id = request.GET.get('comment_id', None)
    if request.session.get('%s_has_voted'%comment_id, False):
        return HttpResponse('你已经投过票了')
    request.session['%s_has_voted'%comment_id] = True
    comment = Comment.objects.get(id=comment_id)
    if request.GET['attitude'] == 'oo':
        comment.oo_num += 1
    else:
        comment.xx_num += 1
    comment.save()
    return HttpResponse('Success')

def set_preference(request):
    img_per_line = request.GET.get('img_per_line', False)
    if img_per_line:
        request.session['img_per_line'] = img_per_line
    night_mode = request.GET.get('night_mode', False)
    if night_mode:
        request.session['night_mode'] = str(night_mode).lower()
    accept_terms = request.GET.get('accept_terms', False)
    if accept_terms:
        request.session['accept_terms'] = 'true'
    username = request.GET.get('username', '')
    if username != '':
        request.session['username'] = username
    return HttpResponse('Success')

def add_image(request):
    name = request.POST.get('name', False)
    if not name:
        return JsonResponse({'result': "请填写昵称！", 'image_id': -1})
    url = request.POST.get('url', False)
    if url:
        try:
            out = StringIO()
            call_command('addusercaturl', url, name, stdout=out)
            new_image_id = out.getvalue().split('.')[1]
        except Exception as e:
            return JsonResponse({'result': str(e), 'image_id': -1})
        return JsonResponse({'result': "添加成功！请耐心等待审核。", 'image_id': new_image_id})
    filename = request.POST.get('filename', False)
    if filename:
        ext = filename.split('.')[-1].strip().lower()
        filename = '/dev/shm/' + hashlib.md5(str(random.random()).encode()).hexdigest() + '.' + ext
        img = request.FILES['file']
        with open(filename, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
        try:
            out = StringIO()
            call_command('addusercatfile', filename, name, stdout=out)
            new_image_id = out.getvalue().split('.')[1]
        except Exception as e:
            return JsonResponse({'result': str(e), 'image_id': -1})
        return JsonResponse({'result': "添加成功！请耐心等待审核。", 'image_id': new_image_id})
    return JsonResponse({'result': "请填写URL或上传文件！", 'image_id': -1})

def review(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            try:
                image_for_review = Image.objects.filter(legal=False)[0]
            except IndexError:
                return HttpResponse("Nothing to review now.")
            context = {
                    'image_for_review': image_for_review,
                    }
            return render(request, 'image/review.html', context)
        else:
            image_id = request.POST['image_id']
            attitude = request.POST['attitude']
            image = Image.objects.get(id=image_id)
            if attitude == 'pass':
                image.legal = True
                image.save()
            elif attitude == 'kill':
                image.delete()
            return HttpResponse('Success')
    else:
        return redirect('index')

def recycle(request):
    return HttpResponse("recycle")

def verify_image(request):
    image_id = request.GET.get('image_id', -1)
    image_id = int(image_id)
    if image_id != -1:
        image = Image.objects.get(id=image_id)
        print('image:', image.original_url)
        result = google_verify_image(image.original_url)
        #result = 0
        if result == -1:
            image.legal = False
            image.save()
            return HttpResponse('您于%s上传的图片疑似含有敏感信息，请等待人工审核。'%image.pub_date)
        elif result == -2:
            image.legal = False
            image.save()
            return HttpResponse('您于%s上传的图片似乎不是猫图，请等待人工审核。'%image.pub_date)
        else:
            image.legal = True
            image.save()
            return HttpResponse('您于%s上传的图片通过审核。'%image.pub_date)
    else:
        return HttpResponse('不要捣乱哦 喵')
