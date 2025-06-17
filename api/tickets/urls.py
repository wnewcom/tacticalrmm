from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/user/', views.UserProfileView.as_view(), name='user-profile'),
]