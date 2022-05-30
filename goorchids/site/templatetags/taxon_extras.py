from django.template.library import Library
from django.template.exceptions import TemplateSyntaxError
from gobotany.core.models import Genus, Taxon
from django.utils.html import format_html
from django.urls import reverse

register = Library()

@register.simple_tag
def genus_link(genus):
    if not isinstance(genus, Genus):
        raise TemplateSyntaxError(
            "genus_link tag requires a single Genus as argument")
    if genus.taxa.filter(goorchidtaxon__ready_for_display=True).count():
        return '<a href="%s">%s</a>'%(reverse('site-genus',
                                              args=[genus.slug]),
                                      genus.name)
    else:
        return genus.name

@register.simple_tag
def species_link(species):
    if not isinstance(species, Taxon):
        raise TemplateSyntaxError(
            "species_link tag requires a single Taxon as argument")
    species = getattr(species, 'goorchidtaxon', species)
    is_ready = getattr(species, 'ready_for_display', False)
    if is_ready:
        return format_html(
            '<a href="%s">%s</a>' % (
                reverse('site-species', args=[species.genus.slug, species.epithet]),
                species.scientific_name
            )
        )
    else:
        return species.scientific_name
