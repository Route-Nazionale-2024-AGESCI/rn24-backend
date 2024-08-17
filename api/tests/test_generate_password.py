from unittest.mock import patch

import pytest
from django.urls import reverse

from people.factories import PersonFactory


@pytest.mark.django_db
class TestGeneratePasswordView:

    @pytest.fixture
    def person(self):
        return PersonFactory(email="test@example.com")

    @pytest.fixture
    def generate_and_send_password_mock(self):
        with patch("api.views.login.serializers.generate_and_send_password") as mock:
            yield mock

    def test_password_reset_success(self, client, person):
        url = reverse("password-generate")
        data = {"username": "test@example.com"}
        response = client.post(url, data)
        assert response.status_code == 201
        assert response.json() == {"message": f"Password generata ed inviata a {person.email}"}

    def test_password_reset_failure(self, client, person):
        url = reverse("password-generate")
        data = {"username": "test+1@example.com"}
        response = client.post(url, data)
        assert response.status_code == 400
        assert response.json() == {"message": "Il nome utente 'test+1@example.com' non esiste"}
