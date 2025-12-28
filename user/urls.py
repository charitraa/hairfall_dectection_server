
from django.urls import path
from .views import LoginView, UserCreateView,UserMeView, UserPhotoUpdateView,UserUpdateView
urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('me/', UserMeView.as_view(), name='user-me'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('update-photo/', UserPhotoUpdateView.as_view(), name='user-photo-update'),
] 