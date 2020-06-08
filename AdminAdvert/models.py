from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


def upload_to(instance, filename):
    media_path = 'uploads/admin/attachments/%s' % (filename)
    return media_path


class AdminAdvert(models.Model):

    MAIN = 'MAIN'
    CENTER = 'CENTER'
    SIDE = 'SIDE'

    POSITION = (
        (MAIN, 'main block'),
        (CENTER, 'center block'),
        (SIDE, 'side block')
    )

    name = models.CharField(_('name of image'), max_length=20, blank=False)
    attachment = models.ImageField(upload_to=upload_to, blank=False, null=True)
    position = models.CharField(_('position of images'), choices=POSITION, max_length=30, blank=False)
    added_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('name', 'attachment')
        ordering = ['-added_at']

    def __str__(self):
        return self.name
