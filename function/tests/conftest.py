import datetime
import os
from unittest.mock import MagicMock

import boto3
import pytest
from moto import mock_aws

from src.app.config import Config
from src.app.models import User


@pytest.fixture
def recently_created_user_with_no_logins():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-07-30T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="N/A",
        password_last_changed="2023-08-30T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="FALSE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def recently_created_user_with_no_information_on_logins():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-07-30T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="no_information",
        password_last_changed="2023-08-30T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="FALSE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def not_recently_created_user_with_no_logins():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-01-01T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="N/A",
        password_last_changed="2023-01-01T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="FALSE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def not_recently_created_user_with_no_information_on_logins():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-01-01T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="no_information",
        password_last_changed="2023-01-01T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="FALSE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def disabled_user_account_less_than_one_month_old():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-07-04T00:00:00+00:00",
        password_enabled="FALSE",
        password_last_used="2023-07-04T00:00:00+00:00",
        password_last_changed="N/A",
        password_next_rotation="N/A",
        mfa_active="TRUE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def active_user():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-07-01T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="2023-07-04T00:00:00+00:00",
        password_last_changed="2023-07-02T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="TRUE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def recently_reenabled_user_with_no_recent_login():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-07-01T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="2023-07-03T00:00:00+00:00",
        password_last_changed="2023-08-03T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="TRUE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def inactive_user_used_within_three_months():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-07-01T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="2023-07-02T00:00:00+00:00",
        password_last_changed="2023-07-01T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="TRUE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


@pytest.fixture
def inactive_user_not_used_within_three_months():
    return User(
        username="test",
        arn="arn:aws:iam::12345678912:user/test",
        user_creation_time="2023-03-01T00:00:00+00:00",
        password_enabled="TRUE",
        password_last_used="2023-03-02T00:00:00+00:00",
        password_last_changed="2023-03-01T00:00:00+00:00",
        password_next_rotation="N/A",
        mfa_active="TRUE",
        access_key_1_active="FALSE",
        access_key_1_last_rotated="N/A",
        access_key_1_last_used_date="N/A",
        access_key_1_last_used_region="N/A",
        access_key_1_last_used_service="N/A",
        access_key_2_active="FALSE",
        access_key_2_last_rotated="N/A",
        access_key_2_last_used_date="N/A",
        access_key_2_last_used_region="N/A",
        access_key_2_last_used_service="N/A",
        cert_1_active="FALSE",
        cert_1_last_rotated="N/A",
        cert_2_active="FALSE",
        cert_2_last_rotated="N/A",
    )


# Freeze time to 2023-08-01 00:00 to enable repeatable datetime comparisons
@pytest.fixture
def freeze_time(monkeypatch):
    now = datetime.datetime(2023, 8, 1, 0, 0, 0)
    dt_mock = MagicMock(wraps=datetime.datetime)
    dt_mock.now.return_value = now
    monkeypatch.setattr(datetime, "datetime", dt_mock)


@pytest.fixture
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture
def iam_client(aws_credentials):
    with mock_aws():
        client = boto3.client("iam", region_name="eu-west-2")
        yield client


@pytest.fixture
def mocked_config(monkeypatch):
    mock_config = {"test1": "test_1_val", "test2": "test_2_val", "foo": "bar"}
    monkeypatch.setattr(Config, "_Config__conf", mock_config)
