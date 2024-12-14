from django.shortcuts import render
from posts.models import Post

def index(request):
    posts = Post.objects.order_by('-publish_date')
    context = {
        'posts': posts
    }
    
    return render(request, 'pages/index.html', context)