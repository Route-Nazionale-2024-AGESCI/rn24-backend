import requests
from django.conf import settings


class AGESCILoginClient:

    AGESCI_HOSTNAME = settings.AGESCI_HOSTNAME
    AGESCI_SECRET = settings.AGESCI_SECRET
    AGESCI_KEY = settings.AGESCI_KEY

    access_token_url = f"https://{AGESCI_HOSTNAME}/service-ext/api/Applicazione/Login"
    login_url = f"https://{AGESCI_HOSTNAME}/service-ext/api/UtenteExt/Login"

    def __init__(self) -> None:
        self.access_token = None

    def refresh_access_token(self):
        response = requests.post(
            url=self.access_token_url,
            json={"secret": self.AGESCI_SECRET, "key": self.AGESCI_KEY},
        )
        if response.status_code == 200:
            self.access_token = response.json()["access_token"]
            return
        # TODO: log error

    def login_AGESCI(self, username, password):
        try:
            response = requests.post(
                url=self.login_url,
                json={"username": username, "password": password},
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            if response.status_code == 200:
                return (True, response.json())
            if response.status_code == 401:
                self.refresh_access_token()
                # TODO: avoid endless loop
                return self.login_AGESCI(username=username, password=password)
            # TODO: log other errors
            return (False, "Invalid credentials")
        except Exception:
            # TODO: log error
            return (False, "Invalid credentials")
