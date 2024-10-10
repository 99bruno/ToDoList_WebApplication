from django.urls import path
from . import views


urlpatterns = [
    # Path Converters
    # int: numbers
    # str: strings
    # path: whole urls /
    # slug: hyphen-and_underscores_stuff
    # UUID: universally unique identifier

    # URL pattern for user login
    path('login/', views.login_user, name="login"),

    # URL pattern for user logout
    path('logout/', views.logout_user, name="logout_user"),

    # URL pattern for user registration
    path('register/', views.register_user, name="register"),
]
