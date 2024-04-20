import pytest
from django.urls import reverse


def test_authentication_is_required(client):
    response = client.get(reverse("profile-detail"))
    assert response.status_code == 403, response.content


@pytest.mark.django_db
def test_token_works(client, person):
    url = reverse("profile-detail")
    response = client.get(url, HTTP_AUTHORIZATION=f"Token {person.user.auth_token}")
    assert response.status_code == 200
