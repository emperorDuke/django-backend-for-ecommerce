from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here

class Location(models.Model):
    address = models.CharField(_('address'), max_length=100, blank=False)
    city = models.CharField(_('city'), max_length=50, blank=False)
    country = models.CharField(_('country'), max_length=50, blank=False)
    zip_code = models.CharField(_('zip code'), max_length=50, blank=True)
    state = models.CharField(_('state'), max_length=50, blank=False)
    added_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ('address', 'city',  'state')
        db_table = 'location'

    def __str__(self):
        return '%s, %s, %s' % (self.city, self.state, self.country)
