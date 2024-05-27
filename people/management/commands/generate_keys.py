from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "generate privkey.pem and pubkey.pem files"

    def handle(self, *args, **options):
        from Crypto.PublicKey import ECC

        key = ECC.generate(curve="p256")
        with open("privkey.pem", "w") as f:
            f.write(key.export_key(format="PEM"))

        with open("pubkey.pem", "w") as f:
            f.write(key.public_key().export_key(format="PEM"))
