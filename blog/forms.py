from django import forms

from .models import Post, Comment, Tag

# Post Form
class PostForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select relevant tags for your post"
    )
    
    class Meta:
        model = Post
        fields = ('title', 'text', 'tags')
        
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

# Search Form for searching posts
class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...',
            'type': 'search'
        }),
        label=''
    )
    
# Tag Form for creating tags
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tag name...'
            })
        }