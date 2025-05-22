from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import Custom_user
import random


# ------------------- Registration View -------------------

def register(request):
    if request.method == "POST":
        username = request.POST.get('username') 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        email = request.POST.get('email') 
        phone = request.POST.get('phone') 
        address = request.POST.get('address') 
        city = request.POST.get('city') 
        state = request.POST.get('state') 
        country = request.POST.get('country') 
        zip_code = request.POST.get('zip_code') 
        image = request.FILES.get('image') 
        password1 = request.POST.get('password1') 
        password2 = request.POST.get('password2') 
        if password1 == password2:
            otp = random.randint(1000,9999)
            user = Custom_user.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,phone=phone,address=address,city=city,state=state,country=country,zip_code=zip_code,image=image,password=password1,otp=otp)
            user.save()
            send_email(request,email,otp)
            return redirect ('login')

    return render(request,'auth/register.html')   


def send_email(request,email, otp):
    subject = 'welcome to my website'
    message = f'Thank you for registering with us.{otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list)


# ------------------- Login View -------------------

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_verified:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')  
            else:
                messages.warning(request, "Account not verified. Please check your email for the OTP.")
                request.session['username_for_otp'] = username
                return redirect('verify_otp')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'auth/login.html')


# ------------------- Logout View -------------------

def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# ------------------- OTP Verification View -------------------

def verify_otp(request):
    username = request.session.get('username_for_otp')

    if not username:
        messages.error(request, "No OTP session found. Please register first.")
        return redirect('register')

    try:
        user = Custom_user.objects.get(username=username)
    except Custom_user.DoesNotExist:
        messages.error(request, "User not found. Please register again.")
        return redirect('register')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')

        if str(user.otp) == str(otp_input): 
            user.is_verified = True
            user.is_active = True
            user.otp = None  
            user.save()
            del request.session['username_for_otp']
            messages.success(request, "OTP verified! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'auth/otp_submit.html')

# ------------------- Forget-pass View -------------------

def Forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = Custom_user.objects.get(email=email)
        except Custom_user.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return render(request, 'auth/forget-pass.html')

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()

        send_mail(
            'Password Reset OTP',
            f'Your OTP to reset your password is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        request.session['email_for_otp'] = email
        messages.info(request, "An OTP has been sent to your email address.")
        return redirect('reset_password_otp')  

    return render(request, 'auth/forget-pass.html')


# ------------------- Reset Password View -------------------

def reset_password_otp(request):
    email = request.session.get('email_for_otp')

    if not email:
        messages.error(request, "Session expired. Please try again.")
        return redirect('forget_pass')

    try:
        user = Custom_user.objects.get(email=email)
    except Custom_user.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('forget_pass')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if str(user.otp) == str(entered_otp):
            user.otp = None
            user.save()
            request.session['reset_email'] = email
            return redirect('set_new_password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'auth/otp_submit.html')  # you can reuse the same OTP form


def set_new_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        email = request.session.get('reset_email')  # You should've stored this in OTP step

        if not email:
            messages.error(request, "Session expired. Try again.")
            return redirect('forget_pass')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('set_new_password')

        try:
            user = Custom_user.objects.get(email=email)
            user.set_password(password1)
            user.save()
            messages.success(request, "Password has been reset successfully.")
            return redirect('login')
        except Custom_user.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forget_pass')

    return render(request, 'auth/set-new-password.html')


# ------------------- Dashboard View -------------------

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('register')
    
    user= request.user

    user_data = Custom_user.objects.get(id=user.id)

    return render(request,'auth/user-dashboard.html',{'user_data':user_data})

# ------------------- Update-profile View -------------------

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            # Don't commit to DB yet
            updated_user = form.save(commit=False)

            password = form.cleaned_data.get('password')
            if password:
                updated_user.set_password(password)
                update_session_auth_hash(request, updated_user)  # keeps session alive
            else:
                # If password was blank, keep the current hashed password
                updated_user.password = user.password

            updated_user.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_dashboard')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'auth/update_profile.html', {'form': form})





