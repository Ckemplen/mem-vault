from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            return None
        path = request.path
        if path == reverse('login') or path.startswith('/register/') or path.startswith('/admin/'):
            return None
        return redirect('login')
