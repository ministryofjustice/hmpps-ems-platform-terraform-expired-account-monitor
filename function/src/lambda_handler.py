import boto3
from aws_lambda_powertools import Logger

from src.app.config import Config
from src.app.helpers import (account_deletion_date_reached,
                             get_credential_report)

iam_client = boto3.client("iam")
logger = Logger(service="APP")
inactivity_threshold = Config.get("inactivity_threshold_days")
exempted_users = Config.get("exempted_users")


@logger.inject_lambda_context(log_event=True)
def handle_event(event, context):
    credential_report = get_credential_report(iam_client)
    users = credential_report.users

    logger.info(f"Found {len(users)} user accounts.")

    inactive_console_users_for_deletion = [
        user
        for user in users
        if account_deletion_date_reached(user, inactivity_threshold)
        and user.username not in exempted_users
    ]

    logger.info(
        f"Found {len(inactive_console_users_for_deletion)} inactive user accounts for deletion."
    )

    for user in inactive_console_users_for_deletion:
        logger.info(
            f"{user.username} is inactive, last console login: {user.password_last_used}"
        )

    return [user.username for user in inactive_console_users_for_deletion]
