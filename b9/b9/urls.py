from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="account.html")),
    path("admin/", admin.site.urls),
    path('user/', include('user.urls')),
    path('accounts/', include('allauth.urls')),
    path('post/', include('post.urls'))
]
