from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('user/', admin.site.urls),
    path('pare/', include('pare_app.urls'), name='pare'),
    path('accounts/', include('accounts.urls')),
]
