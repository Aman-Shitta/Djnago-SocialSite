from django import forms
from .models import Post, Comment

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'row':2}))
    class Meta:
        model = Post
        fields = (
            'content',
            'image'
        )
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label="", widget=(forms.TextInput(attrs={'placeholder':"Add Comment..."})))
    class Meta:
        model = Comment
        fields = (
            'body',
        )