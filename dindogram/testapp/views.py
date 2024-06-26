
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.
def home(request):
    return render(request,'page1.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            return render(request,'career.html',{'user': request.user})  # Replace 'home' with the name of your home page URL
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')



def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
       
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken.")
            return redirect('signup')
        otp = ''.join(random.choices('0123456789', k=4))
        request.session['otp'] = otp
                
        send_mail(
                    'confirm account',
                    f'Your OTP for conforming your account is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
        return render(request, 'send_otp.html', { 'email':email, 'password':password1,'first_name':first_name, 'last_name':last_name})  

    return render(request, 'signup.html')

def verify_otp(request):
    if request.method == 'POST':
        if request.POST.get('password'):
            email=request.POST.get('email')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            password1=request.POST.get('password')
            
        else:
           first_name=None
           email = request.POST.get('email')
        otp_num1= request.POST.get('otp_num1')
        otp_num2= request.POST.get('otp_num2')
        otp_num3= request.POST.get('otp_num3')
        otp_num4= request.POST.get('otp_num4')
        otp_entered=otp_num1+otp_num2+otp_num3+otp_num4
        stored_otp = request.session.get('otp')
        if otp_entered == stored_otp:
            if first_name:
                user = User.objects.create_user( username=last_name,email=email, password=password1,first_name=first_name, last_name=last_name)
                user.save()
                user = authenticate(username=email, password=password1)
                send_mail(
                    'account created succesfully',
                    f'Hello {first_name} {last_name} your account is created successfully...!',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                if email is not None:
                    login(request, user)
                    return render(request,'career.html')  # Replace 'home' with the name of your home page URL pattern
                else:
                    return redirect('signup')
            else:
               return render(request, 'reset_password.html', {'email': email})
        else:
            # Invalid OTP, display error message
            return render(request, 'send_otp.html', {'email': email, 'error_message': 'Invalid OTP'})
    return redirect('send_otp')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                otp = ''.join(random.choices('0123456789', k=4))
                request.session['otp'] = otp
                
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP for resetting the password is: {otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return render(request, 'send_otp.html', {'email': email})
    return render(request, 'forgot.html')


def forgot(request):
    return render(request,'forgot.html')




def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate passwords
        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match', 'email': email})

        # Find the user by email
        user = User.objects.filter(email=email).first()
        if user:
            # Reset the user's password
            user.set_password(new_password)
            user.save()

            # Send an email notification
            send_mail(
                'Password Reset Successful',
                'Your password has been successfully reset.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('login')  # Redirect to login page after successful password reset
        else:
            return render(request, 'reset_password.html', {'error': 'User not found', 'email': email})

    return render(request, 'forgot.html')





def logout_view(request):
    logout(request)
    return redirect('home') 

def startup(request):
    return render(request,'startup.html')
def myidea(request):
    return render(request,'own.html')
def buzz(request):
    return render(request,'buzz.html')
