import json
import urllib.parse

from datetime import datetime
from datetime import timedelta
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from gobotany.core import models
from gobotany.editor.views import character_value_key, tcvfieldname_re

DAY = timedelta(1)

class EditSearchForm(forms.Form):
    start_date = forms.DateField(label=u'Start Date',
                                 required=False)
    end_date = forms.DateField(label=u'End Date',
                               required=False)
    author = forms.ChoiceField(label=u'Editor',
                               required=False)
    taxon = forms.ChoiceField(label=u'Taxon',
                              required=False)

    def __init__(self, *args, **kwargs):
        super(EditSearchForm, self).__init__(*args, **kwargs)
        self.fields['author'].choices = ([('', '----')] +
                    [(e.author, e.author) for e in
                     models.Edit.objects.distinct('author').all()])
        self.fields['taxon'].choices = ([('', '----')] +
                    [(e.scientific_name, e.scientific_name) for e in
                     models.Taxon.objects.order_by('scientific_name').all()])

def paginate(values, request, count=50):
    paginator = Paginator(values, count)

    page = request.GET.get('page')
    try:
        values = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        values = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        values = paginator.page(paginator.num_pages)
    return values

@permission_required('core.botanist')
def list_edits(request):
    edits = models.Edit.objects.order_by('-datetime')
    form = EditSearchForm(request.GET)
    if form.is_valid():
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        if start:
            if end:
                end = end + DAY
            else:
                end = start + DAY
            edits = edits.filter(datetime__range=[start, end])
        if form.cleaned_data['author']:
            edits = edits.filter(author=form.cleaned_data['author'])
        if form.cleaned_data['taxon']:
            edits = edits.filter(
                coordinate1=form.cleaned_data['taxon'])

    edits = paginate(edits, request)

    return render(request, 'gobotany/display_edits.html', {
        'form': form,
        'edits' : edits,
        })


@permission_required('core.botanist')
def list_edited_taxa(request):
    edits = models.Edit.objects.values('coordinate1', 'datetime',
                                       'author').annotate(last_edit=Max('datetime'))

    edits = paginate(edits, request)

    return render(request, 'gobotany/display_taxa.html', {
        'edits' : edits,
        })


@permission_required('core.botanist')
def edit_pile_character(request, pile_slug, character_slug):

    pile = get_object_or_404(models.Pile, slug=pile_slug)
    character = get_object_or_404(models.Character, short_name=character_slug)
    taxa = list(pile.species.all())

    if character.value_type == 'LENGTH':
        return _edit_pile_length_character(request, pile, character, taxa)
    else:
        return _edit_pile_string_character(request, pile, character, taxa)


def _edit_pile_length_character(request, pile, character, taxa):

    # There is little point in being heroic and trying to create exactly
    # one character value for a pair of

    taxon_ids = {taxon.id for taxon in taxa}
    taxon_values = {}
    lit_sources = {}
    minmaxes = {taxon.id: [None, None] for taxon in taxa}

    for tcv in models.TaxonCharacterValue.objects.filter(
            taxon__in=taxa, character_value__character=character
          ).select_related('character_value'):
        v = tcv.character_value
        taxon_values[tcv.taxon_id] = v
        minmaxes[tcv.taxon_id] = [v.value_min, v.value_max]
        lit_sources[tcv.taxon_id] = (tcv.literary_source and
                                     tcv.literary_source.citation_text or '')

    # Process a POST.

    if 'new_values' in request.POST:
        new_values = request.POST['new_values']
        lit_src = request.POST.get('default_lit_src', '')
        # There is no need to redirect to the lit source edit screen from
        # a length character page
        return _save(request, new_values, character=character,
                     default_lit_source=lit_src, skip_redirect=True)

    # Grabbing one copy of each family once is noticeably faster than
    # using select_related('family') up in the taxon fetch:

    family_ids = set(t.family_id for t in taxa)
    families = models.Family.objects.filter(id__in=family_ids)

    taxa.sort(key=pluck('family_id'))  # always sort() before groupby()!
    taxa_by_family_id = { family_id: list(group) for family_id, group
                          in groupby(taxa, key=pluck('family_id')) }

    def grid():
        """Iterator across families and their taxa."""
        for family in families:
            yield 'family', family, None
            for taxon in taxa_by_family_id.get(family.id, ()):
                name = taxon.scientific_name
                if taxon.id not in simple_ids:
                    name += ' (fk)'
                yield 'taxon', name, minmaxes[taxon.id], lit_sources.get(
                    taxon.id, '')

    partner = which_partner(request)
    simple_ids = set(ps.species_id for ps in models.PartnerSpecies.objects
                     .filter(partner_id=partner.id, simple_key=True))

    valued_ids = {id for id, value in list(minmaxes.items()) if value != ['', ''] }
    coverage_percent_full = len(valued_ids) * 100.0 / len(taxa)
    coverage_percent_simple = (len(simple_ids.intersection(valued_ids))
                     * 100.0 / len(simple_ids.intersection(taxon_ids)))

    return render(request, 'gobotany/edit_pile_length.html', {
        'character': character,
        'coverage_percent_full': coverage_percent_full,
        'coverage_percent_simple': coverage_percent_simple,
        'grid': grid(),
        'pile': pile,
        })


