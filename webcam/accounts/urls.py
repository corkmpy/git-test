from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, profile, home, memo_create, memo_update, memo_delete

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView, name='logout'), 
    path('profile/', profile, name='profile'),
    path('memo/create/', memo_create, name='memo_create'),
    path('memo/<int:pk>/update/', memo_update, name='memo_update'),
    path('memo/<int:pk>/delete/', memo_delete, name='memo_delete'),
    path('', home, name='home'),
]
