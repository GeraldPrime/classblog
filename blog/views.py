from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from blog import models
from .models import Post,Category
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.paginator import Paginator

from django.db.models import Count


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the username already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return redirect('signup')

        # Check if the email already exists (optional, for unique emails)
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please use a different email.')
            return redirect('signup')

        # Create and save the user
        newUser = User.objects.create_user(username=name, email=email, password=password)
        newUser.first_name = first_name
        newUser.last_name = last_name
        newUser.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('signin')

    return render(request, 'blogs/signup.html', {})




def signin(request):
    if request.method == 'POST':
        form = request.POST
        name_or_email = form.get('name')  # This can be either username or email
        password = form.get('password')
        
        # Check if the input is an email or username
        user = None
        if '@' in name_or_email:  # Email login case
            user = authenticate(request, username=User.objects.filter(email=name_or_email).first().username, password=password)
        else:  # Username login case
            user = authenticate(request, username=name_or_email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!')
            return redirect('home-page')
        else:
            messages.error(request, 'Login Error: Invalid credentials')
            return redirect('signin')

    return render(request, 'blogs/signin.html', {})




def home(request):
    posts = Post.objects.order_by('-date_posted')  # Order by most recent
    last_post = posts.first()  # Last post
    second_to_last = posts[1] if len(posts) > 1 else None  # Second-to-last post
    third_to_last = posts[2] if len(posts) > 2 else None  # Third-to-last post
    
    sports_posts = Post.objects.filter(category__name='Sports').order_by('-date_posted')
    politics_posts = Post.objects.filter(category__name='Politics').order_by('-date_posted')
    more = Post.objects.filter(category__name='More').order_by('-date_posted')
    
    context = {
        'posts': Post.objects.all(),
        'posts_by_date' : Post.objects.order_by('-date_posted'),  # Order by most recent

        'last_post': last_post,
        'second_to_last': second_to_last,
        'third_to_last': third_to_last,
        'sports_posts': sports_posts,
        'politics_posts': politics_posts,
        'more': more,
        'categories' : Category.objects.annotate(post_count=Count('post')),
    }
    
    # context = {
    #     'posts': Post.objects.all()
    # }
    return render(request, 'blogs/home.html', context)


@login_required
def user_home(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    paginator = Paginator(user_posts, 4)  # Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': Post.objects.filter(author= request.user).order_by('-date_posted'),
        'page_obj': page_obj,
    }
    return render(request, 'user/user.html',context)

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Fetch the uploaded image
        category_id = request.POST.get('category')  # Get the selected category
        category = Category.objects.get(id=category_id)  # Get the Category object
        npost = Post(title=title, content=content, author=request.user,image=image, category=category)
        npost.save()
        # Add a success flash message
        messages.success(request, 'Your post has been created successfully!')
        return redirect('create_post')
    
    categories = Category.objects.all()
    
    return render(request, 'user/create_post.html',{'categories':categories})




def single_post(request, id):
    # by default, id is a string
    # valid_id=False
    # posts = Post.objects.all()
    # print(type(id))
    # post_id = id
    # for post in posts:
    #     if post.id == post_id:# use if you have not converted it in the url:
    #         mainpost= post
    #         valid_id=True
    #         break
    # if valid_id:
    
     # Use get_object_or_404 to handle invalid IDs and avoid unnecessary looping
     
    context={
        'post' : get_object_or_404(Post, id=id),
        'categories' : Category.objects.annotate(post_count=Count('post'))
        
    }
    post = get_object_or_404(Post, id=id)
    categories = Category.objects.all()
        
    return render(request, "blogs/single_post.html", context)




def signout(request):
    logout(request)
    messages.success(request, 'logout successful')
    return redirect('signin')


def custom_404_view(request, exception):
    return render(request, 'blogs/404.html', status=404)
