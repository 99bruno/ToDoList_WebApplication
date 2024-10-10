import datetime

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TagForm, TaskTagForm
from .models import Task, TagTask
from django.http import HttpResponse
from django.db.models import Q


@login_required
def output(request, html_page: str, context: dict) -> HttpResponse:
    """
     Renders the specified HTML page with the given context.

     :param request: HttpRequest object containing metadata about the request.
     :param html_page: str, the name of the HTML page to render.
     :param context: dict, the context data to pass to the template.

     :return: HttpResponse object with the rendered HTML page.
     """

    context["first_tags"] = TagTask.objects.filter(user_id=request.user)[:2]
    context["all_tags_count"] = Task.objects.filter(user_id=request.user, completed=False).count()
    context["completed_tags_count"] = Task.objects.filter(user_id=request.user, completed=True).count()
    context["today_tasks_count"] = Task.objects.filter(user=request.user, completed=False, date=datetime.date.today()).count()
    context["overdue_tasks_count"] = Task.objects.filter(user=request.user, completed=False, date__lt=datetime.date.today()).count()

    return render(request, html_page, context)


def overdue_tasks(request) -> HttpResponse:
    """
    Handles the display and submission of overdue tasks.

    This view function processes GET and POST requests for overdue tasks. For GET requests, it renders the overdue tasks
    page with a list of overdue tasks and a form to add new tasks. For POST requests, it processes the submitted form
    data to add a new task.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'all-tasks' page if a new task is successfully added.
        - HttpResponse: Renders the overdue tasks page with the list of overdue tasks and the task form for GET requests.
    """

    submitted = False
    if request.method == "POST":
        task_form = TaskForm(request.POST, user=request.user)
        if task_form.is_valid():
            event = task_form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('all-tasks')
    else:
        task_form = TaskForm(user=request.user, initial={'date': datetime.date.today()})

        if 'submitted' in request.GET:
            submitted = True

    tasks = Task.objects.filter(user=request.user, completed=False, date__lt=datetime.date.today())
    tasks_amount = tasks.count()

    return output(request, 'tasks/overdue_tasks.html', {
        "Text_of_the_page": "Overdue tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        'submitted': submitted,
        "edit": False,
    })


def todo_overdue_task(request, task_id: int) -> HttpResponse:
    """
    Toggles the completion status of an overdue task.

    This view function retrieves the task with the given task_id, toggles its completion status, saves the changes,
    and redirects the user to the overdue tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be toggled.
    :return: HttpResponse: A redirect to the overdue tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.completed = not task_info.completed
    task_info.save()
    return redirect('overdue-tasks')


def task_detail_overdue(request, task_id: int) -> HttpResponse:
    """
    Renders the task detail page for an overdue task.

    This view function retrieves the task with the given task_id, checks if the task belongs to the current user,
    and renders the task detail page. If the task does not belong to the current user, it raises a 404 error.
    If the form is valid, it saves the task and redirects to the overdue tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be detailed.
    :return: HttpResponse: A redirect to the overdue tasks page if the form is valid,
    otherwise renders the task detail page.
    """

    task_info = Task.objects.get(pk=task_id)

    if task_info.user != request.user:
        raise Http404("Task does not exist or you do not have permission to view it.")

    task_form = TaskForm(request.POST or None, instance=task_info, user=request.user)

    if task_form.is_valid():
        task_form.save()
        return redirect('overdue-tasks')

    tasks = Task.objects.filter(user=request.user, completed=False, date__lt=datetime.date.today())
    tasks_amount = tasks.count()

    return output(request, 'tasks/overdue_tasks.html', {
        "Text_of_the_page": "Overdue tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        "edit": True,
        "task": task_info,
    })


def delete_overdue_task(request, task_id: int) -> HttpResponse:
    """
    Deletes an overdue task.

    This view function retrieves the task with the given task_id, deletes it, and redirects the user to the overdue
    tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be deleted.
    :return: HttpResponse: A redirect to the overdue tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.delete()
    return redirect('overdue-tasks')


