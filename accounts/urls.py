from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # ex: /
    path('', views.TopView.as_view(), name='top'),
    # ex: /login/
    path('login/', views.TopLoginView.as_view(), name='login'),
    # ex: /logout/
    path('logout/', views.TopLogoutView.as_view(), name='logout'),

    # ex: /accounts/user_registration/
    path(app_name + '/user_registration/', views.UserRegistrationView.as_view(), name='user_registration'),
    # ex: /accounts/user_registration/
    path(app_name + '/user_registration/complete/', views.UserRegistrationCompView.as_view(), name='user_registration_complete'),
    # ex: /accounts/profile/2/
    path(app_name + '/profile/<int:pk>/', views.UserProfileView.as_view(), name='profile'),
    # ex: /accounts/profile/2/update/
    path(app_name + '/profile/<int:pk>/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    # ex: /accounts/profile/2/password/
    path(app_name + '/profile/<int:pk>/password/', views.UserPasswordChangeView.as_view(), name='password'),
    # ex: /accounts/profile/2/password/complete
    path(app_name + '/profile/<int:pk>/password/complete/', views.UserPasswordChangeCompleteView.as_view(), name='password_complete'),
]
