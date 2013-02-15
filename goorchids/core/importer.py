"""Add some goorchids-specific import steps.
"""

from gobotany.core.importer import open_csv
import gobotany.core.importer
import logging


log = logging.getLogger('goorchids.core.importer')


def import_goorchid_taxa(db, filename):
    """Load goorchid-specific species data from a CSV file"""
    log.info('Loading goorchid taxa')

    goorchid_taxon_table = db.table('core_goorchidtaxon')

    for row in open_csv(filename):
        goorchid_taxon_table.get(taxon_ptr_id=row['scientific__name']).set(
            pollination='',
            mycorrhiza='',
            monitoring='',
            propagation='',
            restoration='',
            flowering_phenology='',
        )

    taxon_map = db.map('core_taxon', 'scientific_name', 'id')
    goorchid_taxon_table.replace('taxon_ptr_id', taxon_map)
    goorchid_taxon_table.save()


if __name__ == '__main__':
    gobotany.core.importer.full_import_steps += (
        (import_goorchid_taxa, 'taxa.csv'),
    )

    gobotany.core.importer.main()