def today_tasks(request) -> HttpResponse:
    """
    Renders the today tasks page.

    This view function processes GET and POST requests for today's tasks. For GET requests, it renders the today tasks
    page with a list of today's tasks and a form to add new tasks. For POST requests, it processes the submitted form
    data to add a new task.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'today-tasks' page if a new task is successfully added.
        - HttpResponse: Renders the today tasks page with the list of today's tasks and the task form for GET requests.
    """

    submitted = False
    if request.method == "POST":
        task_form = TaskForm(request.POST, user=request.user, initial={'date': datetime.date.today()})
        if task_form.is_valid():
            event = task_form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('today-tasks')
    else:
        task_form = TaskForm(user=request.user, initial={'date': datetime.date.today()})

        if 'submitted' in request.GET:
            submitted = True

    tasks = Task.objects.filter(user=request.user, completed=False, date=datetime.date.today())
    tasks_amount = tasks.count()

    return output(request, 'tasks/today_tasks.html', {
        "Text_of_the_page": "Today tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        'submitted': submitted,
        "edit": False,
    })


def todo_today_task(request, task_id: int) -> HttpResponse:
    """
    Toggles the completion status of a task for today.

    This view function retrieves the task with the given task_id, toggles its completion status, saves the changes,
    and redirects the user to the today tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be toggled.
    :return: HttpResponse: A redirect to the today tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.completed = not task_info.completed
    task_info.save()
    return redirect('today-tasks')


def task_detail_today(request, task_id: int) -> HttpResponse:
    """
    Renders the task detail page for a task scheduled for today.

    This view function retrieves the task with the given task_id, checks if the task belongs to the current user,
    and renders the task detail page. If the task does not belong to the current user, it raises a 404 error.
    If the form is valid, it saves the task and redirects to the today tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be detailed.
    :return: HttpResponse: A redirect to the today tasks page if the form is valid, otherwise renders the task detail
    page.
    """

    task_info = Task.objects.get(pk=task_id)

    if task_info.user != request.user:
        raise Http404("Task does not exist or you do not have permission to view it.")

    task_form = TaskForm(request.POST or None, instance=task_info, user=request.user)

    if task_form.is_valid():
        task_form.save()
        return redirect('today-tasks')

    tasks = Task.objects.filter(user=request.user, completed=False, date=datetime.date.today())
    tasks_amount = tasks.count()

    return output(request, 'tasks/today_tasks.html', {
        "Text_of_the_page": "Today tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        "edit": True,
        "task": task_info,
    })


def delete_today_task(request, task_id: int) -> HttpResponse:
    """
    Deletes a task scheduled for today.

    This view function retrieves the task with the given task_id, deletes it, and redirects the user to the today tasks
    page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be deleted.
    :return: HttpResponse: A redirect to the today tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.delete()
    return redirect('today-tasks')


def all_tasks(request) -> HttpResponse:
    """
    Renders the all tasks page.

    This view function processes GET and POST requests for all tasks. For GET requests, it renders the all tasks
    page with a list of all tasks and a form to add new tasks. For POST requests, it processes the submitted form
    data to add a new task. Also handles the search functionality to filter tasks by title or description.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'all-tasks' page if a new task is successfully added.
        - HttpResponse: Renders the all tasks page with the list of all tasks and the task form for GET requests.
    """

    submitted = False
    if request.method == "POST":
        task_form = TaskForm(request.POST, user=request.user)
        if task_form.is_valid():
            event = task_form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('all-tasks')
    else:
        task_form = TaskForm(user=request.user, initial={'date': datetime.date.today()})

        if 'submitted' in request.GET:
            submitted = True

    search_query = request.GET.get('search', '')
    if search_query:
        tasks = Task.objects.filter(Q(user=request.user) &
                                    Q(completed=False) &
                                    (Q(title__icontains=search_query) |
                                     Q(description__icontains=search_query)))

    else:
        tasks = Task.objects.filter(user=request.user, completed=False)

    tasks_amount = tasks.count()

    return output(request, 'tasks/all_tasks.html', {
        "Text_of_the_page": "All tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        'submitted': submitted,
        "edit": False,
    })


