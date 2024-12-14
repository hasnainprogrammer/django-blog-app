from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse
from posts.models import Post
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        # Getting user supplied data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # checking user supplied data
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username already exits')
                return redirect('register')
                # return HttpResponse('That username already exits')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'That email address is already been taken')
                return redirect('register')
                # return HttpResponse('That email address is already been taken')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Successfully Registered!')
                return redirect('register')
                # return HttpResponse('Successfully Regitered!')
        else:
                messages.error(request, 'Passwords should match!')
                return redirect('register')

                # return HttpResponse('Passwords should match!')

    return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        # Getting user supplied data
         username = request.POST['username']
         password = request.POST['password']

        # user authentication
         user = auth.authenticate(username=username, password=password)
         if user is not None:
              auth.login(request, user)
              messages.success(request, 'Login Successfull!')
              return redirect('index')
         else:
            messages.error(request, 'Login Failed!')
            return redirect('login')
              
    return render(request, 'accounts/login.html')

def logout(request):
    # logged out a user
    auth.logout(request)
    messages.success(request, 'Logout Successfull!')
    return redirect('login')

def dashboard(request):
    # check if user is logged in
    if request.user.is_authenticated:
        # updating user profile
        logged_in_user = User.objects.get(id=request.user.id)
        context = {'logged_in_user': logged_in_user}
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            logged_in_user.username = username
            logged_in_user.email = email
            logged_in_user.save()
            # return HttpResponse('Profile Updated Successfully!')
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('dashboard')
        return render(request, 'accounts/dashboard.html', context)
    else:
        return redirect('login')
    
def user_created_posts(request):
    # delete a post
    if 'delete' in request.GET:
        if request.GET['delete'] == 'true':
            post = Post.objects.get(id=request.GET['postid'])
            post.delete()
            messages.success(request, 'Post Deleted Successfully!')
            return redirect('user_created_posts')
            # return HttpResponse('Post Deleted Successfully!')
         
    # displaying user created posts
    user_posts = Post.objects.order_by('-publish_date').filter(user_id=request.user.id)
    context = {'user_posts': user_posts}
    return render(request, 'accounts/user_created_posts.html', context)

def edit_post(request, post_id):
    # edit a post
    single_post = Post.objects.get(id=post_id)
    # if 'post-image' in request.GET and 'post-title' in request.GET and 'post-body' in request.GET:
    #         if request.GET['post-image'] == '' or request.GET['post-title'] == '' or request.GET['post-body'] == '':
    #             messages.error(request, 'Failed to Update the Post! Make sure you fill all the fields')
    #             return redirect('user_created_posts')
    #             # return HttpResponse('Failed to Post! Make sure you fill all the fields')
    #         else:
    #             post_image = request.GET['post-image']
    #             post_title = request.GET['post-title']
    #             post_body = request.GET['post-body']
    #             single_post.image = post_image
    #             single_post.title = post_title
    #             single_post.body = post_body
    #             single_post.save()
    #             messages.success(request, 'Post Updated Successfully!')
    #             return redirect('user_created_posts')
                # return HttpResponse('Post Updated Successfully!')
    if request.method == 'POST':
        post_title = request.POST['post-title']
        post_body = request.POST['post-body']
        if post_title == '' or post_body == '':
            return HttpResponse('Fill the fields')
        else:   
            post_image = request.FILES['post-image']
            single_post.image = post_image
            single_post.title = post_title
            single_post.body = post_body
            single_post.save()
            messages.success(request, 'Post Updated Successfully!')
            return redirect('user_created_posts')

    context = {'single_post': single_post}
    return render(request, 'accounts/editpost.html', context)