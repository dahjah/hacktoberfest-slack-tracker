from rest_framework import serializers
from .models import UserConfig


class UserConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserConfig
        fields = ['name', 'watch_for_pull_requests', 'notify_count_in_slack']