def _edit_pile_string_character(request, pile, character, taxa):

    values = list(character.character_values.all())
    values.sort(key=character_value_key)

    tcvlist = list(models.TaxonCharacterValue.objects
                   .filter(taxon__in=taxa, character_value__in=values))
    value_map = {(tcv.taxon_id, tcv.character_value_id): tcv
                 for tcv in tcvlist}

    # We now have enough information, and can either handle a POST
    # update of specific data or a GET that displays the whole pile.

    if 'new_values' in request.POST:
        new_values = request.POST['new_values']
        lit_src = request.POST.get('default_lit_src', '')
        return _save(request, new_values, character=character,
                     default_lit_source=lit_src)

    # Grabbing one copy of each family once is noticeably faster than
    # using select_related('family') up in the taxon fetch:

    family_ids = set(t.family_id for t in taxa)
    families = models.Family.objects.filter(id__in=family_ids)

    taxa.sort(key=pluck('family_id'))  # always sort() before groupby()!
    taxa_by_family_id = { family_id: list(group) for family_id, group
                          in groupby(taxa, key=pluck('family_id')) }

    partner = which_partner(request)
    simple_ids = set(ps.species_id for ps in models.PartnerSpecies.objects
                     .filter(partner_id=partner.id, simple_key=True))

    # This view takes far too long to render with slow Django templates,
    # so we simply deliver JSON data for the front-end to render there.

    def grid():
        for family in sorted(families, key=pluck('name')):
            yield [family.name]
            family_taxa = taxa_by_family_id[family.id]
            for taxon in family_taxa:
                vector = ''.join(
                    '1' if (taxon.id, value.id) in value_map else '0'
                    for value in values
                    )
                name = taxon.scientific_name
                if taxon.id not in simple_ids:
                    name += ' (fk)'
                yield [name, vector]

    taxa_with_values = set(tcv.taxon_id for tcv in tcvlist)
    taxa_ids = set(taxon.id for taxon in taxa)

    coverage_percent_full = len(taxa_with_values) * 100.0 / len(taxa)
    coverage_percent_simple = (len(simple_ids.intersection(taxa_with_values))
                     * 100.0 / len(simple_ids.intersection(taxa_ids)))

    return render(request, 'gobotany/edit_pile_character.html', {
        'there_are_any_friendly_texts': any(v.friendly_text for v in values),
        'character': character,
        'coverage_percent_full': coverage_percent_full,
        'coverage_percent_simple': coverage_percent_simple,
        'grid': json.dumps(list(grid())),
        'pile': pile,
        'values': values,
        'values_json': json.dumps([value.value_str for value in values]),
        })