def todo_all_task(request, task_id: int) -> HttpResponse:
    """
    Toggles the completion status of a task.

    This view function retrieves the task with the given task_id, toggles its completion status, saves the changes,
    and redirects the user to the all tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be toggled.
    :return: HttpResponse: A redirect to the all tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.completed = not task_info.completed
    task_info.save()
    return redirect('all-tasks')


def task_detail_all(request, task_id: int) -> HttpResponse:
    """
    Renders the task detail page for a task.

    This view function retrieves the task with the given task_id, checks if the task belongs to the current user,
    and renders the task detail page. If the task does not belong to the current user, it raises a 404 error.
    If the form is valid, it saves the task and redirects to the all tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be detailed.
    :return: HttpResponse: A redirect to the all tasks page if the form is valid, otherwise renders the task detail
    page.
    """

    task_info = Task.objects.get(pk=task_id)

    if task_info.user != request.user:
        raise Http404("Task does not exist or you do not have permission to view it.")

    task_form = TaskForm(request.POST or None, instance=task_info, user=request.user)

    if task_form.is_valid():
        task_form.save()
        return redirect('all-tasks')

    tasks = Task.objects.filter(user=request.user, completed=False)
    tasks_amount = tasks.count()

    return output(request, 'tasks/all_tasks.html', {
        "Text_of_the_page": "All tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        "edit": True,
        "task": task_info,
    })


def delete_all_task(request, task_id: int) -> HttpResponse:
    """
    Deletes a task from the 'all tasks' list.

    This view function retrieves the task with the given task_id, deletes it, and redirects the user to the 'all tasks'
    page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be deleted.
    :return: HttpResponse: A redirect to the 'all tasks' page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.delete()
    return redirect('all-tasks')


def completed_tasks(request) -> HttpResponse:
    """
    Handles the display and submission of completed tasks.

    This view function processes GET and POST requests for completed tasks. For GET requests, it renders the completed
    tasks page with a list of completed tasks and a form to add new tasks. For POST requests, it processes the
    submitted form data to add a new task.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'all-tasks' page if a new task is successfully added.
        - HttpResponse: Renders the completed tasks page with the list of completed tasks and the task form for GET
        requests.
    """

    submitted = False
    if request.method == "POST":
        task_form = TaskForm(request.POST, user=request.user)
        if task_form.is_valid():
            event = task_form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('all-tasks')
    else:
        task_form = TaskForm(user=request.user)

        if 'submitted' in request.GET:
            submitted = True

    tasks = Task.objects.filter(user=request.user, completed=True)
    tasks_amount = tasks.count()

    return output(request, 'tasks/completed_tasks.html', {
        "Text_of_the_page": "Completed Tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        'submitted': submitted,
        "edit": False,
    })


def cancel_todo_task(request, task_id: int) -> HttpResponse:
    """
    Toggles the completion status of a task.

    This view function retrieves the task with the given task_id, toggles its completion status, saves the changes,
    and redirects the user to the completed tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be toggled.
    :return: HttpResponse: A redirect to the completed tasks page.
    """
    task_info = Task.objects.get(pk=task_id)
    task_info.completed = not task_info.completed
    task_info.save()
    return redirect('completed-tasks')


