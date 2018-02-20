from django import forms
from django.forms import ModelForm
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'content']
        widgets = {
                'image_id': forms.HiddenInput(),
                'name': forms.TextInput(),
                'content': forms.Textarea(),
                'pub_date': forms.HiddenInput(),
                'oo_num': forms.HiddenInput(),
                'xx_num': forms.HiddenInput(),
                'reply_to': forms.HiddenInput(),
                }
        labels = {
                'name': '昵称',
                'content': '内容',
                }

