from django.db import models
from gobotany.core.models import Taxon
from gobotany.core.admin import TaxonAdmin
import django.contrib.admin


class GoOrchidTaxon(Taxon):
    """Subclass the GoBotany taxon model to add some orchid-specific fields.
    """

    class Meta:
        verbose_name = "taxon"
        verbose_name_plural = "taxa"

    pollination = models.CharField(max_length=1000)
    mycorrhiza = models.CharField(max_length=1000)
    monitoring = models.CharField(max_length=1000)
    propagation = models.CharField(max_length=1000)
    restoration = models.CharField(max_length=1000)
    flowering_phenology = models.CharField(max_length=1000)
