from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

from . import views
from .views import redirect_login

admin.site.site_header = "Qlma Admin Portal"
admin.site.site_title = "Qlma Admin Portal"
admin.site.index_title = "Welcome to Qlma Admin Portal"

app_name = 'project'

urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('', redirect_login, name='index'),
    path('register/', user_views.RegisterView.as_view(template_name='users/register.html'), name='register'),
    path('activate/<uidb64>/<token>/', user_views.ActivateAccount.as_view(), name='activate'),
    path('profile/', user_views.profile, name='profile'),
    path('user/<str:username>/', user_views.user, name='user'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('', include('news.urls')),
    path('', include('messaging.urls')),
    path('', include('cal.urls')),
    path('', include('users.urls')),
    path('', include('timetable.urls')),
    path('polls/', include('polls.urls')),
    path('lunch/', include('lunch.urls')),

    path('staff/', views.staff, name='staff'),


    path('school/<int:school_id>/', views.school, name='school'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)