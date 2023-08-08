from rest_framework import status
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateLanguage:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.post('/library/languages/', {'name': 'a'})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

