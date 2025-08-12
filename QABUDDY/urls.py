
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from checklist.views import CustomLoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #  path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', include('checklist.urls')),
]
