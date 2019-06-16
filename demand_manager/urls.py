from django.urls import path
from . import views

app_name = 'demand_manager'
urlpatterns = [
    # ex: /demand_manager/
    # path('', views.DemandTopView.as_view(), name='top'),
    path('', views.DemandTopFilterView.as_view(), name='top'),

    # ex: /demand_manager/login/
    #path('login/', views.DemandLoginView.as_view(), name='login'),
    # ex: /demand_manager/logout/
    #path('logout/', views.DemandLogoutView.as_view(), name='logout'),

    # ex: /demand_manager/create/
    path('create/', views.DemandCreateView.as_view(), name='create'),
    # ex: /demand_manager//2/
    path('<int:pk>/', views.DemandDetailView.as_view(), name='detail'),
    # ex: /demand_manager/2/update/
    path('<int:pk>/update/', views.DemandUpdateView.as_view(), name='update'),
    # ex: /demand_manager/2/delete/
    path('<int:pk>/delete/', views.DemandDeleteView.as_view(), name='delete'),
    # ex: /demand_manager/analysis/
    path('analysis/', views.DemandAnalysisView.as_view(), name='analysis'),
]
