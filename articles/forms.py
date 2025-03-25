from django.forms import ModelForm
from django import forms
from .models import Article, Comment

class ArticleForm(ModelForm):
    title = forms.CharField(
        widget = forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta():
        model = Article
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }

class CommentForm(ModelForm):
    class Meta():
        model = Comment
        # fields = '__all__'
        # fields = ('content', ) # 추가할 필드 목록

        exclude = ('article', ) # 제외할 필드 목록