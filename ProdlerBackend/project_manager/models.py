from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
# Create your models here.


class Project(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_crated_by')
    name = models.TextField(max_length=225, blank=False, null=False)
    project_members = models.ManyToManyField(User)
    created_on = models.DateField(default=timezone.now)
    tags = ArrayField(models.CharField(max_length=225, default=''), blank=True)

    def __str__(self):
        return self.name

    objects = models.Manager()

    @staticmethod
    def verify_project_name(project_name, user):
        if Project.objects.filter(admin=user).filter(name=project_name).exists():
            return True
        else:
            return False


class Milestones(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='milestone_created_by')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project', default='')
    title = models.CharField(max_length=225, default='', null=False)
    created_date = models.DateField(default=timezone.now)
    deadline = models.DateField(default=None, blank=False)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    objects = models.Manager()


class Issues(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_created_by', default=0)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='project', default=0, null=True, blank=True)
    milestone = models.ForeignKey(Milestones, on_delete=models.CASCADE, verbose_name='milestone', default=0, null=True, blank=True)
    title = models.CharField(max_length=225, default='', null=False)
    details = models.CharField(max_length=1000, default='')
    created_on = models.DateField(default=timezone.now)
    tags = models.CharField(max_length=225, blank=True, null=True, default='')

    def __str__(self):
        return self.title

    objects = models.Manager()


class Comments(models.Model):
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='issue_comment_by')
    text = models.CharField(max_length=500, default='', blank=True)
    comment_date = models.DateField(default=timezone.now)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE, verbose_name='issue', default='')

    def __str__(self):
        return self.text

    objects = models.Manager()
