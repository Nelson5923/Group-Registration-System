from django.contrib import admin
from GroupMatchingModel.models import Membership, Project, Group, Profile

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'min_member', 'max_member', 'deadline', 'description')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('project', 'group_name', 'description')

# Register your models here.
admin.site.register(Membership)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Profile)