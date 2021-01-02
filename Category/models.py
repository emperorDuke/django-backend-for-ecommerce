from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from utils.code_generator import generator


class Category(MPTTModel):
    name = models.CharField(_("category name"), max_length=50, unique=True)  
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    ref_no = models.CharField(_('reference number'), max_length=50, unique=True)
    
    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'
        db_table = 'Category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.ref_no:
            self.ref_no = generator(self)
        super(Category, self).save(*args, **kwargs)

    
