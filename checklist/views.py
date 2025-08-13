

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Task, Checklist, ProductManager, Developer
from .forms import TaskForm, ChecklistForm, UserCreateForm, ProductManagerForm, DeveloperForm
from django.db.models import Q

from django.shortcuts import render
from django.db.models import Count


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
# class ChecklistListView(LoginRequiredMixin, ListView):
#     model = Checklist
#     template_name = 'checklist/checklist_list.html'
#     context_object_name = 'checklists'
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sprint = self.request.GET.get('sprint')
#         search = self.request.GET.get('search')

#         if sprint:
#             queryset = queryset.filter(task__sprint_no=sprint)
#         if search:
#             queryset = queryset.filter(task__task_name__icontains=search)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['sprints'] = Task.objects.values_list('sprint_no', flat=True).distinct()
#         return context



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Checklist, Task

class ChecklistListView(LoginRequiredMixin, ListView):
    model = Checklist
    template_name = 'checklist/checklist_list.html'
    context_object_name = 'checklists'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Restrict normal users to only their own checklists
        if not self.request.user.is_staff:
            queryset = queryset.filter(created_by=self.request.user)

        sprint = self.request.GET.get('sprint')
        search = self.request.GET.get('search')

        if sprint:
            queryset = queryset.filter(task__sprint_no=sprint)
        if search:
            queryset = queryset.filter(task__task_name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sprints'] = Task.objects.values_list('sprint_no', flat=True).distinct().order_by('sprint_no')
        context['selected_sprint'] = self.request.GET.get('sprint', '')
        context['search_query'] = self.request.GET.get('search', '')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_name'] = self.model._meta.verbose_name
        return context    


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

@login_required
def cover_page(request):
    selected_sprint = request.GET.get("sprint", "")

    # Get all sprints from Task table (or Sprint model if you have one)
    sprints = Task.objects.values_list("sprint_no", flat=True).distinct().order_by("sprint_no")

    # Filter checklists by selected sprint
    checklists = Checklist.objects.all()
    if selected_sprint:
        checklists = checklists.filter(task__sprint_no=selected_sprint)

    # Group by sprint and created_by user
    grouped_data = (
        checklists
        .values("task__sprint_no", "created_by__username")
        .annotate(total_checklists=Count("sl_no"))
        .order_by("task__sprint_no", "created_by__username")
    )

    # Organize data into nested dict { sprint_no: [ {user, total}, ... ] }
    sprint_summary = {}
    for item in grouped_data:
        sprint_no = item["task__sprint_no"]
        username = item["created_by__username"]
        total = item["total_checklists"]

        if sprint_no not in sprint_summary:
            sprint_summary[sprint_no] = []
        sprint_summary[sprint_no].append({"user": username, "total": total})

    context = {
        "sprints": sprints,
        "selected_sprint": selected_sprint,
        "sprint_summary": sprint_summary
    }
    return render(request, "checklist/cover_page.html", context)
    