import os, sys, inspect, json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/add_cw_log_error_metric"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock
from add_cw_log_error_metric.app import *
import datetime
from unittest.mock import patch
import boto3


class CWLogUnitTest(unittest.TestCase):
    all_log_groups = [
        {
            "logGroupName": "/aws/aes/domains/ziegler-es/application-logs",
            "creationTime": 1574359409994,
            "metricFilterCount": 1,
            "arn": "arn:aws:logs:us-east-1:706415383428:log-group:/aws/aes/domains/ziegler-es/application-logs:*",
            "storedBytes": 1271745,
        }
    ]

    metric_filters_already_exists = {
        "metricFilters": [
            {
                "filterName": "ops-aws-basic-filters-cw-metric-filters-6-ErrorMetricFilterc41b4323cc29e9a4f308f68dbd23af52-172S93J5URRIN",
                "filterPattern": "?error ?Error ?ERROR ?exception ?Exception ?Exception",
                "metricTransformations": [
                    {
                        "metricName": "ops-aws-aws-aes-domains-ziegler-es-application-logs",
                        "metricNamespace": "ops-aws",
                        "metricValue": "1",
                    }
                ],
                "creationTime": 1576884644693,
                "logGroupName": "/aws/aes/domains/ziegler-es/application-logs",
            },
            {
                "filterName": "ops-aws-basic-super-api",
                "filterPattern": "?error ?Error ?ERROR ?exception ?Exception ?Exception",
                "metricTransformations": [
                    {
                        "metricName": "ops-aws-aws-aes-super-api",
                        "metricNamespace": "ops-aws",
                        "metricValue": "1",
                    }
                ],
                "creationTime": 1576884644693,
                "logGroupName": "/aws/super-api",
            },
        ]
    }

    metric_filters_does_not_exist = {
        "metricFilters": [
            {
                "filterName": "ops-aws-basic-filters-cw-metric-filters-6-ErrorMetricFilterc41b4323cc29e9a4f308f68dbd23af52-172S93J5URRIN",
                "filterPattern": "?error ?Error ?ERROR ?exception ?Exception ?Exception",
                "metricTransformations": [
                    {
                        "metricName": "ops-aws-aws-super-api",
                        "metricNamespace": "ops-aws",
                        "metricValue": "1",
                    }
                ],
                "creationTime": 1576884644693,
                "logGroupName": "/aws/super-api",
            }
        ]
    }

    @mock.patch(
        "LogMetricFilters.LogMetricFilters.get_source_resource_candidates",
        mock.MagicMock(return_value=all_log_groups),
    )
    @mock.patch(
        "LogMetricFilters.LogMetricFilters.get_current_alarm_resources",
        mock.MagicMock(return_value=metric_filters_already_exists),
    )
    @mock.patch(
        "add_cw_log_error_metric.app.create_event",
        mock.MagicMock(return_value="mocked"),
    )
    def test_func_lambda_handler__given_metric_already_exists__then_counts_match(self):
        # Arrange
        os.environ[
            "EXCLUDE_REGEX"
        ] = "^.*[cC]loud[tT]rail.*$|^.*ops-aws-[^f].*$|^.*Single.*$"
        os.environ["EVENTS_BUCKET"] = "fake-bucket"

        # Act
        result = lambda_handler({"mode": "TEST"}, "")

        # Assert
        self.assertGreater(len(result), 0)
        self.assertEqual(result["total_cloudwatch_logs"], 1)
        self.assertEqual(result["initial_ops_aws_metrics"], 2)
        self.assertEqual(len(result["logs_without_ops_aws_metrics"]), 0)

    @mock.patch(
        "LogMetricFilters.LogMetricFilters.get_source_resource_candidates",
        mock.MagicMock(return_value=all_log_groups),
    )
    @mock.patch(
        "LogMetricFilters.LogMetricFilters.get_current_alarm_resources",
        mock.MagicMock(return_value=metric_filters_does_not_exist),
    )
    @mock.patch(
        "add_cw_log_error_metric.app.create_event",
        mock.MagicMock(return_value="mocked"),
    )
    def test_func_lambda_handler__given_metric_does_not_exist__then_tries_to_add_it(
        self,
    ):
        # Arrange
        os.environ[
            "EXCLUDE_REGEX"
        ] = "^.*[cC]loud[tT]rail.*$|^.*ops-aws-[^f].*$|^.*Single.*$"
        os.environ["EVENTS_BUCKET"] = "fake-bucket"

        # Act
        result = lambda_handler({"mode": "TEST"}, "")

        # Assert
        self.assertGreater(len(result), 0)
        self.assertEqual(result["total_cloudwatch_logs"], 1)
        self.assertEqual(len(result["logs_without_ops_aws_metrics"]), 1)

    @mock.patch(
        "LogMetricFilters.LogMetricFilters.get_source_resource_candidates",
        mock.MagicMock(return_value=all_log_groups),
    )
    @mock.patch(
        "LogMetricFilters.LogMetricFilters.get_current_alarm_resources",
        mock.MagicMock(return_value=metric_filters_does_not_exist),
    )
    @mock.patch(
        "add_cw_log_error_metric.app.create_event",
        mock.MagicMock(return_value="mocked"),
    )
    def test_func_lambda_handler__given_filter_ziegler__then_ziegler_not_added(self):
        # Arrange
        os.environ[
            "EXCLUDE_REGEX"
        ] = "^.*[cC]loud[tT]rail.*$|^.*ops-aws-[^f].*$|^.*Single.*$|^.*ziegler-es.*$"
        os.environ["EVENTS_BUCKET"] = "fake-bucket"

        # Act
        result = lambda_handler({"mode": "TEST"}, "")

        # Assert
        self.assertGreater(len(result), 0)
        self.assertEqual(result["total_cloudwatch_logs"], 1)
        self.assertEqual(result["filtered_list"], [])
        self.assertEqual(len(result["logs_without_ops_aws_metrics"]), 1)

    def test_func_is_old_alarm__given_alarm_is_older_than_30_days(self):
        # Arrange
        alarm = {
            "StateUpdatedTimestamp": datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(31)
        }
        # Act
        result = is_old_alarm(alarm)
        # Assert
        self.assertTrue(result)

    def test_func_is_old_alarm__given_alarm_is_not_older_than_30_days(self):
        # Arrange
        alarm = {
            "StateUpdatedTimestamp": datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(10)
        }
        # Act
        result = is_old_alarm(alarm)
        # Assert
        self.assertFalse(result)

    @patch.object(boto3, "client")
    def test_func_get_old_alarms_names_array__given(self, mock_client):
        # Arrange
        boto3.client.return_value.describe_alarms.return_value = {
            "MetricAlarms": [
                {
                    "AlarmName": "OldAlarm",
                    "StateUpdatedTimestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    )
                    - datetime.timedelta(31),
                },
                {
                    "AlarmName": "NewAlarm",
                    "StateUpdatedTimestamp": datetime.datetime.now(
                        datetime.timezone.utc
                    )
                    - datetime.timedelta(5),
                },
            ]
        }
        # Act
        result = get_old_alarms_names_array()
        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual("OldAlarm", result[0])
