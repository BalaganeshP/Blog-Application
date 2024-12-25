from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post,AboutUs, category
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm, ForgotPasswordForm, LoginForm, PostForm,RegisterForm, ResetPasswordForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


# Create your views here.
'''
posts=[
        {'id':1,'title': 'post 1','content':'content of post 1'},
        {'id':2,'title': 'post 2','content':'content of post 2'},
        {'id':3,'title': 'post 3','content':'content of post 3'},
        {'id':4,'title': 'post 4','content':'content of post 4'},
    ]
'''

def index(request):
    blog_tittle="Latest Posts"
    all_posts=Post.objects.all()

    # Paginate
    paginator = Paginator(all_posts,4)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'blog/index.html',{'blog_tittle':blog_tittle,'page_obj': page_obj})
    

def detail(request, slug):
    #post = next((item for item in posts if item['id'] == int(post_id)), None) 
    try:
        post=Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post Does Not Exists")
    #logger = logging.getLogger("TESTING")
    #logger.debug(f'post variable is {post}')
    return render(request,'blog/detail.html',{'Post': post,'related_posts':related_posts})

def old_url_redirect(request):
    return redirect("reverse('blog:new_page_url)")

def new_url_view(request):
    return HttpResponse("puthu paiyan")

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

        logger = logging.getLogger("TESTING")
        if form.is_valid():    
            logger.debug(f'post Data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message = 'Your Email has been sent!'
            return render(request,'blog/contact.html',{'form':form,'success_message':success_message})
        else:
            logger.debug('Form validation failure')
        return render(request,'blog/contact.html',{'form':form,'name':name, 'email':email, 'message':message})
    return render(request,'blog/contact.html')

def about_view(request):
    about_content = AboutUs.objects.first().content
    return render(request,'blog/about.html',{'about_content':about_content})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  #user data created
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'Registeration Successfull.You can login')
            return redirect("blog:login")# redirect to loginpage
   
    return render(request, 'blog/register.html',{'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        #login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request,user)       
                print("Login Success")
                return redirect("blog:dashboard")# redirect to dashboard
    return render(request, 'blog/login.html',{'form':form})

def dashboard(request):
    blog_title = "My Posts"
    #getting user post
    all_posts=Post.objects.filter(user=request.user)
    paginator = Paginator(all_posts,4)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/dashboard.html',{"blog_title": blog_title,'page_obj':page_obj})

def logout(request):
    auth_logout(request)
    return redirect("blog:index")

def forgot_password(request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        #form
       form =  ForgotPasswordForm(request.POST)
       if form.is_valid():
           email = form.cleaned_data['email']
           user= User.objects.get(email=email)
           

           token = default_token_generator.make_token(user)
           uid = urlsafe_base64_encode(force_bytes(user.pk))
           current_site = get_current_site(request)
           domain = current_site.domain
           subject = "Reset Passwor Requested"
           message = render_to_string('blog/reset_password_email.html', {'domain': domain, 'uid': uid, 'token': token})


           send_mail(subject,message, 'noreply@jvlcode.com', [email])
           messages.success(request,'Email has been sent')
           
    return render(request, 'blog/forgot_password.html', {'form': form})
  


def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    if request.method == 'POST':
        #form
        form = ResetPasswordForm(request.POST)
       
        if form.is_valid():
            new_password =form.cleaned_data['new_password']

            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                messages.success(request,'Your password has been reset successfully! ')
                return redirect('blog:login')                   
            else:
                 messages.error(request, 'The password reset link is invalid')
   
                
   
    return render(request, 'blog/reset_password.html', {'form': form})

def new_post(request):
        categories= category.objects.all()
        form=PostForm()
        if request.method == 'POST':
            #form
            form=PostForm(request.POST, request.FILES)
            if form.is_valid():
                post=form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('blog:dashboard')
        return render(request, 'blog/new_post.html',{'categories':categories,'form':form})

def edit_post(request, post_id):
    categories= category.objects.all()
    post = get_object_or_404(Post,id=post_id)
    form = PostForm()
    if request.method == "POST":
        #form
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post Updated successfully! ')
            return redirect('blog:dashboard')

    return render(request, 'blog/edit_post.html', {'categories':categories, 'post': post, 'form':form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request,'Post deleted successfully! ')
    return redirect('blog:dashboard')
