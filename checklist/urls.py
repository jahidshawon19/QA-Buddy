from django.urls import path
from . import views

urlpatterns = [
    # Task URLs (accessible by any authenticated user)
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/add/', views.TaskCreateView.as_view(), name='task_add'),
    path('tasks/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # Checklist URLs
    path('checklists/', views.ChecklistListView.as_view(), name='checklist_list'),
    path('checklists/add/', views.ChecklistCreateView.as_view(), name='checklist_add'),
    path('checklists/<int:pk>/edit/', views.ChecklistUpdateView.as_view(), name='checklist_edit'),
    path('checklists/<int:pk>/delete/', views.ChecklistDeleteView.as_view(), name='checklist_delete'),

    # Product Manager URLs (staff only)
    path('pms/', views.ProductManagerListView.as_view(), name='pm_list'),
    path('pms/add/', views.ProductManagerCreateView.as_view(), name='pm_add'),
    path('pms/<int:pk>/edit/', views.ProductManagerUpdateView.as_view(), name='pm_edit'),
    path('pms/<int:pk>/delete/', views.ProductManagerDeleteView.as_view(), name='pm_delete'),

    # Developer URLs (staff only)
    path('devs/', views.DeveloperListView.as_view(), name='dev_list'),
    path('devs/add/', views.DeveloperCreateView.as_view(), name='dev_add'),
    path('devs/<int:pk>/edit/', views.DeveloperUpdateView.as_view(), name='dev_edit'),
    path('devs/<int:pk>/delete/', views.DeveloperDeleteView.as_view(), name='dev_delete'),

    # User Management URLs (staff only)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # Home redirect - show Checklist list
    path('', views.ChecklistListView.as_view(), name='home'),

     path("cover/", views.cover_page, name="cover_page"),
]