def task_detail_completed(request, task_id: int) -> HttpResponse:
    """
    Renders the task detail page for a completed task.

    This view function retrieves the task with the given task_id, checks if the task belongs to the current user,
    and renders the task detail page. If the task does not belong to the current user, it raises a 404 error.
    If the form is valid, it saves the task and redirects to the completed tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be detailed.
    :return: HttpResponse: A redirect to the completed tasks page if the form is valid, otherwise renders the task
    detail page.
    """

    task_info = Task.objects.get(pk=task_id)

    if task_info.user != request.user:
        raise Http404("Task does not exist or you do not have permission to view it.")

    task_form = TaskForm(request.POST or None, instance=task_info, user=request.user)

    if task_form.is_valid():
        task_form.save()
        return redirect('completed-tasks')

    tasks = Task.objects.filter(user=request.user, completed=True)
    tasks_amount = tasks.count()

    return output(request, 'tasks/completed_tasks.html', {
        "Text_of_the_page": "Completed Tasks",
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        "edit": True,
        "task": task_info,
    })


def delete_completed_task(request, task_id: int) -> HttpResponse:
    """
    Deletes a completed task.

    This view function retrieves the task with the given task_id, deletes it, and redirects the user to the completed
    tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be deleted.
    :return: HttpResponse: A redirect to the completed tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.delete()
    return redirect('completed-tasks')


@login_required
def all_tags(request) -> HttpResponse:
    """
    Function to render the all tags page.

    This view function processes GET and POST requests for the all tags page. For GET requests, it renders the all tags
    page with a list of all tags and a form to add new tags. For POST requests, it processes the submitted form data
    to add a new tag.

    :param request: The HTTP request object containing metadata about the request.
    :returns:
        - HttpResponse: A redirect to the 'all-tags' page if a new tag is successfully added.
        - HttpResponse: Renders the all tags page with the list of all tags and the tag form for GET requests.
    """

    submitted = False
    if request.method == "POST":
        tag_form = TagForm(request.POST)
        if tag_form.is_valid():
            event = tag_form.save(commit=False)
            event.user_id = request.user  # Assign the task to the currently logged-in user
            event.save()
            return redirect('all-tags')
    else:
        tag_form = TagForm()

        if 'submitted' in request.GET:
            submitted = True

    tags = TagTask.objects.filter(user_id=request.user)
    tags_amount = tags.count()

    return output(request, 'tasks/tags.html', {
        "Text_of_the_page": "Tags",
        "amount": tags_amount,
        "content_to_unpack": tags,
        "form": tag_form,
        'submitted': submitted,
        "edit": False,
    })


@login_required
def tag(request, tag_id: int) -> HttpResponse:
    """
    Function to render the tag page.

    This view function retrieves the tag with the given tag_id, checks if the tag belongs to the current user,
    and renders the tag page. If the tag does not belong to the current user, it raises a 404 error.

    :param request: The HTTP request object containing metadata about the request.
    :param tag_id: The ID of the tag to be rendered.
    :return: HttpResponse: Renders the tag page with the tag details and form.
    """

    tag_info = TagTask.objects.get(pk=tag_id)

    if tag_info.user_id != request.user:
        raise Http404("Task does not exist or you do not have permission to view it.")

    tag_form = TagForm(request.POST or None, instance=tag_info)

    if tag_form.is_valid():
        tag_form.save()
        return redirect('all-tags')

    tags = TagTask.objects.filter(user_id=request.user)
    tags_amount = tags.count()

    return output(request, 'tasks/tags.html', {
        "Text_of_the_page": "Tags",
        "amount": tags_amount,
        "content_to_unpack": tags,
        "form": tag_form,
        "edit": True,
        "tag": tag_info,
    })


def delete_tag(request, tag_id: int) -> HttpResponse:
    """
    Deletes a tag.

    This view function retrieves the tag with the given tag_id, deletes it, and redirects the user to the all tags page.

    :param request: The HTTP request object containing metadata about the request.
    :param tag_id: The ID of the tag to be deleted.
    :return: HttpResponse: A redirect to the all tags page.
    """

    tag_info = TagTask.objects.get(pk=tag_id)
    tag_info.delete()
    return redirect('all-tags')


@login_required
def tag_filter(request, tag_id: int) -> HttpResponse:
    """
    Filters tasks by a specific tag.

    This view function processes GET and POST requests to filter tasks by a given tag. For GET requests, it renders the
    filtered tasks page with a list of tasks associated with the specified tag. For POST requests, it processes the
    submitted form data to add a new task under the specified tag.

    :param request: The HTTP request object containing metadata about the request.
    :param tag_id: The ID of the tag to filter tasks by.
    :return: HttpResponse: Renders the filtered tasks page with the list of tasks and the task form.
    """

    submitted = False
    if request.method == "POST":
        task_form = TaskTagForm(request.POST, user=request.user, tag_id=tag_id)
        if task_form.is_valid():
            event = task_form.save(commit=False)
            event.user = request.user  # Assign the task to the currently logged-in user
            event.save()
            return redirect('fiter-by-tag', tag_id=tag_id)
    else:
        task_form = TaskTagForm(user=request.user, tag_id=tag_id)

        if 'submitted' in request.GET:
            submitted = True

    tasks = Task.objects.filter(tag_id=tag_id, user=request.user, completed=False)
    tasks_amount = tasks.count()

    tag_info = TagTask.objects.get(pk=tag_id)

    return output(request, 'tasks/filter_by_tag.html', {
        "Text_of_the_page": tag_info.tag_name,
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        "edit": False,
        "tag": tag_info,
        'submitted': submitted,
    })


def todo_filtered_task(request, task_id: int) -> HttpResponse:
    """
    Toggles the completion status of a filtered task.

    This view function retrieves the task with the given task_id, toggles its completion status, saves the changes,
    and redirects the user to the filtered tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be toggled.
    :return: HttpResponse: A redirect to the filtered tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.completed = not task_info.completed
    task_info.save()
    return redirect('fiter-by-tag', tag_id=TagTask.objects.get(tag_name=task_info.tag).id)


