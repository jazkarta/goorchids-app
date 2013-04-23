from collections import OrderedDict
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import receiver
from gobotany.plantoftheday.models import PlantOfTheDay
from gobotany.core.models import Taxon


GLOBAL_RANK_CODES = OrderedDict((
    ('GX', 'Presumed Extirpated'),
    ('GH', 'Possible Extirpated'),
    ('G1', 'Critically Imperiled'),
    ('G2', 'Imperiled'),
    ('G3', 'Vulnerable'),
    ('G4', 'Apparently Secure'),
    ('G5', 'Secure'),
))

STATE_RANK_CODES = OrderedDict((
    ('SX', 'Presumed Extirpated'),
    ('SH', 'Possible Extirpated'),
    ('S1', 'Highly State Rare'),
    ('S2', 'State Rare'),
    ('S3', 'Watch List'),
    ('S4', 'Apparently Secure'),
    ('S5', 'Secure'),
))

STATE_STATUS_CODES = OrderedDict((
    ('E', 'Endangered'),
    ('T', 'Threatened'),
    ('X', 'Extirpated'),
    ('SC', 'Species of Concern'),
    ('H', 'Historical'),
))

FEDERAL_STATUS_CODES = OrderedDict((
    ('LE', 'Listed Endangered'),
    ('LT', 'Listed Threatened'),
    ('PE', 'Proposed Endangered'),
    ('PT', 'Proposed Threatened'),
    ('C', 'Candidate'),
))

CANADIAN_RANK_CODES = OrderedDict((
    ('0.2', 'Extinct'),
    ('0.1', 'Extirpated'),
    ('1', 'At Risk'),
    ('2', 'May Be At Risk'),
    ('3', 'Sensitive'),
    ('4', 'Secure'),
    ('5', 'Undetermined'),
    ('6', 'Not assessed'),
    ('7', 'Exotic'),
    ('8', 'Accidental')
))

WETLAND_STATUS_CODES = OrderedDict((
    ('OBL', 'Obligate Wetland'),
    ('FACW', 'Facultative Wetland'),
    ('FAC', 'Facultative'),
    ('FACU', 'Facultative Upland'),
    ('UPL', 'Upland'),
))


class GoOrchidTaxon(Taxon):
    """Subclass the GoBotany taxon model to add orchid-specific fields.
    """

    class Meta:
        verbose_name = "taxon"
        verbose_name_plural = "taxa"

    ready_for_display = models.BooleanField(default=False)
    pollination = models.CharField(max_length=1000, blank=True)
    mycorrhiza = models.CharField(max_length=1000, blank=True)
    monitoring = models.CharField(max_length=1000, blank=True)
    propagation = models.CharField(max_length=1000, blank=True)
    restoration = models.CharField(max_length=1000, blank=True)
    flowering_phenology = models.CharField(max_length=1000, blank=True)

    # Conservation status
    global_rank = models.CharField(
        max_length=2, null=True, blank=True,
        choices=GLOBAL_RANK_CODES.items()
    )
    us_status = models.CharField(
        max_length=2, null=True, blank=True,
        choices=FEDERAL_STATUS_CODES.items(),
        verbose_name='US status',
    )
    ca_rank = models.CharField(
        max_length=3, null=True, blank=True,
        choices=CANADIAN_RANK_CODES.items(),
        verbose_name='Canadian rank',
    )

    @property
    def images(self):
        return self.taxon_ptr.images


class RegionalConservationStatus(models.Model):
    """Zero or more conservation status values per species+region."""

    STATE_NAMES = sorted(settings.STATE_NAMES.items(), key=lambda x: x[1])

    taxon = models.ForeignKey(GoOrchidTaxon, related_name='regional_conservation_statuses')
    region = models.CharField(choices=STATE_NAMES, max_length=80)
    status = models.CharField(choices=STATE_STATUS_CODES.items(), max_length=2,
                              default=None, null=True, blank=True)
    rank = models.CharField(choices=STATE_RANK_CODES.items(), max_length=2,
                            default=None, null=True, blank=True)
    wetland_status = models.CharField(choices=WETLAND_STATUS_CODES.items(), max_length=4,
                                      default=None, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'regional conservation statuses'
        ordering = ('region', 'status', 'rank')
        unique_together = (
            ('taxon', 'region', 'status'),
            ('taxon', 'region', 'rank'),
        )

    def __unicode__(self):
        return u'%s: %s, %s' % (self.region, self.status, self.rank)


@receiver(models.signals.post_save, sender=GoOrchidTaxon)
def update_potd_after_taxon_save(sender, **kw):
    """After a taxon is saved, make sure it has an entry in the plantoftheday table."""
    instance = kw['instance']
    try:
        PlantOfTheDay.objects.filter(
            scientific_name=instance.scientific_name, partner_short_name='gobotany').get()
    except ObjectDoesNotExist:
        PlantOfTheDay(scientific_name=instance.scientific_name, partner_short_name='gobotany').save()


class ImportLog(models.Model):
    """Log of imports run"""
    filename = models.CharField(max_length=100)
    start = models.DateTimeField()
    duration = models.IntegerField(null=True)
    success = models.NullBooleanField(null=True)
    message = models.TextField(null=True)
