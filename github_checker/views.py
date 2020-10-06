from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, mixins
from .models import (UserConfig, GithubUserConfig, NotificationSetting,
                     SlackOrg, ConnectionUserConfig, UserConfig)
from .serializers import UserConfigSerializer, SlackSerializer
from .tasks import get_user_github, check_user_and_update
from rest_framework.response import Response
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.decorators import action, renderer_classes
import requests
from django.conf import settings


# Create your views here.

class SlackViewset(viewsets.ViewSet):

    queryset = SlackOrg.objects.all()
    serializer_class = SlackSerializer

    @action(detail=False, methods=['post'], url_path="interact")
    @csrf_exempt
    def interact(self, request):
        print("Interact called!")
        print(request)
        print(request.POST)
        modal_body = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "Github Pull Request Settings",
                        "emoji": true
                    }
                },
                {
                    "type": "input",
                    "block_id": "input123",
                    "label": {
                        "type": "plain_text",
                        "text": "Github Username"
                    },
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "github_username",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "github username"
                        }
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Options"
                    },
                    "accessory": {
                        "type": "checkboxes",
                        "options": [
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Enable Checking Github for New Contributions"
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "enables scanning of github for new pull requests"
                                },
                                "value": "watch_for_pull_requests"
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Show new Pull Requests in Slack"
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "post new pull requests in slack as soon as they are found"
                                },
                                "value": "notify_count_in_slack"
                            }
                        ],
                        "initial_options": [
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Enable Checking Github for New Contributions"
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "enables scanning of github for new pull requests"
                                },
                                "value": "watch_for_pull_requests"
                            },
                            {
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "Show new Pull Requests in Slack"
                                },
                                "description": {
                                    "type": "mrkdwn",
                                    "text": "post new pull requests in slack as soon as they are found"
                                },
                                "value": "notify_count_in_slack"
                            }
                        ]
                    }
                }
            ]
        }
        return Response(modal_body)

    def complete_oauth(self, code):
        params = {
            "code": code,
            "client_id": settings.SLACK_CLIENT_ID,
            "client_secret": settings.SLACK_CLIENT_SECRET,
            "redirect_uri": settings.SLACK_CLIENT_REDIRECT_URI,
        }
        resp = requests.post("https://slack.com/api/oauth.v2.access",
                             data=params)
        print(resp.json())
        return resp.json()

    @action(detail=False, methods=['get'], url_path="oauth")
    @renderer_classes([StaticHTMLRenderer])
    @csrf_exempt
    def oauth(self, request):
        print("Oauth called!")
        print(request)
        print(request.POST)
        resp = self.complete_oauth(request.GET.get("code"))
        if resp.get("ok"):
            slack_org, created = SlackOrg.objects.get_or_create(
                team_id=resp.get("team", {}).get("id"),
                defaults={"name": resp.get("team", {}).get("name"),
                          "bot_user_id": resp.get("bot_user_id"),
                          "bot_access_token": resp.get("access_token")})
            return Response("Slack Org Successfully" +
                            f"{'created' if created else 'updated'}!" +
                            "You may safely close this window."
                            )
        return Response()


class RegisteredUsersViewset(viewsets.ModelViewSet):

    queryset = UserConfig.objects.all()
    serializer_class = UserConfigSerializer

    @action(detail=False, methods=['post'], url_path='register')
    @csrf_exempt
    def register(self, request):
        team_id = request.POST.get('team_id')
        slack_org = SlackOrg.objects.filter(team_id=team_id)[0]
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        resp_url = request.POST.get('response_url')
        text = request.POST.get('text')
        # Grab defaults TODO: allow user to choose this in a slack dialog box
        notif_settings = NotificationSetting.objects.all()[0]
        github_details = get_user_github(text.strip())
        if not github_details:
            return Response(f"Unable to find github user: {text}")  # Respond 200 so slack doesn't report error
        print(github_details)
        github_user, gh_created = GithubUserConfig.objects.get_or_create(
            id=github_details.get("id"), defaults=github_details)
        print(github_user)
        user_config, u_created = UserConfig.objects.get_or_create(
            name=github_details.get("name"), github_user=github_user,
            defaults={
                "watch_for_pull_requests": True,
                "notify_count_in_slack": True
            })
        slack_user_config, sc = ConnectionUserConfig.objects.get_or_create(
            slack_id=user_id, defaults={"slack_name": user_name,
                                        "slack_id": user_id,
                                        "slack_org": slack_org,
                                        "notification_settings": notif_settings
                                        }
        )
        user_config.conn_configs.add(slack_user_config)
        print(f"Getting and updating for user: {user_config}")
        check_user_and_update(user_config)
        requests.post(resp_url, {"response_type": "ephemeral",
                                 "text": "Successfully Subscribed!"})
        return Response({"response_type": "ephemeral",
                         "text": f"<@{user_id}> successfully registered {text} for tracking!"
                         })

    @action(detail=False, methods=['post'], url_path='edit')
    @csrf_exempt
    def editRegsitration(self, request):
        pass