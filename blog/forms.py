from django import forms

from .models import Post, Comment

# Post Form
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
        
# Comment Form
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            })
        }
        labels = {
            'content': 'Your Comment'
        }