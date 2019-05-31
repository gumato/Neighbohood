from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404
import datetime as dt
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    date = dt.date.today()
    return render(request,'index.html',{"date": date })

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

