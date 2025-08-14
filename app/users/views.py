from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from .models import Invitation


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(View):
    template_name = "users/register.html"

    def dispatch(self, request, token, *args, **kwargs):
        self.invitation = get_object_or_404(Invitation, token=token, used=False)
        if self.invitation.expires_at < timezone.now():
            return render(request, "users/invitation_invalid.html", status=404)
        return super().dispatch(request, token, *args, **kwargs)

    def get(self, request, token):
        form = UserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, token):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            self.invitation.used = True
            self.invitation.save()
            login(request, user)
            return redirect("home")
        return render(request, self.template_name, {"form": form})


@login_required
def home(request):
    return render(request, "users/home.html")
