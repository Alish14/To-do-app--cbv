"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path ,include
from django.contrib.auth import views as auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Project Todo app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alish14.mod@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)




urlpatterns = [
     path('admin/', admin.site.urls),
     path('', include('todo.urls')),
     path("accounts/",include("accounts.urls")),
     path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_reset/password_change_done.html'),
         name='password_change_done'),

     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_reset/password_change.html'),
         name='password_change'),

     path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_done.html'),
         name='password_reset_done'),

     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
     path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),

     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset/password_reset_complete.html'),
         name='password_reset_complete'),
     path('api/v1/',include('todo.api.v1.urls')),
    path('swagger/api.json',schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
]
