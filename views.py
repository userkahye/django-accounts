from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from .forms import RegistrationForm

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'clients/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        
        # Check if the request is AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  
            if form.is_valid():
                form.save()
                # Send success JSON response with a message and redirect URL
                return JsonResponse({
                    'success': True,
                    'message': 'Registration successful!', 
                    'redirect_url': reverse('register')
                })
            else:
                # Send error JSON with form validation errors
                return JsonResponse({
                    'success': False,
                    'errors': form.errors 
                }, status=400)
    
