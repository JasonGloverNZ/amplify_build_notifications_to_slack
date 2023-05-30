# amplify_build_notifications_to_slack

A python 3.7 compatible lambda function that can be used to process Amplify build notification SNS topics and send a formatting message to a specified slack channel.

You'll need to create a webhook in Slack.

The function can map the meaningless Amplify codes into a "friendly name" for your apps.  Very useful if you have more than one.