@permission_required('core.botanist')
def edit_pile_taxon(request, pile_slug, taxon_slug):
    # Only replace the first hyphen, because some plants have a hyphen
    # in their specific epithet.
    MAX_REPLACE_HYPHEN = 1
    name = taxon_slug.capitalize().replace('-', ' ', MAX_REPLACE_HYPHEN)

    pile = get_object_or_404(models.Pile, slug=pile_slug)
    taxon = get_object_or_404(models.Taxon, scientific_name=name)

    # A POST updates the taxon and redirects, instead of rendering.

    if 'new_values' in request.POST:
        new_values = request.POST['new_values']
        lit_src = request.POST.get('default_lit_src', '')
        return _save(request, new_values, taxon=taxon,
                     default_lit_source=lit_src)

    # Yield a sequence of characters.
    # Each character has .values, a sorted list of character values
    # Each value has .checked, indicating that the species has it.

    common_characters = list(models.Character.objects.filter(
            short_name__in=models.COMMON_CHARACTERS, value_type='TEXT'))
    pile_characters = list(pile.characters.all())

    tcvlist = list(models.TaxonCharacterValue.objects.filter(taxon=taxon)
                   .select_related('character_value'))
    value_map1 = {tcv.character_value_id: tcv for tcv in tcvlist}
    value_map2 = {tcv.character_value.character_id: tcv.character_value
                  for tcv in tcvlist}
    lit_source_map = {tcv.character_value.character_id: (
                      tcv.literary_source and tcv.literary_source.citation_text
                      or '')
                      for tcv in tcvlist}

    def annotated_characters(characters):
        def generator():
            for character in characters:

                if character.value_type == 'LENGTH':
                    value = value_map2.get(character.id)
                    if value is None:
                        character.min = None
                        character.max = None
                    else:
                        character.min = value.value_min
                        character.max = value.value_max
                        character.lit_source = lit_source_map.get(character.id)

                else:
                    character.values = list(character.character_values.all())
                    character.values.sort(key=character_value_key)
                    for value in character.values:
                        value.checked = (value.id in value_map1)
                        if value.checked:
                            character.is_any_value_checked = True

                yield character
        return generator

    return render(request, 'gobotany/edit_pile_taxon.html', {
        'common_characters': annotated_characters(common_characters),
        'pile': pile,
        'pile_characters': annotated_characters(pile_characters),
        'taxon': taxon,
        })


def _save(request, new_values, character=None, taxon=None,
          default_lit_source='', skip_redirect=False):
    dt = timezone.now()
    new_values = json.loads(new_values)

    if character is None:
        get_character = models.Character.objects.get
        character_taxon_value_tuples = [
            (get_character(short_name=name), taxon, v, lit_src)
            for (name, v, lit_src) in new_values
        ]
    elif taxon is None:
        get_taxon = models.Taxon.objects.get
        character_taxon_value_tuples = [
            (character, get_taxon(scientific_name=name), v, lit_src)
            for (name, v, lit_src) in new_values
        ]

    for character, taxon, value, lit_src in character_taxon_value_tuples:
        # Empty values are Nulls
        lit_src = lit_src.strip() or default_lit_source.strip() or None
        if character.value_type == 'LENGTH':
            old_value = _save_length(request, character, taxon, value, lit_src)
        else:
            old_value = _save_textual(request, character, taxon, value, lit_src)

        models.Edit(
            author=request.user.username,
            datetime=dt,
            itemtype='character-value',
            coordinate1=taxon.scientific_name,
            coordinate2=character.short_name,
            old_value=json.dumps(old_value),
            ).save()

    if skip_redirect:
        return redirect(request.path)

    return redirect(dt.strftime(
        '/edit/cv/lit-sources/%Y.%m.%d.%H.%M.%S.%f/?return_to='
        + urllib.parse.quote(request.path)))

