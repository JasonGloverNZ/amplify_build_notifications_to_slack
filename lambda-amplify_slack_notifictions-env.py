import urllib3
import json

http = urllib3.PoolManager()

# ENV VARS
slack_webhook_url = "https://hooks.slack.com/services/xxxxxxxxxxxxxxxx/yyyyyyyyyyyyyyy/zzzzzzzzzzzzzz"
slack_channel = "#feed-deployments-to-prod"
amplify_apps = [
        ["d8at6dhtsptot0", "user-app"],
        ["d3x67dtu9vhib0", "admin-console"],
        ["d7df23dw79hib0", "partner-app"]
    ]


def app_name_from_event_message(eventMsg):
    for amplify_app_code, app_friendly_name in amplify_apps:
        if amplify_app_code in eventMsg:
            return app_friendly_name

    return "UNKNOWN"


def get_status_from_event_message(eventMsg):
    if "Your build status is STARTED" in eventMsg:
        return "STARTED"
    elif "Your build status is FAILED" in eventMsg:
        return "FAILED"
    elif "Your build status is SUCCEED" in eventMsg:
        return "SUCCEED"
    else:
        return "UNKNOWN"

        
def get_build_details_from_message(eventMsg):
    start_index = eventMsg.find("Go to https://console.aws.amazon.com")
    if start_index != -1:
        return eventMsg[start_index:]
    else:
        return "UNKNOWN"


def emoji_from_status(status):
    if status == "STARTED":
        return ":building_construction:"
    elif status == "FAILED":
        return ":skull:"
    elif status == "SUCCEED":
        return ":white_check_mark:"
    else:
        return "UNKNOWN"

    
def format_build_event_message(appName, buildStatus, forMoreDetails):
    statusEmoji = emoji_from_status(buildStatus)
    return f"{statusEmoji} Amplify build status of {buildStatus} for [{appName}]\n\n{forMoreDetails}"


def lambda_handler(event, context):
    eventMsg = event["Records"][0]["Sns"]["Message"]
    appName = app_name_from_event_message(eventMsg)
    buildStatus = get_status_from_event_message(eventMsg)
    forMoreDetails = get_build_details_from_message(eventMsg)
    msg = {
        "channel": slack_channel,
        "username": "WEBHOOK_USERNAME",
        "text": format_build_event_message(appName, buildStatus, forMoreDetails),
        "icon_emoji": ":awslogo:",
    }
    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", slack_webhook_url, body=encoded_msg)
    print(
        {
            "message": f"App [{appName}] {eventMsg}",
            "status_code": resp.status,
            "response": resp.data,
        }
    )
