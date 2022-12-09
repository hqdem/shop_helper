from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('shop_helper.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