def delete_filtered_task(request, task_id: int) -> HttpResponse:
    """
    Deletes a filtered task.

    This view function retrieves the task with the given task_id, deletes it, and redirects the user to the filtered
    tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param task_id: The ID of the task to be deleted.
    :return: HttpResponse: A redirect to the filtered tasks page.
    """

    task_info = Task.objects.get(pk=task_id)
    task_info.delete()
    return redirect('fiter-by-tag', tag_id=TagTask.objects.get(tag_name=task_info.tag).id)


@login_required
def tag_filter_task(request, tag_id: int, task_id: int) -> HttpResponse:
    """
    Renders the task detail page for a task filtered by a specific tag.

    This view function retrieves the task with the given task_id, checks if the task belongs to the current user,
    and renders the task detail page. If the task does not belong to the current user, it raises a 404 error.
    If the form is valid, it saves the task and redirects to the filtered tasks page.

    :param request: The HTTP request object containing metadata about the request.
    :param tag_id: The ID of the tag to filter tasks by.
    :param task_id: The ID of the task to be detailed.
    :return: HttpResponse: A redirect to the filtered tasks page if the form is valid, otherwise renders the task
    detail page.
    """

    task_info = Task.objects.get(pk=task_id)

    # Check if the task belongs to the current user
    if task_info.user != request.user:
        raise Http404("Task does not exist or you do not have permission to view it.")

    task_form = TaskForm(request.POST or None, instance=task_info, user=request.user)

    if task_form.is_valid():
        task_form.save()
        return redirect('fiter-by-tag', tag_id=tag_id)

    tasks = Task.objects.filter(user=request.user, tag_id=tag_id, completed=False)
    tasks_amount = tasks.count()

    tag_info = TagTask.objects.get(pk=tag_id)

    return output(request, 'tasks/filter_by_tag.html', {
        "Text_of_the_page": tag_info.tag_name,
        "amount": tasks_amount,
        "content_to_unpack": tasks,
        "form": task_form,
        "edit": True,
        "tag": tag_info,
        "task": task_info,
    })
