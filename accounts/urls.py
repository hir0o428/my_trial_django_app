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
    path(app_name + '/user_registration/', views.UserRegistrationView.as_view(),
         name='user_registration'),
    # ex: /accounts/user_registration/send_mail/
    path(app_name + '/user_registration/complete/send_mail/', views.UserRegistrationMailView.as_view(),
         name='user_registration_send_mail'),
    # ex: /accounts/user_registration/<token>
    path(app_name + '/user_registration/complete/<token>', views.UserRegistrationCompleteView.as_view(),
         name='user_registration_complete'),
    # ex: /accounts/profile/2/
    path(app_name + '/profile/<int:pk>/', views.UserProfileView.as_view(),
         name='profile'),
    # ex: /accounts/profile/2/update/
    path(app_name + '/profile/<int:pk>/update/', views.UserProfileUpdateView.as_view(),
         name='profile_update'),
    # ex: /accounts/profile/2/password/
    path(app_name + '/profile/<int:pk>/password_change/', views.UserPasswordChangeView.as_view(),
         name='password_change'),
    # ex: /accounts/profile/2/password/complete
    path(app_name + '/profile/<int:pk>/password/complete/', views.UserPasswordChangeCompleteView.as_view(),
         name='password_change_complete'),
    # ex: /accounts/password_reset/
    path(app_name + '/password_reset/', views.UserPasswordResetView.as_view(),
         name='password_reset'),
    # ex: /accounts/password_reset/send_mail/
    path(app_name + '/password_reset/send_mail/', views.UserPasswordResetMailView.as_view(),
         name='password_reset_send_mail'),
    # ex: /accounts/password_reset/confirm/
    path(app_name + '/password_reset/confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    # ex: /accounts/password_reset/complete/
    path(app_name + '/password_reset/complete/', views.UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
