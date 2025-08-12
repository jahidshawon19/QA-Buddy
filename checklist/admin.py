from django.contrib import admin
from .models import ProductManager, Developer, Task, Checklist

@admin.register(ProductManager)
class ProductManagerAdmin(admin.ModelAdmin):
    list_display = ('sl_no', 'name')

@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('sl_no', 'name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('sl_no', 'task_name', 'sprint_no')

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('sl_no', 'task', 'test_area', 'status', 'retest_status', 'sprint', 'created_by')
    list_filter = ('status', 'retest_status', 'sprint')
    search_fields = ('task__task_name', 'test_area', 'created_by__username')