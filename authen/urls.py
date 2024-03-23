from django.urls import path, include
from django.contrib.auth import views as auth_views
from authen import views
import core
urlpatterns = [
    path('', views.home, name="home"),
    # path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'),name='login'),
    path('login/', views.CustomLoginView.as_view(), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name="signup"),
    path('request/', include('core.urls')),
    path('confirm_signup/', views.confirm_signup, name='confirm_signup'),

]



# When passing 'auth/login.html' for template_name parameter, we tell auth.views.LoginView that the path will be used for login form 

# Using auth.views.LogoutView helps us handle logout request automatically, we only need to call {% url 'logout' %} where we want to make logout event in the HTML template.

