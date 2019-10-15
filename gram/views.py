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