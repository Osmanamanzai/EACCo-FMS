from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from accounts.views import dashboard
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='dashboard')),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('projects/', include('projects.urls')),
    path('expenses/', include('transactions.urls')),
    path('reports/', include('reports.urls')),
]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)