from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from .forms import Form
from django.core.paginator import Paginator
from django.contrib import messages


def posts(request):
    posts = Post.objects.order_by('-publish_date')
    paginator = Paginator(posts, 6)
    try:
        page_number = request.GET['page']
        page_obj = paginator.get_page(page_number)
    except:
        page_obj = paginator.page(paginator.num_pages)
    # context = {
    #     'posts': posts
    # }
    return render(request, 'posts/posts.html', {'page_obj': page_obj})

def makepost(request):
    if request.method == 'POST':
        user_id = request.user.id
        post_title = request.POST['post-title']
        post_body = request.POST['post-body']
        if post_title == '' or post_body == '':
            messages.error(request, 'fill the fields')
        else:   
            print(request.FILES)
            post_image = request.FILES['post-image']
            post = Post(user_id_id=user_id, image=post_image, title=post_title, body=post_body)
            post.save()
            messages.success(request, 'Posted Successfully!')
    # -----------------------------------------------
    
    return render(request, 'posts/makepost.html')

def post(request, post_id):
    if 'comment-text' in request.GET:
        if request.user.is_authenticated:
            if request.GET['comment-text'] == '':
                messages.error(request, 'Comment field should not be left blank!')
            else:
                user_id = request.user.id
                comment_text = request.GET['comment-text']
                comment = Comment(user_id_id=user_id, post_id_id=post_id, comment_text=comment_text)
                comment.save()
                messages.success(request, 'Commented Successfully')
        else:
            messages.error(request, 'Login to Comment')
        
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.order_by('-comment_date').filter(post_id_id=post_id)
    context = {
        'post': post,
        'comments': comments 
    }
    return render(request, 'posts/post.html', context)

def search(request):
    if 'search' in request.GET:
        if request.GET['search'] != '':
            user_search_input = request.GET['search']
            searched_posts = Post.objects.all().order_by('-publish_date').filter(title__icontains=user_search_input)
            context = { 
                'searched_posts': searched_posts
            }
        else:
            messages.error(request, 'Type Something on the search field')
    return render(request, 'posts/search.html', context)