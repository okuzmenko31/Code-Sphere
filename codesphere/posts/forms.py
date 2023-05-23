from django import forms
from .models import Posts
from tags.models import Tags
from ckeditor.widgets import CKEditorWidget


class CreatePostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(label='Tags',
                                          queryset=Tags.objects.all(),
                                          widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Posts
        fields = ('title', 'short_description', 'text', 'tags', 'cover_photo')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': CKEditorWidget(),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_photo': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tags.objects.all()

        if 'tags' in self.data:
            self.fields['tags'].queryset = Tags.objects.all()
