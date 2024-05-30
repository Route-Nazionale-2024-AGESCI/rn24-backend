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
        """
        curl -XPOST
        https://XXX/service-ext/api/Applicazione/Login
        -H "Content-Type: application/json"
        --data '{"secret":"XXX","key":"XXX"}'

        HTTP/1.1 200 OK
        {"accessToken":"XXX","duration":20,"expiryDate":"2024-05-31T00:03:42.0333513+02:00"}

        HTTP/1.1 400 Bad Request
        Applicazione non riconosciuta.

        """
        response = requests.post(
            url=self.access_token_url,
            json={"secret": self.AGESCI_SECRET, "key": self.AGESCI_KEY},
        )
        if response.status_code == 200:
            self.access_token = response.json()["accessToken"]
            return
        # TODO: log error

    def login_AGESCI(self, username, password):
        """
        curl -XPOST
        https://XXX/service-ext/api/UtenteExt/Login
        -H "Content-Type: application/json"
        -H "Authorization: Bearer XXX"
        --data '{"username":"XXX","password":"XXX"}'

        HTTP/1.1 200 OK
        {
            "codSocio":,
            "nome":,
            "cognome":,
            "dataNascita":,
            "sesso":,
            "codGruppo":,
            "nomeGruppo":,
            "codZona":,
            "nomeZona":,
            "codRegione":,
            "nomeRegione":
        }

        HTTP/1.1 400 Bad Request
        Username e/o password non corretti.

        (token errato)
        HTTP/1.1 401 Unauthorized
        body vuoto
        """
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


class AGESCIResetPasswordClient:
    """
    curl
    '/service/api/account/PasswordRecovery'
    -H 'Accept: */*'
    -H 'Content-Type: application/json'
    --data-raw '{"cSocio":"XXX","email":"XXX"}'

    HTTP/1.1 200 OK
    "Ti è stata inviata una mail con un link per reimpostare la password"

    HTTP/1.1 404 Not Found
    "Errore! Utente non trovato"
    """

    AGESCI_HOSTNAME = settings.AGESCI_HOSTNAME
    PASSWORD_RESET_URL = f"https://{AGESCI_HOSTNAME}/service/api/account/PasswordRecovery"

    def send_reset_password_email(self, agesci_id: str, email: str):
        try:
            response = requests.post(
                url=self.PASSWORD_RESET_URL,
                json={"cSocio": agesci_id, "email": email},
            )
            if response.status_code == 200:
                return (True, response.content)
            return (False, response.content)
        except Exception:
            # TODO: log error
            return (False, "Errore")
