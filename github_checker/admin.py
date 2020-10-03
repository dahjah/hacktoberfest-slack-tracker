from django.contrib import admin
from .models import (PullRequest, GithubUserConfig,
                     SlackOrg, SlackUserConfig,
                     UserConfig, NotificationSettings)

# Register your models here.
@admin.register(PullRequest)
class PRAdmin(admin.ModelAdmin):
    pass

@admin.register(GithubUserConfig)
class GithubUserConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(SlackOrg)
class SlackOrgAdmin(admin.ModelAdmin):
    pass

@admin.register(SlackUserConfig)
class SlackUserConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    pass