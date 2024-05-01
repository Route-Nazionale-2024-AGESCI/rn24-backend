from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from authentication.AGESCI import AGESCILoginClient
from people.models.person import Person

User = get_user_model()


class AGESCIAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        success, data = AGESCILoginClient().login_AGESCI(username, password)
        if not success:
            return None

        person = Person.objects.filter(agesci_id=username).first()
        if not person:
            # this is a valid Scout but not registered to RN24
            # TODO: log
            return None
        # we do not update Person data from AGESCI payload
        # we decide to trust the data we have in our DB
        if person.user is None:
            user = User(
                username=username,
                email=person.email,
                first_name=person.first_name,
                last_name=person.last_name,
            )
            user.save()
            person.user = user
            person.save()
        if not person.user.is_active:
            return None
        return person.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
