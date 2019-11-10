from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationForm
from django_auth.forms import PasswordResetConfirmationForm

# Create your views here.
def index(request):
    """Return the index.html file"""
    return render(request,  'index.html')
    

@login_required 
def logout(request):
    """Logout"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))
    
    
def login(request):
    """ Return a login page """
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username = request.POST['username'],
                                     password = request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Username or Password incorrect ! ! !")
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {"login_form": login_form})
    
def registration(request):
    """Display the registration form """
    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST) #We instanciate the form from the post
        if registration_form.is_valid(): #if the form is valid
            registration_form.save() # Save it to the database (we don't have to specify, as we have already done it in the class metadata -> model = User)
            user = auth.authenticate(username = request.POST['username'],
                                     password = request.POST['password1']) #we authenticate the user
            if user: #if authentication was successful
                auth.login(user = user, request = request) #we log them in
                messages.success(request, "You have successfully been registered")
                return redirect(reverse('index'))
            else:
                messages.error(request, "Unable to register at this time")
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {"registration_form": registration_form})
    
    
def user_profile(request):
    user = User.objects.get(email=request.user.email) #retrieving the user data for the one that has the email address stored in our request object
    return render(request, 'profile.html', {'profile': user}) 
    
def password_reset(request):
    return render(request, 'password_reset_form.html')