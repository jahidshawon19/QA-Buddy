

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import Task, Checklist, ProductManager, Developer
from .forms import TaskForm, ChecklistForm, UserCreateForm, ProductManagerForm, DeveloperForm
from django.db.models import Q

# from django.contrib.auth.views import LoginView
# from django.contrib import messages






# Mixin to restrict views to staff users only
class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# ------------------------------------
# Task Views - accessible by all logged-in users
# ------------------------------------
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'checklist/task_list.html'
    context_object_name = 'tasks'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'checklist/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'checklist/task_form.html'
    success_url = reverse_lazy('task_list')


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'checklist/confirm_delete.html'
    success_url = reverse_lazy('task_list')


# ------------------------------------
# Checklist Views - accessible by all logged-in users
# ------------------------------------
class ChecklistListView(LoginRequiredMixin, ListView):
    model = Checklist
    template_name = 'checklist/checklist_list.html'
    context_object_name = 'checklists'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sprint = self.request.GET.get('sprint')
        search = self.request.GET.get('search')

        if sprint:
            queryset = queryset.filter(task__sprint_no=sprint)
        if search:
            queryset = queryset.filter(task__task_name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sprints'] = Task.objects.values_list('sprint_no', flat=True).distinct()
        return context

class ChecklistCreateView(LoginRequiredMixin, CreateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'checklist/checklist_form.html'
    success_url = reverse_lazy('checklist_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        if obj.task:
            obj.sprint = obj.task.sprint_no
        obj.save()
        return redirect(self.success_url)


class ChecklistUpdateView(LoginRequiredMixin, UpdateView):
    model = Checklist
    form_class = ChecklistForm
    template_name = 'checklist/checklist_form.html'
    success_url = reverse_lazy('checklist_list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.task:
            obj.sprint = obj.task.sprint_no
        obj.save()
        return redirect(self.success_url)


class ChecklistDeleteView(LoginRequiredMixin, DeleteView):
    model = Checklist
    template_name = 'checklist/confirm_delete.html'
    success_url = reverse_lazy('checklist_list')


# ------------------------------------
# Product Manager CRUD Views - staff only
# ------------------------------------
class ProductManagerListView(StaffRequiredMixin, ListView):
    model = ProductManager
    template_name = 'checklist/pm_list.html'
    context_object_name = 'pms'


class ProductManagerCreateView(StaffRequiredMixin, CreateView):
    model = ProductManager
    form_class = ProductManagerForm
    template_name = 'checklist/pm_form.html'
    success_url = reverse_lazy('pm_list')


class ProductManagerUpdateView(StaffRequiredMixin, UpdateView):
    model = ProductManager
    form_class = ProductManagerForm
    template_name = 'checklist/pm_form.html'
    success_url = reverse_lazy('pm_list')


class ProductManagerDeleteView(StaffRequiredMixin, DeleteView):
    model = ProductManager
    template_name = 'checklist/confirm_delete.html'
    success_url = reverse_lazy('pm_list')


# ------------------------------------
# Developer CRUD Views - staff only
# ------------------------------------
class DeveloperListView(StaffRequiredMixin, ListView):
    model = Developer
    template_name = 'checklist/dev_list.html'
    context_object_name = 'devs'


class DeveloperCreateView(StaffRequiredMixin, CreateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'checklist/dev_form.html'
    success_url = reverse_lazy('dev_list')


class DeveloperUpdateView(StaffRequiredMixin, UpdateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'checklist/dev_form.html'
    success_url = reverse_lazy('dev_list')


class DeveloperDeleteView(StaffRequiredMixin, DeleteView):
    model = Developer
    template_name = 'checklist/confirm_delete.html'
    success_url = reverse_lazy('dev_list')


# ------------------------------------
# User Management Views - staff only
# ------------------------------------
class UserListView(StaffRequiredMixin, ListView):
    model = User
    template_name = 'checklist/user_list.html'
    context_object_name = 'users'


class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'checklist/user_form.html'
    success_url = reverse_lazy('user_list')


class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
    template_name = 'checklist/user_form.html'
    success_url = reverse_lazy('user_list')


class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = User
    template_name = 'checklist/confirm_delete.html'
    success_url = reverse_lazy('user_list')




# class CustomLoginView(LoginView):
#     def form_valid(self, form):
#         messages.success(self.request, "Assalamulaikum")
#         return super().form_valid(form)