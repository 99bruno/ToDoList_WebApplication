from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .forms import RegisterUserForm


def login_user(request) -> HttpResponse:
    """
    Handles user login functionality.

    This view function processes login requests. If the request method is POST, it attempts to authenticate the user
    with the provided username and password. If authentication is successful, the user is logged in and redirected to
    the 'all-tasks' page. If authentication fails, an error message is displayed and the user is redirected back to
    the login page. For GET requests, it renders the login page.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'all-tasks' page if login is successful.
        - HttpResponse: A redirect to the login page with an error message if login fails.
        - HttpResponse: Renders the login page for GET requests.
    """

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all-tasks')
        else:
            messages.success(request, "There Was An Error Logging In, Try Again...")
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})


def logout_user(request) -> HttpResponse:
    """
    Handles user logout functionality.

    This view function logs out the user and redirects them to the login page with a success message.

    :param request: The HTTP request object containing metadata about the request.
    :returns: HttpResponse: A redirect to the login page with a success message.
    """

    logout(request)
    messages.success(request, "You Were Logged Out!")
    return redirect('login')


def register_user(request):
    """
    Handles user registration functionality.

    This view function processes registration requests. If the request method is POST, it attempts to register the
    user with the provided data. If registration is successful, the user is authenticated, logged in, and redirected
    to the 'all-tasks' page. For GET requests, it renders the registration page with an empty registration form.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'all-tasks' page if registration is successful.
        - HttpResponse: Renders the registration page with an empty registration form for GET requests.
    """

    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful!")
            return redirect('all-tasks')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register_user.html', {
        'form': form,
    })
