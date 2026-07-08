from django.contrib import admin
from django import forms
from django.db import models
import gobotany.core.admin
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.forms import BaseGenericInlineFormSet
from django.contrib.contenttypes.admin import GenericTabularInline
from gobotany.core.models import (Taxon, PartnerSpecies, ContentImage,
                                  Genus, Family, CopyrightHolder, Pile)
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


class GoOrchidTaxonGenericInlineFormset(BaseGenericInlineFormSet):
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

    def clean(self):
        super(GoOrchidTaxonGenericInlineFormset, self).clean()

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue
            if self._should_delete_form(form):
                continue
            if form.errors:
                continue
            if not form.has_changed():
                continue

            instance = form.instance
            try:
                instance.clean()
            except ValidationError as e:
                form.add_error(None, e)
                raise forms.ValidationError(
                    'Please correct the image errors below.')


class ContentImageAdminForm(forms.ModelForm):
    class Meta:
        model = ContentImage
        fields = '__all__'

    def _post_clean(self):
        try:
            super(ContentImageAdminForm, self)._post_clean()
        except ContentImage.image_type.RelatedObjectDoesNotExist:
            self.add_error(
                'image_type',
                'This field is required when uploading an image.')

    def clean(self):
        cleaned_data = super(ContentImageAdminForm, self).clean()

        image = cleaned_data.get('image')
        if image and not cleaned_data.get('image_type'):
            self.add_error(
                'image_type',
                'This field is required when uploading an image.')

        return cleaned_data


class ContentImageInline(GenericTabularInline):
    model = ContentImage
    form = ContentImageAdminForm
    formset = GoOrchidTaxonGenericInlineFormset


class TaxonAdmin(gobotany.core.admin.TaxonAdmin):
    __doc__ = gobotany.core.admin.TaxonAdmin.__doc__.replace('Go Botany',
                                                             'Go Orchids') + \
        '<style type="text/css">.field-piles { display: none; }</style>'
    # Replace all single line text widgets with a text area
    formfield_overrides = {
        models.CharField: {'widget': forms.Textarea},
    }

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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'piles':
            kwargs = {}
            if Pile.objects.count():
                kwargs['initial'] = [Pile.objects.get()]
            return db_field.formfield(**kwargs)
        return super(TaxonAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class GenusAdmin(gobotany.core.admin.GenusAdmin):
    __doc__ = gobotany.core.admin.GenusAdmin.__doc__.replace('Go Botany',
                                                             'Go Orchids')

    inlines = gobotany.core.admin.GenusAdmin.inlines + [ContentImageInline]


class FamilyAdmin(gobotany.core.admin.FamilyAdmin):
    __doc__ = gobotany.core.admin.FamilyAdmin.__doc__.replace('Go Botany',
                                                              'Go Orchids')

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
#admin.site.register(CopyrightHolder, CopyrightHolderAdmin)
