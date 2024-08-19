import pytest

from src.app.helpers import *

MOCK_INACTIVITY_THRESHOLD = 90


def test_recently_created_user_is_to_be_deleted(
    freeze_time, recently_created_user_with_no_logins
):
    assert (
        account_deletion_date_reached(
            recently_created_user_with_no_logins,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == False
    )


def test_not_recently_created_user_is_to_be_deleted(
    freeze_time, not_recently_created_user_with_no_logins
):
    assert (
        account_deletion_date_reached(
            not_recently_created_user_with_no_logins,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == True
    )


def test_user_who_never_signed_in_no_information_within_threshold_is_still_expired(
    freeze_time,
    not_recently_created_user_with_no_information_on_logins,
):
    assert (
        account_deletion_date_reached(
            not_recently_created_user_with_no_information_on_logins,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == True
    )


def test_disabled_user_is_to_be_deleted(
    freeze_time, disabled_user_account_less_than_one_month_old
):
    assert (
        account_deletion_date_reached(
            disabled_user_account_less_than_one_month_old,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == False
    )


def test_active_user_is_to_be_deleted(freeze_time, active_user):
    assert (
        account_deletion_date_reached(active_user, MOCK_INACTIVITY_THRESHOLD) == False
    )


def test_inactive_user_used_within_three_months_is_to_be_deleted(
    freeze_time, inactive_user_used_within_three_months
):
    assert (
        account_deletion_date_reached(
            inactive_user_used_within_three_months,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == False
    )


def test_inactive_user_not_used_within_three_months_is_to_be_deleted(
    freeze_time, inactive_user_not_used_within_three_months
):
    assert (
        account_deletion_date_reached(
            inactive_user_not_used_within_three_months,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == True
    )


def test_recently_reenabled_user_is_to_be_deleted(
    freeze_time, recently_reenabled_user_with_no_recent_login
):
    assert (
        account_deletion_date_reached(
            recently_reenabled_user_with_no_recent_login,
            MOCK_INACTIVITY_THRESHOLD,
        )
        == False
    )
