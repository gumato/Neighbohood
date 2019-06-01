from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from .models import Profile,Neighbourhood,Business
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,ProfileForm
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *



# Create your views here.
def index(request):
    date = dt.date.today()
    profiles = Profile.objects.all()
    # rates = Rate.objects.all()
    return render(request,'index.html',{"date": date})

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
@login_required
def profile_path(request,id_user):
    user=User.objects.get(id=id_user)
    images = Project.objects.all()
    my_profile = Profile.objects.filter(user_id=request.user)[0:1]

    return render(request,'profile.html',{'profile':my_profile})    

def search(request):
    if 'project' in request.GET and request.GET['project']:
        search_term = request.GET.get('project')
        search_project = Project.search_by_name(search_term)
        message = f'{search_term}'

        return render(request, 'search.html',{'message':message, 'projects':search_project})
    else:
        message = 'Enter term to search'
        return render(request, 'search.html', {'message':message})
def post_new(request):

    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form =UploadForm()

    return render(request,'post_new.html',locals())

@login_required(login_url='/accounts/login/')
def new_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.editor = current_user
            project.save()
        return redirect('index')

    else:
        form = UploadForm()
    return render(request, 'new_project.html', {"form": form})



def single_post(request,project_id):
   
    projects = Project.objects.get(id=project_id)
    print(projects.image.url)
 

    return render(request,'single_project.html',{"projects":projects})


def editprofile(request):

    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
    
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user_id=request.user
            profile.save()
            return redirect('profile',request.user.id)
    else:
        form =ProfileForm()
        
    return render(request,'editprofile.html',locals()) 


