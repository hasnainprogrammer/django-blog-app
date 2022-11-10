from django.shortcuts import render
from blog_app.models import Blog

# Create your views here.
def index(request):
    myposts = Blog.objects.all()[:5]
    context = {
        'posts': myposts,
    }
    return render(request,'index.html', context)
def details(request,id):
    myposts = Blog.objects.get(id=id)
    return render(request,'details.html',{'post': myposts})
def posts(request):
    myposts = Blog.objects.all()[:5]
    context = {
        'posts': myposts,
    }
    return render(request,'index.html', context)
