from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail

from . tokens import generate_token
from gfg import settings

# Create your views here.
def home(request):
    messages = request._messages
    fname = None
    for message in messages:
        if "Welcome," in message.message:
            fname = message.message.split(", ")[1].split("!")[0]
            break
    
    return render(request, 'authentication/index.html', {'fname': fname})

def signup(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "USername already exsists!")
            return redirect('home')

        if User.objects.filter(email = email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwwords didnt match")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be alphanumeric")
            return redirect('home')

        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = fname
        myUser.last_name = lname
        myUser.is_active = False
        myUser.save()

        messages.success(request, "Your Account has been successfully created")

        # Mail Portion

        subject = "Welcome to GFG - Login"
        message = " Hello, " +myUser.first_name + " !!\n"+" Welcome to GFG!! \n Thanks for visiting our website \n We have also sent you a confirmation email, please confirm the email address to activate your account!!. \n\n Thanking you, \n Parth Patel"
        from_email = settings.EMAIL_HOST_USER
        to_list  = [myUser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Confirm Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email at GFG Django login!!"
        message2 = render_to_string('email_confirmation.html',{
            'name':myUser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myUser.pk)),
            'token': generate_token.make_token(myUser)
        })
        email = EmailMessage(
            email_subject, message2, settings.EMAIL_HOST_USER,[myUser.email]
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')
    

    return render(request, 'authentication/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'authentication/index.html', {'fname':fname})

        else:
            messages.error(request, "Bad Credentials")
        return redirect('home')
    
    return render(request, 'authentication/signin.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myUser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myUser = None

    if myUser is not None and generate_token.check_token(myUser, token):
        myUser.is_active = True
        myUser.save()
        login(request, myUser)
        
        messages.success(request, f"Welcome, {myUser.first_name}!")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')