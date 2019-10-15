from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required(login_url='/accounts/login/')
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