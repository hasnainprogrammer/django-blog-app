from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Post, Comment
from django.shortcuts import get_object_or_404
from .forms import Form
from django.core.paginator import Paginator

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
    # if 'post-image' in request.GET and 'post-title' in request.GET and 'post-body' in request.GET:
    #     if request.GET['post-image'] == '' or request.GET['post-title'] == '' or request.GET['post-body'] == '':
    # if request.method == "POST":
    #     if request.POST['post-title'] == '' or request.POST['post-body'] == '':
    #         return HttpResponse('Failed to Post! Make sure you fill all the fields')
    # else:
    #   # user_id = request.user.id
        # post_image = request.GET['post-image']
        # post_title = request.GET['post-title']
        # post_body = request.GET['post-body']
        # post = Post(user_id_id=user_id, image=post_image, title=post_title, body=post_body)
        # post.save()
        # print(request.POST) 
        # -------------------------------------------   
    #     form = Form(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponse('Posted Successfully!')
    # form = Form()
    # context = {'form': form}
    # -----------------------------------------------
    if request.method == 'POST':
        user_id = request.user.id
        post_title = request.POST['post-title']
        post_body = request.POST['post-body']
        if post_title == '' or post_body == '':
            return HttpResponse('Fill the fields')
        else:   
            print(request.FILES)
            post_image = request.FILES['post-image']
            post = Post(user_id_id=user_id, image=post_image, title=post_title, body=post_body)
            post.save()
            return HttpResponse('Posted Successfully!')
    # -----------------------------------------------
    
    return render(request, 'posts/makepost.html')

def post(request, post_id):
    if 'comment-text' in request.GET:
        if request.user.is_authenticated:
            if request.GET['comment-text'] == '':
                return HttpResponse('COMMENT FIELD SHOULD NOT BE EMPTY!')
            else:
                user_id = request.user.id
                comment_text = request.GET['comment-text']
                comment = Comment(user_id_id=user_id, post_id_id=post_id, comment_text=comment_text)
                comment.save()
                return HttpResponse('Commented Successfully!')
        else:
            return HttpResponse('Login to Comment!')
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
            return HttpResponse('Type Something on the search field')
    return render(request, 'posts/search.html', context)