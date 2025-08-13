from django.db import models
from django.conf import settings

class ProductManager(models.Model):
    sl_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Developer(models.Model):
    sl_no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Task(models.Model):
    sl_no = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=255)
    sprint_no = models.IntegerField()

    def __str__(self):
        return f"{self.task_name} (Sprint {self.sprint_no})"
    
    def __str__(self):
        return str(self.sprint_no)

class Checklist(models.Model):
    STATUS_CHOICES = [
        ('PASSED', 'PASSED'),
        ('NOT_EXECUTED', 'NOT EXECUTED'),
        ('FAILED', 'FAILED'),
    ]

    sl_no = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='checklists')
    test_area = models.CharField(max_length=255)
    test_scenario = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_checklists')
    approved_by_PM = models.ForeignKey(ProductManager, on_delete=models.SET_NULL, null=True, blank=True)
    approved_by_dev = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_EXECUTED')
    # NOTE: I used 'retest_status' (assumed from your earlier messages)
    retest_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_EXECUTED')
    actual_evidence = models.URLField(max_length=500, blank=True)
    bug_link = models.URLField(max_length=500, blank=True)
    # store sprint number (derived from task.sprint_no on save)
    sprint = models.IntegerField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.task:
            self.sprint = self.task.sprint_no
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Checklist #{self.sl_no} - {self.task.task_name}"