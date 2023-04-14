from django import forms
from .models import Post,Comment
from django_summernote.widgets import SummernoteWidget
# 글을 작성하는 폼입니다. 위젯으로 작성공간 만들어줬습니다.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post', 'photo', 'tags',]
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control mt-2'}),
        'post': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        'photo': forms.ClearableFileInput(attrs={'class': 'form-control mt-2'}),
        'tags' : forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': '콤마(,)로 구분해주세요'}),
        }
        labels = {
            'title': '제목',
            'post': '내용',
            'photo': '사진',
            'tags': '태그',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}),
        }
