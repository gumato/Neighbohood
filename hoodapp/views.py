from django.shortcuts import render,redirect
from django.http  import HttpResponse,Http404


# Create your views here.
def index(request):
    date = dt.date.today()
    return render(request,'index.html{"date":date})

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
