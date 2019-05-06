from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /accounts/user_registration/
    path('user_registration/', views.UserRegistrationView.as_view(), name='user_registration'),
    # ex: /accounts/user_registration/
    path('user_registration/complete/', views.UserRegistrationCompView.as_view(), name='user_registration_complete'),
    # ex: /accounts/profile/2/
    path('profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    # ex: /accounts/profile/2/update/
    path('profile/<int:pk>/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    # ex: /accounts/profile/2/password/
    path('profile/<int:pk>/password/', views.UserPasswordChangeView.as_view(), name='password'),
    # ex: /accounts/profile/2/password/complete
    path('profile/<int:pk>/password/complete/', views.UserPasswordChangeCompleteView.as_view(), name='password_complete'),
]
