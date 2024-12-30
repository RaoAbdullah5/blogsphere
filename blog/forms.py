from django import forms
from .models import Comment , Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'description']  # Adjust according to your model fields

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
