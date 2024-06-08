from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm, MemoForm
from .models import Memo
from itertools import zip_longest
import calendar
from django.utils import timezone
from django.contrib.auth import logout
from datetime import date

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def CustomLogoutView(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    memos = Memo.objects.filter(user=user)
    return render(request, 'registration/profile.html', {'user': user, 'memos': memos})

@login_required
def memo_create(request):
    user = request.user
    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = user
            memo.date = date.today()
            memo.save()
            return redirect('profile')
    else:
        form = MemoForm()
    return render(request, 'registration/memo.html', {'form': form})

@login_required
def memo_update(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'registration/memo.html', {'form': form, 'memo': memo})

@login_required
def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == 'POST':
        memo.delete()
        return redirect('profile')
    return render(request, 'registration/memo_delete.html', {'memo': memo})
    
def home(request):
    return render(request, 'home.html')
@login_required
def profile_view(request):
    user = request.user
    today = date.today()
    context = {
        'user': user,
    }
    return render(request, 'registration/profile.html', context)