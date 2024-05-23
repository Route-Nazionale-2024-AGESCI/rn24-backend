import pytest
from django.urls import reverse

from authentication.AGESCI import AGESCIResetPasswordClient


@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture
    def agesci_password_reset_success_mock(self, requests_mock):
        requests_mock.post(
            AGESCIResetPasswordClient.PASSWORD_RESET_URL,
            status_code=200,
            text="Ti è stata inviata una mail con un link per reimpostare la password",
        )
        return requests_mock

    @pytest.fixture
    def agesci_password_reset_failure_mock(self, requests_mock):
        requests_mock.post(
            AGESCIResetPasswordClient.PASSWORD_RESET_URL,
            status_code=404,
            text="Errore! Utente non trovato",
        )
        return requests_mock

    def test_password_reset_success(self, client, agesci_password_reset_success_mock):
        url = reverse("password-reset")
        data = {"email": "test@example.com", "agesci_id": "12345"}
        response = client.post(url, data)
        assert response.status_code == 201
        assert response.json() == {
            "message": "Ti è stata inviata una mail con un link per reimpostare la password"
        }

    def test_password_reset_failure(self, client, agesci_password_reset_failure_mock):
        url = reverse("password-reset")
        data = {"email": "test@example.com", "agesci_id": "12345"}
        response = client.post(url, data)
        assert response.status_code == 400
        assert response.json() == {"message": "Errore! Utente non trovato"}
