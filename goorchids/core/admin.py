from django.contrib import admin
from django import forms
import gobotany.core.admin
from django.contrib.contenttypes import generic
from gobotany.core.models import (Taxon, PartnerSpecies, ContentImage,
                                  Genus, Family, CopyrightHolder)
from .models import GoOrchidTaxon, RegionalConservationStatus


class TaxonConservationStatusInline(admin.TabularInline):
    model = RegionalConservationStatus
    extra = 1


class TaxonPartnerInline(admin.TabularInline):
    model = PartnerSpecies
    extra = 0
    exclude = ('species_page_heading', 'species_page_blurb')
    verbose_name = 'Partner'
    verbose_plural = 'Partner sites'


class GoOrchidTaxonGenericInlineFormset(generic.BaseGenericInlineFormSet):
    """We need the GenericRelation to point to the parent ContentType 'Taxon',
    not the subclass"""

    def __init__(self, data=None, files=None, instance=None, **kw):
        if isinstance(instance, GoOrchidTaxon):
            if hasattr(instance, 'taxon_ptr'):
                instance = instance.taxon_ptr
            else:
                # Create a temporary Taxon object to mirror our
                # ephemeral GoOrchidTaxon
                taxon_proxy = Taxon()
                taxon_proxy.__dict__ = instance.__dict__
                instance = taxon_proxy
        super(GoOrchidTaxonGenericInlineFormset, self).__init__(data=data,
                                                                files=files,
                                                                instance=instance,
                                                                **kw)


class ContentImageInline(generic.GenericTabularInline):
    model = ContentImage
    formset = GoOrchidTaxonGenericInlineFormset


class TaxonAdmin(gobotany.core.admin.TaxonAdmin):
    __doc__ = gobotany.core.admin.TaxonAdmin.__doc__

    inlines = [
        TaxonConservationStatusInline,
        gobotany.core.admin.TaxonSynonymInline,
        gobotany.core.admin.TaxonCommonNameInline,
        gobotany.core.admin.TaxonLookalikeInline,
        TaxonPartnerInline,
        ContentImageInline,
    ]

    exclude = ('wetland_indicator_code',)

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Make sure our added fields are shown with a Textarea widget
        formfield = super(TaxonAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name in (
                'pollination', 'mycorrhiza', 'monitoring',
                'propagation', 'restoration', 'flowering_phenology'):
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


class GenusAdmin(gobotany.core.admin.GenusAdmin):
    __doc__ = gobotany.core.admin.GenusAdmin.__doc__

    inlines = gobotany.core.admin.GenusAdmin.inlines + [ContentImageInline]


class FamilyAdmin(gobotany.core.admin.FamilyAdmin):
    __doc__ = gobotany.core.admin.FamilyAdmin.__doc__

    inlines = gobotany.core.admin.FamilyAdmin.inlines + [ContentImageInline]


class CopyrightHolderAdmin(gobotany.core.admin._Base):
    """

    <p>
    Only images with authors matching a registered Copyright Holder by
    `coded_name` will be displayed in the site
    </p>
    """
    model = CopyrightHolder
    ordering = ('expanded_name',)


admin.site.unregister(Taxon)
admin.site.register(GoOrchidTaxon, TaxonAdmin)
admin.site.unregister(Genus)
admin.site.register(Genus, GenusAdmin)
admin.site.unregister(Family)
admin.site.register(Family, FamilyAdmin)
admin.site.register(CopyrightHolder, CopyrightHolderAdmin)
