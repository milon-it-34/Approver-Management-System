from django.shortcuts import redirect
from django.urls import reverse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path not in [reverse('login'), reverse('signup'), reverse('confirm_signup')]:
                return redirect('login')
        response = self.get_response(request)
        return response
