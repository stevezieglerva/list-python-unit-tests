import os, sys, inspect, json
import boto3

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/add_cw_log_error_metric"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from unittest import mock
from unittest.mock import patch
from add_cw_log_error_metric.LogMetricFilters import *
from add_cw_log_error_metric.filter_list_by_regexs import *


class LogMetricFiltersUnitTests(unittest.TestCase):
    def test_constructor__given_whats_needed__then_no_exceptions(self):
        # Arrange

        # Act
        result = LogMetricFilters("log_metric_filters")

        # Assert

    def test_get_ec2_instance_name_from_log_group__given_ec2_log_group_name__then_return_matching_instance(
        self,
    ):
        # Arrange
        input = "/project/ec2/i-0ffdac9ff36a77ef4/cron"
        subject = LogMetricFilters("log_metric_filters")

        # Act
        results = subject.get_ec2_instance_name_from_log_group(input)
        print(f"\nextracted instance: {results}\n")

        # Assert
        self.assertEqual(results, "i-0ffdac9ff36a77ef4")

    @patch.object(boto3, "resource")
    def test_get_ec2_info_for_related_log_groups__given_some_are_ec2__then_ec2s_info_returned(
        self, mock_client
    ):
        # Arrange
        input = [
            "aws/manual_log",
            "aws/manual_log2",
            "/project/ec2/i-0ffdac9ff36a77ef4/cron",
            "/project/ec2/i-5ffdac9ff36a77edd/http",
        ]
        subject = LogMetricFilters("log_metric_filters")
        boto3.resource.return_value.Instance.return_value.tags = [
            {"Key": "Environment", "Value": "dev"},
            {"Key": "Name", "Value": "dev-solr"},
        ]

        # Act
        results = subject.get_ec2_info_for_related_log_groups(input)
        print(json.dumps(results, indent=3, default=str))
        print(json.dumps(results, default=str))

        # Assert
        expected = [
            {
                "log_group_name": "aws/manual_log",
                "log_type": "log_type_not_ec2",
                "ec2_tag_info": {},
            },
            {
                "log_group_name": "aws/manual_log2",
                "log_type": "log_type_not_ec2",
                "ec2_tag_info": {},
            },
            {
                "log_group_name": "/project/ec2/i-0ffdac9ff36a77ef4/cron",
                "log_type": "log_type_ec2",
                "ec2_tag_info": [
                    {"Key": "Environment", "Value": "dev"},
                    {"Key": "Name", "Value": "dev-solr"},
                ],
            },
            {
                "log_group_name": "/project/ec2/i-5ffdac9ff36a77edd/http",
                "log_type": "log_type_ec2",
                "ec2_tag_info": [
                    {"Key": "Environment", "Value": "dev"},
                    {"Key": "Name", "Value": "dev-solr"},
                ],
            },
        ]
        self.assertEqual(results, expected)

    @mock.patch(
        "add_cw_log_error_metric.LogMetricFilters.LogMetricFilters.get_ec2_info_for_related_log_groups",
        mock.MagicMock(
            return_value=[
                {
                    "log_group_name": "aws/manual_log",
                    "log_type": "log_type_not_ec2",
                    "ec2_tag_info": {},
                },
                {
                    "log_group_name": "aws/manual_log2",
                    "log_type": "log_type_not_ec2",
                    "ec2_tag_info": {},
                },
                {
                    "log_group_name": "/project/ec2/i-0ffdac9ff36a77ef4/cron",
                    "log_type": "log_type_ec2",
                    "ec2_tag_info": [
                        {"Key": "Environment", "Value": "dev"},
                        {"Key": "Name", "Value": "dev-solr"},
                    ],
                },
                {
                    "log_group_name": "/project/ec2/i-5ffdac9ff36a77edd/http",
                    "log_type": "log_type_ec2",
                    "ec2_tag_info": [
                        {"Key": "Environment", "Value": "prod"},
                        {"Key": "Name", "Value": "prod-solr"},
                    ],
                },
            ]
        ),
    )
    def test_filter_log_group_names_for_ec2_tags__given_few_ec2_logs_should_be_removed__then_they_are_removed(
        self,
    ):
        # Arrange
        input = [
            "aws/manual_log",
            "aws/manual_log2",
            "/project/ec2/i-0ffdac9ff36a77ef4/cron",
            "/project/ec2/i-5ffdac9ff36a77edd/http",
        ]
        subject = LogMetricFilters("log_metric_filters")

        # Act
        results = subject.filter_log_group_names_for_ec2_tags(input, "", ".*dev.*")
        print(results)

        # Assert
        self.assertEqual(
            results,
            [
                "aws/manual_log",
                "aws/manual_log2",
                "/project/ec2/i-5ffdac9ff36a77edd/http",
            ],
        )
