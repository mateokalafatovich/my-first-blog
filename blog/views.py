from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils.text import slugify
from .models import Post, Comment, Like, Tag
from .forms import PostForm, CommentForm, SearchForm, TagForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    search_form = SearchForm()
    tags = Tag.objects.all()
    
    # Handle search
    query = request.GET.get('query')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        search_form = SearchForm(initial={'query': query})
    
    # Handle tag filtering
    tag_slug = request.GET.get('tag')
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)

    context = {
        'posts': posts,
        'search_form': search_form,
        'tags': tags,
        'selected_tag': selected_tag,
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)

# View to handle posts and their comments
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(approved=True)
    comment_form = CommentForm()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', pk=post.pk)
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': post.is_liked_by(request.user),
        'like_count': post.get_like_count()
    }
    
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form}) 

# View for handling like/unlike functionality
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        # If like already exists, remove it (unlike)
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request
        return JsonResponse({
            'liked': liked,
            'like_count': post.get_like_count()
        })
    
    return redirect('post_detail', pk=post.pk)

# Dedicate search view
def search_posts(request):
    form = SearchForm()
    posts = Post.objects.none()
    query = None
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Post.objects.filter(
                Q(title__icontains=query) | 
                Q(text__icontains=query) |
                Q(tags__name__icontains=query),
                published_date__isnull=False
            ).distinct().order_by('-published_date')
    
    context = {
        'form': form,
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search_results.html', context)

# View posts filtered by a specific tag
def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        tags=tag, 
        published_date__isnull=False
    ).order_by('-published_date')
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/posts_by_tag.html', context)
