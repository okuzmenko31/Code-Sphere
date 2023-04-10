from django import forms
from .models import Comment


class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control',
                                          'rows': 4})
        }
        labels = {
            'text': 'Your comment'
        }
