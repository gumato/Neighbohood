from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from .forms import *
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *



# Create your views here.
def index(request):
    date = dt.date.today()
    neighbourhood = Neighbourhood.objects.all()
    return render(request,'index.html',{"date": date,"neighbourhood":neighbourhood})

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                to_email = form.cleaned_data.get('email')
                return HttpResponse('Confirm your email address to complete registration')
           
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'Form':form})

def search_results(request):

    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.search_by_neighbourhood(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"businesses": searched_businesses})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

login_required(login_url='/accounts/login/')
def hood(request):
    date = dt.date.today()
    return render(request, 'hood.html', locals())

@login_required(login_url='/accounts/login')
def add_post(request):
    if request.method == 'POST':
        postform = PostForm(request.POST, request.FILES)
        if postform.is_valid():
            post = postform.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('hood')
    else:
        postform = PostForm()
    return render(request,'add_post.html',locals())


@login_required(login_url='/accounts/login/')
def business(request, hood_id):
    date = dt.date.today()
    print(date)
    bs = Business.objects.filter(neighbourhood_id=hood_id)
    print(bs)
    return render(request, 'hood.html', locals())

def profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)

    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)
    images = Image.get_profile_images(profile.id)
    title = f'@{profile} Neighbourhood photos and videos'

    return render(request, 'profile/profile.html', {'title':title, 'profile':profile, 'profile_details':profile_details})


@login_required(login_url='/accounts/login/')
def new_neighbourhood(request):
    current_user = request.user
    
    if request.method == 'POST':
        form = NeighbourhoodForm(request.POST, request.FILES)
        if form.is_valid():
            neighbourhood = form.save(commit=False)
            neighbourhood.user = current_user
            neighbourhood.profile = profile
            neighbourhood.save()
        return redirect('index')
    else:
        form = NeighbourhoodForm()
    return render(request, 'new_neighbourhood.html', {"form": form})

@login_required(login_url='/accounts/login')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.user = request.user
            edit.save()
            return redirect('profile/edit_profile')
    else:
        form = ProfileForm()

    return render(request, 'profile/edit_profile.html', {'form':form})


@login_required(login_url='/accounts/login')
def upload_business(request):
    if request.method == 'POST':
        uploadform = BusinessForm(request.POST, request.FILES)
        if uploadform.is_valid():
            upload = uploadform.save(commit=False)
            upload.save()
            return redirect('index')
    else:
        uploadform = BusinessForm()
    return render(request,'upload_business.html',locals())


