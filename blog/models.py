from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# Post Model
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    # return title
    def __str__(self):
        return self.title
    
    # get likes
    def get_like_count(self):
        return self.likes.count()
    
    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    def get_comment_count(self):
        return self.comments.filter(approved=True).count()
    
# Comment Model
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_date']
        
        def __str__(self):
            return f'Comment by {self.author.username} on {self.post.title}'

# Like Model        
class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user') # Prevent duplicate likes
        
    def __str__(self):
        return f'{self.user.username} likes {self.post.title}'

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_post_count(self):
        return self.posts.filter(published_date__isnull=False).count()