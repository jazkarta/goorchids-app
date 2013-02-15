from django.contrib import admin
from django import forms
import gobotany.core.admin
from gobotany.core.models import Taxon
from .models import GoOrchidTaxon


class TaxonAdmin(gobotany.core.admin.TaxonAdmin):

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
