from django.shortcuts import render
from .forms import UserForm,UserProfileInfoForm

#for log in
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        #grab info off the forms
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #grab everything from the base user form
            user =user_form.save() #saves User form to database
            user.set_password(user.password)#hashing password
            user.save()#saves changes to the user updated with hashed password

            #grab profile form
            profile = profile_form.save(commit=False) #commit=False tells it to not write to the database yet. to avoid collisions
            profile.user = user #this sets up onetoone relationship

            #check if photo provided, then assign to profile.profile_pic
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']  #['key'] is based on name 'upload_to' in models

            #save profile info to database
            profile.save()
            registered = True
            print('REGISTERED!')

        else:
            #prints out errors that arise, if forms arent valid
            print(user_form.errors,profile_form.errors)

    else:
        # if method was not POST, just provides forms to be displayed
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    #{'key',value} is for template tagging. key should match what is in the html. value should match variable in this 'views.py' file
    return render(request, 'basic_app/registration.html',{'user_form':user_form,
                                                        'profile_form':profile_form, 'registered':registered})



@login_required
def special(request):
    return HttpResponse("you are logged in! here is special info")



@login_required  #builtin decorator requires loggedin to perform function
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username') #gets from html post the input with name = 'username'
        password = request.POST.get('password')

        #django built in user authentication
        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                #once logged in send to new page
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account No Longer Active")
        else:
            print('login attempted and failed') #note to console
            return HttpResponse("Invalid Login, Try again")
    else:
        return render(request,'basic_app/log_in.html')
