from django.db.models.signals import pre_save
from django.dispatch import receiver
from events.models.event import Event


@receiver(pre_save, sender=Event)
def create_event_cmspage(sender, instance=None, created=False, **kwargs):
    if not instance.page:
        from cms.models import CMSPage

        events_page = CMSPage.objects.get(title="Eventi")
        page = CMSPage(title=instance.name)
        events_page.add_child(instance=page)
        instance.page = page
    elif instance.page.title != instance.name:
        instance.page.title = instance.name
        instance.page.save()
