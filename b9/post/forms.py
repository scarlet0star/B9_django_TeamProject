from django import forms
from .models import Post,Comment
# 글을 작성하는 폼입니다. 위젯으로 작성공간 만들어줬습니다.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'post', 'photo')
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control mt-2'}),
        'post': forms.Textarea(attrs={'class': 'form-control mt-2', 'rows' : 10}),
        'photo': forms.ClearableFileInput(attrs={'class': 'form-control mt-2'})
        }
        labels = {
            'title': '제목',
            'post': '내용',
            'photo': '사진',
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    
    class Meta:
        model = Comment
        fields = ['content']