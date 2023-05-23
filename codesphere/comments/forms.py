from django import forms
from .models import Comment
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': CKEditorUploadingWidget()
        }
        labels = {
            'text': 'Your comment'
        }
