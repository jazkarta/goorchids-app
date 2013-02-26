from django.contrib import admin
from django import forms
import gobotany.core.admin
from gobotany.core.models import Taxon, PartnerSpecies
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


class TaxonAdmin(gobotany.core.admin.TaxonAdmin):
    __doc__ = gobotany.core.admin.TaxonAdmin.__doc__

    inlines = [
        TaxonConservationStatusInline,
        gobotany.core.admin.TaxonSynonymInline,
        gobotany.core.admin.TaxonCommonNameInline,
        gobotany.core.admin.TaxonLookalikeInline,
        TaxonPartnerInline,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Make sure our added fields are shown with a Textarea widget
        formfield = super(TaxonAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name in (
                'pollination', 'mycorrhiza', 'monitoring',
                'propagation', 'restoration', 'flowering_phenology'):
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


admin.site.unregister(Taxon)
admin.site.register(GoOrchidTaxon, TaxonAdmin)
