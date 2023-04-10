from django import forms
from .models import Comment
from mdeditor.fields import MDTextFormField


class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': MDTextFormField()
        }
        labels = {
            'text': 'Your comment'
        }
