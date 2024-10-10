from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    # Path Converters
    # int: numbers
    # str: strings
    # path: whole urls /
    # slug: hyphen-and_underscores_stuff
    # UUID: universally unique identifier

    # Home Page
    path('', views.all_tasks),

    # All Tasks pages
    path('tasks', views.all_tasks, name="all-tasks"),  # all tasks
    path('todo_task/<task_id>', views.todo_all_task, name='todo-all-task'),  # todo all task
    path('task/<int:task_id>', views.task_detail_all, name='all-task-detail'),  # task detail
    path('delete_task/<task_id>', views.delete_all_task, name='delete-all-task'),  # delete task

    # Overdue Tasks pages
    path('overdue_tasks', views.overdue_tasks, name='overdue-tasks'),  # overdue tasks
    path('todo_overdue_task/<task_id>', views.todo_overdue_task, name='todo-overdue-task'),  # todo overdue task
    path('overdue_task/<int:task_id>', views.task_detail_overdue, name='overdue-task-detail'),  # overdue task detail
    path('delete_overdue_task/<task_id>', views.delete_overdue_task, name='delete-overdue-task'),  # delete overdue task

    # Today Tasks pages
    path('today_tasks', views.today_tasks, name='today-tasks'),  # today tasks
    path('todo_today_task/<task_id>', views.todo_today_task, name='todo-today-task'),  # todo today task
    path('today_task/<int:task_id>', views.task_detail_today, name='today-task-detail'),  # today task detail
    path('delete_today_task/<task_id>', views.delete_today_task, name='delete-today-task'),  # delete today task

    # Completed Tasks pages
    path('Completed', views.completed_tasks, name='completed-tasks'),  # completed tasks
    path('cancel_todo_task/<task_id>', views.cancel_todo_task, name='cancel-todo-task'),  # cancel todo task
    path('completed_task/<int:task_id>', views.task_detail_completed, name='completed-task-detail'),  # completed task detail
    path('delete_completed_task/<task_id>', views.delete_completed_task, name='delete-completed-task'),  # delete completed task

    # Tags pages
    path('all_tags', views.all_tags, name="all-tags"),  # all tags
    path('tag/<tag_id>', views.tag, name="tag-detail"),  # tag detail
    path('delete_tag/<tag_id>', views.delete_tag, name="delete-tag"),  # delete tag
    path('todo_filtered_task/<task_id>', views.todo_filtered_task, name='todo-filtered-task'),  # todo filtered task
    path('delete_tagged_task/<task_id>', views.delete_filtered_task, name='delete-filtered-task'),  # delete filtered task
    path('fiter_by_tag/<tag_id>', views.tag_filter, name='fiter-by-tag'),  # filter by tag
    path('tag_filter_task/<str:tag_id>/<int:task_id>/', views.tag_filter_task, name='tag-filter-task'),  # tag filter task
]
