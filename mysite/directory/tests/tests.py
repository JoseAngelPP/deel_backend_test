import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from directory.api.serializers import UserSerializer
from directory.models import Company

User = get_user_model()

"""
To make a test API call over an authenticated API endpoint, follow
this pattern:


```
from django.urls import reverse
from rest_framework.test import APIClient

client = APIClient()
user = ...
client.force_authenticate(user=self.user)
response = client.get(reverse('{REVERSED_URL}'))
```

"""


def create_company(name):
    # Create a new Company instance with the given name
    return Company.objects.create(name=name)


def create_user(username, company):
    # Create a new User instance with the given username, company, and default values for other fields
    return User.objects.create_user(
        username=username,
        first_name="Test",
        last_name="User",
        email=f"{username}@example.com",
        company=company,
    )


class UsersViewSetAPICase(TestCase):
    def setUp(self):
        # Set up the test environment
        self.client = APIClient()

        # Create two Company instances
        self.company_a = create_company("Test Company A")
        self.company_b = create_company("Test Company B")

        # Create two User instances, each associated with a different Company
        self.user_1 = create_user("test_user_1", self.company_a)
        self.user_2 = create_user("test_user_2", self.company_b)

        # Create a token for user_1 for authentication
        self.token = Token.objects.create(user=self.user_1)
        self.headers = {"Authorization": f"Token {self.token.key}"}

    def test_list_users(self):
        # Authenticate user_1
        self.client.force_authenticate(user=self.user_1)

        # Make a GET request to the users' list
        url = reverse("users-list")
        response = self.client.get(url, **self.headers)

        # Verify that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response contains data
        json_content = response.content
        json_content = json.loads(response.content)

        # Verify that user_1 is in the response, but user_2 is not
        serialized_user_1 = UserSerializer(self.user_1).data
        self.assertIn(serialized_user_1, json_content)

        serialized_user_2 = UserSerializer(self.user_2).data
        self.assertNotIn(serialized_user_2, json_content)

    def test_reports_action(self):
        # Authenticate user_1
        self.client.force_authenticate(user=self.user_1)

        # Make a GET request to the reports action for a specific user (user_1)
        url = reverse("users-reports", args=[self.user_1.pk])
        response = self.client.get(url)

        # Verify that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response contains data
        json_content = response.content
        json_content = json.loads(response.content)

        # Verify that the reports for user_1 are in the response
        reports = self.user_1.reports.all()
        serialized_reports = UserSerializer(reports, many=True).data
        self.assertEqual(serialized_reports, json_content)
