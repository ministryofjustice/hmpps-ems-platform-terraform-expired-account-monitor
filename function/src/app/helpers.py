import datetime
import fileinput
from time import sleep
from typing import Any, List

from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from pydantic import BaseModel

from src.app.config import Config
from src.app.models import CredentialReport, User

logger = Logger(service="expired-account-monitor")


# Utility function to generate pydantic models from args (normally kwargs)
def populate_model_from_args(model: BaseModel, args: List[Any]):
    return model(**{field: arg for field, arg in zip(model.model_fields, args)})


def get_credential_report(iam_client) -> CredentialReport:
    iam_client.generate_credential_report()
    success = False
    retry_limit = Config.get("get_credential_report_retry_limit")
    retries = 0

    while not success and retries < retry_limit:
        try:
            iam_client.get_credential_report()
            success = True
        except Exception as e:
            logger.info(e)
            sleep(1)
        finally:
            retries = retries + 1

    if retries == retry_limit:
        raise Exception(f"Unable to get credential report after {retries} attempts")

    logger.info(f"Got credential report after {retries} attempts")

    response = iam_client.get_credential_report()
    content = response["Content"].decode("utf8").strip()
    rows = content.split("\n")
    body = rows[1:]
    users = [populate_model_from_args(User, row.split(",")) for row in body]

    return CredentialReport(users=users)


def has_never_logged_in(user: User) -> bool:
    return user.password_last_used in ("N/A", "no_information", False)


def has_exceeded_inactivity_deletion_threshold(
    user: User, inactivity_threshold: int
) -> bool:
    if isinstance(user.password_last_used, datetime.date):
        dt_since_login = datetime.datetime.now() - user.password_last_used.replace(
            tzinfo=None
        )
        days_since_login = dt_since_login.days

        return days_since_login > inactivity_threshold

    return False


def has_not_logged_in_within_account_expiry_limit_since_account_creation(
    user: User, inactivity_threshold: int
) -> bool:
    if isinstance(user.user_creation_time, datetime.date):
        dt_since_login = datetime.datetime.now() - user.user_creation_time.replace(
            tzinfo=None
        )
        days_since_login = dt_since_login.days

        return days_since_login > inactivity_threshold

    return False


def account_deletion_date_reached(
    user: User,
    inactivity_threshold: int,
):
    # Holds account on the system from ninety days since account creation
    if has_never_logged_in(user):
        if has_not_logged_in_within_account_expiry_limit_since_account_creation(
            user, inactivity_threshold
        ):
            return True

    if has_exceeded_inactivity_deletion_threshold(user, inactivity_threshold):
        return True

    return False
