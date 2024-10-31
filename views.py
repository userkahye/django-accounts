from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RegistrationForm, LoginForm
from .accounts import AccountService01
from .userauth import UserMiddleware01

class RegistrationView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'clients/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        
        # Check if the request is AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
            if form.is_valid():
                # Get the cleaned data from the form
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                # Use the AccountService to hash the password and save the user
                AccountService01.save_user_with_hashed_password(username, password, email=email)
                
                # Send success JSON response with a message and redirect URL
                return JsonResponse({
                    'success': True,
                    'message': 'Registration successful!',
                    'redirect_url': reverse('login')
                })
            else:
                # Send error JSON with form validation errors
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
        else:
            # Handle non-AJAX request
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                # Save the user using AccountService
                AccountService01.save_user_with_hashed_password(username, password, email=email)

                # Redirect to the login page
                return HttpResponseRedirect(reverse('login'))
            else:
                # Re-render the form with errors for non-AJAX request
                return render(request, 'clients/register.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'clients/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        # Check if the request is an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = UserMiddleware01.authenticate_user(request, username, password)

                if user is not None:
                    UserMiddleware01.login_user(request, user)
                    return JsonResponse({'success': True, 'redirect_url': reverse('dashboard')})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid username or password.'}, status=400)
        else:
            # Handle non-AJAX request
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = UserMiddleware01.authenticate_user(request, username, password)

                if user is not None:
                    UserMiddleware01.login_user(request, user)

                    return HttpResponseRedirect(reverse('register'))
                else:

                    form.add_error(None, 'Invalid username or password.')
                    
            return render(request, 'clients/login.html', {'form': form})


class DashboardView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')  

        client = request.user  
        return render(request, 'clients/dashboard.html', {'client': client}) 


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        
        UserMiddleware01.logout_user(request)  

        return render(request, 'clients/login.html')  