from gobotany.core.models import Taxon
from .core.models import GoOrchidTaxon

for taxon in Taxon.objects.all():
    t = GoOrchidTaxon(taxon_ptr=taxon)
    for field in taxon._meta.fields:
        setattr(t, field.attname, getattr(taxon, field.attname))
    t.save()
