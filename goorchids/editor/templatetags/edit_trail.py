import json
from django.utils import timezone
from datetime import timedelta
from django.template import base as template
from gobotany.core.models import Taxon, Character, Edit, Pile
from gobotany.editor import views as edit_views
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

register = template.Library()

BASE_TABLE = u"""
  <table>
    <thead>
      <tr>
        <th class="date">Date</th>
        <th class="author">Editor</th>
        <th class="coord">%s</th>
        <th class="orig-value">Original Value</th>
      </tr>
    </thead>
    <tbody>
    %s
    </tbody>
  </table>
"""

BASE_ROW = u"""
      <tr class="{row_class}">
        <td class="date">{date:%Y-%m-%d %H:%M}</td>
        <td class="author">{author}</td>
        <td class="coord">{coord}</td>
        <td class="orig-value">{old_value}</td>
      </tr>
"""

@register.filter(name='format_old_value')
def format_old_value(value):
    value = json.loads(value)
    if isinstance(value, list) or isinstance(value, tuple):
        return escape(', '.join(str(v) for v in value))
    else:
        return escape(str(value))

@register.filter(name='taxon_edit')
def taxon_edit_link(scientific_name):
    try:
        taxon = Taxon.objects.get(scientific_name=scientific_name)
        taxon_link = '<a href="%s">%s</a>'%(
            reverse(edit_views.edit_pile_taxon,
                    args=(taxon.piles.all()[0].slug,
                          taxon.slug())),
            escape(taxon.scientific_name))
    except (ObjectDoesNotExist, IndexError):
        taxon_link = escape(scientific_name)
    return mark_safe(taxon_link)

@register.filter(name='character_edit')
def character_edit_link(short_name):
    try:
        character = Character.objects.get(short_name=short_name)
        # Character Pile may be null, in which case, use the first Pile
        pile = character.pile or Pile.objects.all()[0]
        character_link = '<a href="%s">%s</a>'%(
            reverse(edit_views.edit_pile_character,
                    args=(pile.slug,
                          character.short_name)),
            escape(character.name))
    except ObjectDoesNotExist:
        character_link = escape(short_name)
    return mark_safe(character_link)

@register.simple_tag
def taxon_edits(taxon):
    if not isinstance(taxon, Taxon):
        raise template.TemplateSyntaxError(
            "taxon_edits tag requires a single Taxon as argument")
    edits = Edit.objects.filter(coordinate1=taxon.scientific_name,
                                itemtype='character-value').order_by(
        '-datetime')

    end = timezone.now()
    start = end - timedelta(7)
    edits = edits.filter(datetime__range=[start, end])
    if not edits:
        return '<p>No recent edits</p>'

    rows = []
    for i, edit in enumerate(edits):
        character_link = character_edit_link(edit.coordinate2)
        rows.append(
            BASE_ROW.format(date=edit.datetime,
                            author=escape(edit.author),
                            old_value=format_old_value(edit.old_value),
                            coord=character_link,
                            row_class=i%2 and 'even' or 'odd'))
    return BASE_TABLE%('Character', u'\n'.join(rows))

@register.simple_tag
def character_edits(character):
    if not isinstance(character, Character):
        raise template.TemplateSyntaxError(
            "character_edits tag requires a single CharacterValue as argument")
    edits = Edit.objects.filter(coordinate2=character.short_name,
                                itemtype='character-value').order_by(
        '-datetime')

    end = timezone.now()
    start = end - timedelta(7)
    edits = edits.filter(datetime__range=[start, end])
    if not edits:
        return '<p>No recent edits</p>'

    rows = []
    for i, edit in enumerate(edits):
        taxon_link = taxon_edit_link(edit.coordinate1)
        rows.append(
            BASE_ROW.format(date=edit.datetime,
                            author=escape(edit.author),
                            old_value=format_old_value(edit.old_value),
                            coord=taxon_link,
                            row_class=i%2 and 'even' or 'odd'))
    return BASE_TABLE%('Taxon', u'\n'.join(rows))
