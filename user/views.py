from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from .forms import SignUpForm, ProfileUpdateForm
from django.contrib.auth.views import LoginView
from .models import Profile


@csrf_protect
def signup_view(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST, files=request.FILES)

        if form.is_valid():
            user = form.save()
            # try:
            #     profile = request.user.profile
            # except Profile.DoesNotExist:
            #     profile = Profile.objects.create(user=request.user)  # Create profile if missing

            login(request, user)
            return redirect('profile')

    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


class UserLogin(LoginView):
    redirect_authenticated_user = True      # login qilgan userni qaytib login page ga yubormayd

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('blog:index')

    def form_valid(self, form):
        responses = super().form_valid(form)
        if self.request.user.is_authenticated:
            Profile.objects.get_or_create(user=self.request.user)
        return responses

    def form_invalid(self, form):
        messages.error(self.request, 'Username or Password incorrect')
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    logout(request)
    return redirect('blog:index')

# def profile_view(request):
#     profile = get_object_or_404(Profile, user=request.user)
#     return render(request, 'registration/profile.html', {'profile': profile, 'user': request.user})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    #profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    return render(request, 'registration/profile.html', {'form': form, 'profile': profile})


from blog.models import Message
from .forms import MessageForm
from django.http import JsonResponse

def send_message(request):

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            form.save()
            # messages.success('Xabar muvaffaqiyatli yuborildi!')
            return JsonResponse({'message': "Xabar muvaffaqiyatli yuborildi!"})

        else: JsonResponse({'error': "Nimadir xato boldi"}, status=400)
    else:
        form = MessageForm()

    return render(request, 'blog/contact.html', {'form': form})

