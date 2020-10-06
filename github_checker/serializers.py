from rest_framework import serializers
from .models import UserConfig, SlackOrg


class SlackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SlackOrg
        fields = ['name']


class UserConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserConfig
        fields = ['name']