import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths

logger = Logger(service="expired-account-monitor")


class Config:
    __conf = {
        "inactivity_threshold_days": 90,
        "default_region": "eu-west-2",
        "get_credential_report_retry_limit": 5,
        "exempted_users": [
            "<root_account>",
            "hmpps-g4s-preprod-gdpr-data-upload-service-user",
            "hmpps-g4s-prod-gdpr-data-upload-service-user",
            "hmpps-iam-central-monitoring",
            "terraform-service-user",
            "hmpps_serco_ac_service_user",
        ],
    }

    @staticmethod
    def get(name):
        value = None

        logger.debug("Retrieving config value for key {0}".format(name))
        if name in Config.__conf:
            value = Config.__conf[name]

        value = os.environ.get(name, value)

        if value is None:
            raise KeyError(
                "Could not retrieve configuration value for [{0}]".format(name)
            )

        return value
