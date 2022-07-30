"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views as view

app_name = "main"
urlpatterns = [
    path('', view.index, name="index"),     # name="" is used for jinja
    path('accounts/login/', view.EALoginView.as_view(), name='login'),
    path('accounts/profile/', view.profile, name='profile'),
    path('accounts/logout/', view.EALogoutView.as_view(), name='logout'),
    path('accounts/profile/change/', view.ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/password/change/', view.EAPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/done/', view.RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', view.RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', view.user_activate, name='register_activate'),
    path('accounts/profile/delete/', view.DeleteUserView.as_view(), name='profile_delete'),
    path('tools/csv-connection/csv-upload-success/', view.csv_upload),
    path('tools/<str:tool>/', view.tools_page, name='tools'),
    path('<str:page>/', view.other_page, name='other'),
]
