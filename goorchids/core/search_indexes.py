from gobotany.core.models import Taxon
from gobotany.search.search_indexes import TaxonIndex
from goorchids.core.models import GoOrchidTaxon
from haystack import site


class GoOrchidTaxonIndex(TaxonIndex):

    def read_queryset(self):
        """Exclude taxa that are not marked as ready for display."""
        return self.model._default_manager.filter(ready_for_display=True).all()


site.unregister(Taxon)
site.register(GoOrchidTaxon, GoOrchidTaxonIndex)
