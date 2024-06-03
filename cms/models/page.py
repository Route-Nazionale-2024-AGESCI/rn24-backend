from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index

from common.abstract import CommonAbstractModel
from common.qr import QRCodeMixin


class CMSPage(Page, QRCodeMixin, CommonAbstractModel):
    body = RichTextField(blank=True)
    search_fields = Page.search_fields + [
        index.SearchField("body"),
    ]
    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def qr_payload(self):
        return f"P#{self.uuid}"

    def get_admin_url(self):
        return f"/cms/pages/{self.id}/edit/"

    class Meta:
        verbose_name = "pagina"
        verbose_name_plural = "pagine"
