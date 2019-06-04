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
    hoods = Neighbourhood.objects.all()
    return render(request,'index.html',{"date": date,"hoods":hoods})

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

def profile(request):
        date = dt.date.today()
        current_user = request.user
        profile = Profile.objects.get(user=current_user.id)
        hoods = Neighbourhood.objects.all()
        return render(request, 'profile/profile.html', {"date": date, "profile":profile,"hoods":hoods}) 

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'business' in request.GET and request.GET["business"]:
        search_term = request.GET.get("business")
        searched_businesses = Business.objects.filter(name=search_term)
        message = f"{search_term}"
        profiles=  Profile.objects.all( )
      
        return render(request, 'search.html',{"message":message,"business": searched_businesses,'profiles':profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})
@login_required(login_url='/accounts/login/')
def new_hood(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = HoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.user = current_user
            hood.profile = profile
            hood.save()
        return redirect('index')
    else:
        form = HoodForm()
    return render(request, 'new_hood.html', {"form": form})
def hoods(request,id):
    date = dt.date.today()
    post=Neighbourhood.objects.get(id=id)
    business = Business.objects.filter(neighbourhood=post)
    return render(request,'hood.html',{"post":post,"date":date, "business":business})

def edit_profile(request):
    date = dt.date.today()
    current_user = request.user
    profile = Profile.objects.get(user=current_user.id)
    if request.method == 'POST':
        signup_form = EditForm(request.POST, request.FILES,instance=request.user.profile) 
        if signup_form.is_valid():
            signup_form.save()
            return redirect('profile')
    else:
        signup_form =EditForm() 
        
    return render(request, 'profile/edit_profile.html', {"date": date, "form":signup_form,"profile":profile})

def post_business(request,id):
    date = dt.date.today()
    hood=Neighbourhood.objects.get(id=id)
    business = Business.objects.filter(neighbourhood=hood)
    form = BusinessForm()
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.profile = request.user.profile
            business.neighbourhood = hood
            business.save()
            return redirect('index')
    else:
        form = BusinessForm()
        return render(request,'new_business.html',{"form":form,"business":business,"hood":hood,  "date":date})


