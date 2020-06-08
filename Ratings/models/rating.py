from django.db import models
from django.utils.translation import gettext_lazy as _

class Rating (models.Model):
    average_rating = models.DecimalField(_('total rating average'), null=True, max_digits=5, decimal_places=1, default=0.0)
    n_one_star_votes = models.PositiveIntegerField(_('number of 1 star ratings'), null=True, default=0)
    n_two_stars_votes = models.PositiveIntegerField(_('number of 2 star ratings'), null=True, default=0)
    n_three_stars_votes = models.PositiveIntegerField(_('number of 3 star ratings'), null=True, default=0)
    n_four_stars_votes = models.PositiveIntegerField(_('number of 4 star ratings'), null=True, default=0)
    n_five_stars_votes = models.PositiveIntegerField(_('number of 5 star ratings'), null=True, default=0)
    n_votes = models.PositiveIntegerField(_('number of votes'), null=True, default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-average_rating']