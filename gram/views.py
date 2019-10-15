from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
# @login_required(login_url='/accounts/login/')
def home (request):
    image_form = PostForm()
    images = Post.objects.all()
    commentform = CommentForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile.post(form)

    return render(request, 'home.html', locals())

@login_required(login_url='/accounts/login/')
def prof(request):
    images = request.user.profile.posts.all()
    user_object = request.user
    user_images = user_object.profile.posts.all()
    user_saved = [save.photo for save in user_object.profile.saves.all()]
    user_liked = [like.photo for like in user_object.profile.mylikes.all()]
    print(user_liked)
    return render(request, 'adminprofile.html', locals())\
@login_required(login_url='/accounts/login/')
def edit(request):
    if request.method == 'POST':
        print(request.FILES)
        new_profile = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if new_profile.is_valid():
            new_profile.save()
            print(new_profile.fields)
            # print(new_profile.fields.profile_picture)
            return redirect('myaccount')
    else:
        new_profile = ProfileForm(instance=request.user.profile)
    return render(request, 'edit.html', locals())

@login_required(login_url='/accounts/login/')
def user(request, user_id):
    user_object=get_object_or_404(User, pk=user_id)
    if request.user == user_object:
        return redirect('myaccount')
    is_following = user_object.profile not in request.user.profile.follows
    user_images = user_object.profile.posts.all()
    user_liked = [like.photo for like in user_object.profile.mylikes.all()]
    return render(request, 'profile.html', locals())