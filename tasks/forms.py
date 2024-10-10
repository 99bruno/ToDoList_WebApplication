from django import forms
from django.forms import ModelForm
from .models import Task, TagTask


class TaskForm(ModelForm):
    """
    A form for creating and updating Task instances.

    This form includes fields for the task's title, description, tag, and date. It also customizes the queryset
    for the tag field to only include tags associated with the current user.

    Attributes:
        Meta: A class that defines the model and fields used in the form.
        __init__: Initializes the form and customizes the tag field's queryset based on the user.
    """

    class Meta:
        """
        Metaclass to specify the model and fields to be used in the form.
        """

        model = Task
        fields = ['title', 'description', 'tag', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tag': forms.Select(attrs={'class': 'form-select custom-tag-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the TaskForm.

        This method customizes the queryset for the tag field to only include tags associated with the current user.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments, including the current user.
        """

        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['tag'].queryset = TagTask.objects.filter(user_id=user)


class TaskTagForm(ModelForm):
    """
    A form for creating and updating Task instances with a specific tag.

    This form includes fields for the task's title, description, tag, and date. It customizes the queryset
    for the tag field to only include tags associated with the current user and sets the initial tag value.

    Attributes:
        Meta: A class that defines the model and fields used in the form.
        __init__: Initializes the form, customizes the tag field's queryset based on the user, and sets the initial tag value.
    """

    class Meta:
        """
        Metaclass to specify the model and fields to be used in the form.
        """

        model = Task
        fields = ['title', 'description', 'tag', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tag': forms.Select(attrs={'class': 'form-select custom-tag-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Initializes the TaskTagForm.

        This method customizes the queryset for the tag field to only include tags associated with the current user
        and sets the initial value for the tag field.

        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments, including the current user and tag_id.
        """

        user = kwargs.pop('user', None)
        tag_id = kwargs.pop('tag_id', None)
        super(TaskTagForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['tag'].queryset = TagTask.objects.filter(user_id=user)
        self.fields['tag'].initial = tag_id
        self.fields['tag'].initial = tag_id


class TagForm(ModelForm):
    """
    A form for creating and updating TagTask instances.

    This form includes a field for the tag's name and customizes the widget for better styling with Bootstrap.

    Attributes:
        Meta: A class that defines the model and fields used in the form.
    """

    class Meta:
        """
        Metaclass to specify the model and fields to be used in the form.
        """

        model = TagTask
        fields = ['tag_name']
        widgets = {
            'tag_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
