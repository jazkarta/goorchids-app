from datetime import timedelta
from django import forms
from django.db.models import Max
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gobotany.core import models

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
