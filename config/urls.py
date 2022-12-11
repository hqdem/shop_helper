from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    re_path(r'auth-token/', include('djoser.urls.authtoken')),
    path('api/v1/', include('shop_helper.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