def _save_length(request, character, taxon, minmax, lit_source=None):

    tcvs = list(models.TaxonCharacterValue.objects
                .filter(character_value__character=character, taxon=taxon)
                .select_related('character_value'))
    source = None

    if tcvs:
        tcv = tcvs[0]
        if lit_source is not None:
            source, created = models.SourceCitation.objects.get_or_create(
                citation_text=lit_source
            )
            tcv.literary_source = source
            tcv.save()
        value = tcv.character_value
        old_values = [value.value_min, value.value_max]
        is_value_shared = len(value.taxon_character_values.all())

        # Delete any null/null lengths
        if minmax[0] is None and minmax[1] is None:
            tcv.delete()
            tcv.character_value.delete()
            return old_values

        if is_value_shared:
            tcv.delete()
        else:
            value.value_min = minmax[0]
            value.value_max = minmax[1]
            value.save()
            return
    else:
        old_values = [None, None]

    value = models.CharacterValue(
        character=character,
        value_min=minmax[0],
        value_max=minmax[1],
        )
    value.save()

    models.TaxonCharacterValue(character_value=value, taxon=taxon,
                               literary_source=source).save()
    return old_values

def _save_textual(request, character, taxon, vector, lit_source=''):
    values = list(character.character_values.all())
    values.sort(key=character_value_key)

    tcvs = list(models.TaxonCharacterValue.objects.filter(
        character_value__in=values, taxon=taxon))
    tcvmap = {tcv.character_value_id: tcv for tcv in tcvs}
    source = None

    # Modify any empty lit sources if a default lit source is provided
    if lit_source:
        source, created = models.SourceCitation.objects.get_or_create(
            citation_text=lit_source
        )
        for tcv in tcvs:
            if not tcv.literary_source:
                tcv.literary_source = source
                tcv.save()

    old_values = []

    for value, digit in zip(values, vector):
        has_it = value.id in tcvmap
        needs_it = digit == '1'

        if has_it:
            old_values.append(value.value_str)

        if needs_it and not has_it:
            models.TaxonCharacterValue(
                taxon=taxon, character_value=value,
                literary_source=source).save()
        elif not needs_it and has_it:
            tcvmap[value.id].delete()

    return old_values


@permission_required('core.botanist')
def edit_lit_sources(request, dotted_datetime):

    return_to = request.GET.get('return_to', '.')
    if len(return_to) <= 1:
        return_to = request.POST.get('return_to', '.')

    if request.method == 'POST':
        for key in request.POST:
            match = tcvfieldname_re.match(key)
            if not match:
                continue
            number = int(match.group(1))
            tcvs = models.TaxonCharacterValue.objects.filter(id=number)
            if not tcvs:
                # Ignore a tcv that has disappeared in the meantime.
                continue
            tcv = tcvs[0]
            if request.POST[key]:
                citation = models.SourceCitation.objects.get(pk=request.POST[key])
                tcv.literary_source = citation
            else:
                tcv.literary_source = None
            tcv.save()
        return redirect(return_to)

    if dotted_datetime.count('.') != 6:
        raise Http404()

    integers = [int(field) for field in dotted_datetime.split('.')]
    year, month, day, hour, minute, second, us = integers
    d = datetime(year, month, day, hour, minute, second, us)
    d = timezone.make_aware(d, timezone.utc)
    edits = models.Edit.objects.filter(datetime=d, itemtype='character-value')

    # TODO: if no edits, jump away?

    tcvlist = []

    for edit in edits:
        taxon_name = edit.coordinate1
        short_name = edit.coordinate2
        taxon = models.Taxon.objects.get(scientific_name=taxon_name)
        character = models.Character.objects.get(short_name=short_name)
        tcvs = models.TaxonCharacterValue.objects.filter(
            taxon=taxon, character_value__character=character,
            ).select_related(
                'taxon', 'character_value', 'character_value__character'
            )
        tcvlist.extend(tcvs)

    citation_list = models.SourceCitation.objects.all()

    return render(request, 'gobotany/edit_lit_sources.html', {
        'return_to': return_to,
        'tcvlist': tcvlist,
        'citation_list': citation_list
        })
