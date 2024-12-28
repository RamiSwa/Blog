from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Category, Tag, Comment
from .forms import CommentForm

def home(request):
    posts = Post.objects.filter(status=Post.PUBLISHED).order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.PUBLISHED)
    post.views += 1
    post.save()

    related_posts = post.get_related_posts()
    comments = post.comments.filter(approved=True)  # Fetch only approved comments
    form = CommentForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('blog:post_detail', slug=post.slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
        'form': form,
    })

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.PUBLISHED).order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

def tag_posts(request, name):
    tag = get_object_or_404(Tag, name=name)
    posts = tag.posts.filter(status=Post.PUBLISHED).order_by('-created_at')
    return render(request, 'blog/tag_posts.html', {'tag': tag, 'posts': posts})

@login_required
def like_post(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({'likes_count': post.like_count()})
    return HttpResponseBadRequest('Invalid request method.')

@login_required
def dislike_post(request, id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
        return JsonResponse({'dislikes_count': post.dislike_count()})
    return HttpResponseBadRequest('Invalid request method.')
