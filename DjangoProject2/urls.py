
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from books.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', auth_views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('', include('books.urls')),

]
