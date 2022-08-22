import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate


@pytest.fixture
def user_test_auth():
    user = User.objects.create_user(
        email="test@test.com", nickname="test", password="1!@#ali", is_verified=True
    )
    return user


@pytest.mark.django_db
class TestTodoApi:
    client = APIClient()

    def test_get_Task_response_401_status(self):
        url = reverse("api-v1:Task-list")
        response = self.client.get(url)
        assert response.status_code == 401

    def test_Create_Task_response_401_status(self):
        url = reverse("api-v1:Task-list")
        data = {"title": "test", "complete": True}
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_Create_Task_response_201_status(self, user_test_auth):
        url = reverse("api-v1:Task-list")
        data = {"title": "test", "complete": True}
        user = user_test_auth
        self.client.force_login(user=user)

        response = self.client.post(url, data)
        assert response.status_code == 201

    def test_get_Task_response_200_status(self, user_test_auth):
        url = reverse("api-v1:Task-list")
        user = user_test_auth
        self.client.force_login(user=user)
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_Task_invalid_data_response_400_status(self, user_test_auth):
        url = reverse("api-v1:Task-list")
        user = user_test_auth
        self.client.force_login(user=user)
        data = {}
        user = user_test_auth
        self.client.force_login(user=user)
        response = self.client.post(url, data)
        assert response.status_code == 400
