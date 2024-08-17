import logging
import random
import string

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def random_password():
    length = random.randint(8, 16)
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for i in range(length))
    return password


def generate_and_send_password(user):
    password = random_password()
    user.set_password(password)
    user.save()
    send_mail(
        "RN24 APP: le tue credenziali",
        f"URL: https://rn24-app.agesci.it\n\nnome utente: {user.username}\n\npassword: {password}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    logger.info("password generata ed inviata per %s email: %s", user.username, user.email)
