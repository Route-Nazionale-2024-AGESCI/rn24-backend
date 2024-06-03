import base64
import io

import qrcode
from django.utils.html import format_html


class QRCodeMixin:
    def qr_ascii(self):
        qr = qrcode.QRCode()
        qr.add_data(self.qr_payload())
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        return f.read()

    def qr_png(self):
        qr = qrcode.QRCode()
        qr.add_data(self.qr_payload())
        qr.make()
        img = qr.make_image()
        f = io.BytesIO()
        img.save(f, format="PNG")
        f.seek(0)
        return f.read()

    def qr_png_base64(self):
        png = self.qr_png()
        base64_png = base64.b64encode(png)
        return format_html('<img src="data:image/png;base64,{}">', base64_png.decode("utf-8"))

    def qr_svg(self):
        qr = qrcode.QRCode()
        qr.add_data(self.qr_payload())
        qr.make(image_factory=qrcode.image.svg.SvgImage)
        img = qr.make_image(fill_color="black", back_color="white")
        f = io.StringIO()
        img.save(f, format="SVG")
        f.seek(0)
        return f.read()

    def qr_payload(self):
        raise NotImplementedError()
