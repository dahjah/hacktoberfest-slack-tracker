from django.contrib import admin
from .models import (PullRequest, GithubUserConfig,
                     SlackOrg, ConnectionUserConfig,
                     UserConfig, NotificationSetting)

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

@admin.register(ConnectionUserConfig)
class ConnectionUserConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(UserConfig)
class UserConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(NotificationSetting)
class NotificationSettingsAdmin(admin.ModelAdmin):
    pass